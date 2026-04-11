"""
Golf Skins Web App
------------------
Flask backend that accepts a scorecard photo, extracts data via Claude vision,
and calculates gross + net skins.

Setup:
  pip install flask anthropic
  set ANTHROPIC_API_KEY=your_key_here   (Windows)
  python app.py

Then open the URL printed in the console from your phone's browser.
"""

import os
import json
import base64
import socket
from dataclasses import dataclass, field
from typing import Optional
from flask import Flask, render_template, request, jsonify
import anthropic


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20 MB max upload


# ---------------------------------------------------------------------------
# Golf logic (self-contained, mirrors golf_skins.py core)
# ---------------------------------------------------------------------------

@dataclass
class Hole:
    number: int
    par: int
    handicap_rating: int


@dataclass
class Player:
    name: str
    handicap: int
    scores: list[int] = field(default_factory=list)


def strokes_received(handicap: int, hole_rating: int) -> int:
    base  = handicap // 18
    extra = 1 if hole_rating <= (handicap % 18) else 0
    return base + extra


def find_skins(
    players: list[Player],
    holes: list[Hole],
    use_net: bool,
) -> dict[int, Optional[str]]:
    results: dict[int, Optional[str]] = {}
    for hole in holes:
        scores: dict[str, int] = {}
        for player in players:
            gross = player.scores[hole.number - 1]
            scores[player.name] = (
                gross - strokes_received(player.handicap, hole.handicap_rating)
                if use_net else gross
            )
        low     = min(scores.values())
        leaders = [name for name, s in scores.items() if s == low]
        results[hole.number] = leaders[0] if len(leaders) == 1 else None
    return results


def vegas_scores(
    team1: list[Player],
    team2: list[Player],
    holes: list[Hole],
) -> dict:
    t1_total = 0
    t2_total = 0
    hole_results = []

    for hole in holes:
        cap = hole.par + 2

        def player_detail(p: Player):
            gross   = p.scores[hole.number - 1]
            strokes = strokes_received(p.handicap, hole.handicap_rating)
            net     = min(gross - strokes, cap)
            birdie  = gross < hole.par
            return {"name": p.name, "gross": gross, "net": net, "strokes": strokes, "birdie": birdie}

        t1_details = [player_detail(p) for p in team1]
        t2_details = [player_detail(p) for p in team2]

        t1_birdied = any(d["birdie"] for d in t1_details)
        t2_birdied = any(d["birdie"] for d in t2_details)

        def pair_digits(details, flip: bool) -> int:
            nets = sorted(d["net"] for d in details)
            if flip:
                nets = list(reversed(nets))
            return nets[0] * 10 + nets[1]

        # A team's score gets flipped when the OPPONENT had a birdie
        t1_number = pair_digits(t1_details, flip=t2_birdied)
        t2_number = pair_digits(t2_details, flip=t1_birdied)

        if t1_number < t2_number:
            t1_pts, t2_pts = t2_number - t1_number, 0
        elif t2_number < t1_number:
            t1_pts, t2_pts = 0, t1_number - t2_number
        else:
            t1_pts, t2_pts = 0, 0

        t1_total += t1_pts
        t2_total += t2_pts

        hole_results.append({
            "number":     hole.number,
            "par":        hole.par,
            "t1_details": t1_details,
            "t2_details": t2_details,
            "t1_number":  t1_number,
            "t2_number":  t2_number,
            "t1_birdied": t1_birdied,
            "t2_birdied": t2_birdied,
            "t1_pts":     t1_pts,
            "t2_pts":     t2_pts,
            "t1_running": t1_total,
            "t2_running": t2_total,
        })

    return {
        "holes":    hole_results,
        "t1_total": t1_total,
        "t2_total": t2_total,
        "differential": abs(t1_total - t2_total),
        "winner": 1 if t1_total > t2_total else (2 if t2_total > t1_total else 0),
    }


QUOTA_POINTS = {-2: 6, -1: 4, 0: 2, 1: 1}  # score vs par → points; 2+ over = 0


def quota_scores(
    players: list[Player],
    holes: list[Hole],
) -> dict:
    quotas    = {p.name: 36 - p.handicap for p in players}
    earned    = {p.name: 0 for p in players}
    hole_results = []

    for hole in holes:
        hole_players = []
        for p in players:
            gross    = p.scores[hole.number - 1]
            diff     = gross - hole.par
            pts      = QUOTA_POINTS.get(diff, 0)
            earned[p.name] += pts
            hole_players.append({
                "name": p.name, "gross": gross,
                "diff": diff, "points": pts,
                "running": earned[p.name],
            })
        hole_results.append({
            "number": hole.number, "par": hole.par,
            "players": hole_players,
        })

    results = [
        {
            "name":       name,
            "quota":      quotas[name],
            "earned":     earned[name],
            "vs_quota":   earned[name] - quotas[name],
        }
        for name in [p.name for p in players]
    ]
    results.sort(key=lambda r: r["vs_quota"], reverse=True)

    return {"holes": hole_results, "results": results}


def nassau_scores(
    team1: list[Player],
    team2: list[Player],
    holes: list[Hole],
) -> dict:
    """
    2v2 best-ball match play Nassau with autos (presses).
    Autos: when a team goes exactly 2 down in any active match within a 9-hole
    segment, a new independent match opens on the next hole. Autos can stack.
    3 segments: front 9 (with autos), back 9 (with autos), total 18 (no autos).
    """
    all_players = team1 + team2
    min_hcp     = min(p.handicap for p in all_players)
    hole_results = []

    for hole in holes:
        def player_detail(p: Player, _min=min_hcp):
            gross   = p.scores[hole.number - 1]
            strokes = strokes_received(p.handicap - _min, hole.handicap_rating)
            return {"name": p.name, "gross": gross, "net": gross - strokes, "strokes": strokes}

        t1_details = [player_detail(p) for p in team1]
        t2_details = [player_detail(p) for p in team2]
        t1_best = min(d["net"] for d in t1_details)
        t2_best = min(d["net"] for d in t2_details)
        result  = 1 if t1_best < t2_best else (2 if t2_best < t1_best else 0)

        hole_results.append({
            "number":     hole.number,
            "par":        hole.par,
            "t1_details": t1_details,
            "t2_details": t2_details,
            "t1_best":    t1_best,
            "t2_best":    t2_best,
            "result":     result,
        })

    def process_segment(hrs: list[dict], with_autos: bool = True) -> Optional[dict]:
        if not hrs:
            return None

        # Each match: start_idx (into hrs), running wins, prev_diff for auto detection
        matches: list[dict] = [
            {"start_idx": 0, "t1w": 0, "t2w": 0, "prev_diff": 0, "is_auto": False}
        ]
        hole_statuses: list[dict] = []

        for idx, hole in enumerate(hrs):
            new_presses: list[dict] = []
            for match in matches:
                if match["start_idx"] > idx:
                    continue
                if hole["result"] == 1:
                    match["t1w"] += 1
                elif hole["result"] == 2:
                    match["t2w"] += 1
                diff = match["t1w"] - match["t2w"]
                # Trigger auto when diff just reaches ±2 (was ±1) and holes remain
                if (with_autos
                        and abs(diff) == 2
                        and abs(match["prev_diff"]) == 1
                        and idx + 1 < len(hrs)):
                    new_presses.append({
                        "start_idx": idx + 1,
                        "t1w": 0, "t2w": 0, "prev_diff": 0, "is_auto": True,
                    })
                match["prev_diff"] = diff

            auto_opens = len(new_presses) > 0
            matches.extend(new_presses)

            statuses = [
                {
                    "match_num": mi,
                    "is_auto":   m["is_auto"],
                    "t1w": m["t1w"], "t2w": m["t2w"],
                    "diff": m["t1w"] - m["t2w"],
                }
                for mi, m in enumerate(matches) if m["start_idx"] <= idx
            ]
            hole_statuses.append({"statuses": statuses, "auto_opens": auto_opens})

        match_results = [
            {
                "match_num":  mi,
                "is_auto":    m["is_auto"],
                "start_hole": hrs[m["start_idx"]]["number"],
                "end_hole":   hrs[-1]["number"],
                "t1_wins":    m["t1w"],
                "t2_wins":    m["t2w"],
                "winner":     1 if m["t1w"] > m["t2w"] else (2 if m["t2w"] > m["t1w"] else 0),
            }
            for mi, m in enumerate(matches)
        ]

        return {"matches": match_results, "hole_statuses": hole_statuses}

    front = [h for h in hole_results if h["number"] <= 9]
    back  = [h for h in hole_results if h["number"] > 9]

    return {
        "holes": hole_results,
        "front": process_segment(front, with_autos=True),
        "back":  process_segment(back,  with_autos=True),
        "total": process_segment(hole_results, with_autos=False),
    }


def better_ball_scores(
    teams: list[list[Player]],
    holes: list[Hole],
) -> dict:
    """For each hole, sum each team's 2 lowest net scores. Lowest team total wins."""
    hole_results = []
    team_totals  = [0] * len(teams)

    for hole in holes:
        team_holes = []
        for ti, team in enumerate(teams):
            net_scores = []
            for player in team:
                gross   = player.scores[hole.number - 1]
                strokes = strokes_received(player.handicap, hole.handicap_rating)
                net_scores.append({
                    "name": player.name, "gross": gross,
                    "net": gross - strokes, "strokes": strokes,
                })
            net_scores.sort(key=lambda x: x["net"])
            best_two   = net_scores[:2]
            team_score = sum(s["net"] for s in best_two) if len(best_two) >= 2 else None
            if team_score is not None:
                team_totals[ti] += team_score
            team_holes.append({"team_score": team_score, "contributors": best_two})

        low = min((t["team_score"] for t in team_holes if t["team_score"] is not None), default=None)
        for th in team_holes:
            th["winner"] = (th["team_score"] == low and low is not None)

        hole_results.append({
            "number": hole.number, "par": hole.par,
            "handicap_rating": hole.handicap_rating,
            "teams": team_holes,
        })

    min_total = min(team_totals)
    return {
        "holes":       hole_results,
        "team_totals": team_totals,
        "min_total":   min_total,
    }


# ---------------------------------------------------------------------------
# Claude vision extraction
# ---------------------------------------------------------------------------

EXTRACTION_PROMPT = """\
This is a golf scorecard. Extract all data and return ONLY valid JSON — no markdown, no explanation.

Required format:
{
  "holes": [
    {"number": 1, "par": 4, "handicap_rating": 7},
    ...
  ],
  "players": [
    {"name": "Player Name", "handicap": 14, "scores": [4, 5, 3, 6, 4, 4, 3, 5, 4, 4, 4, 3, 5, 4, 4, 3, 5, 4]},
    ...
  ]
}

Rules:
- Return holes in order 1–18 (or 1–9 for a 9-hole card).
- The row labeled "Hdcp", "HCP", "Stroke", "Handicap", or similar is the handicap_rating (1 = hardest hole).
- Each handicap_rating 1–18 appears exactly once across all holes.
- scores array length must equal the holes array length and be in hole order.
- If a score cell is blank or illegible, use null.
- Include only players who have at least one score filled in.
- Do not include "Handicap" or "Net" rows as players.
- Each player's name cell contains a small box or subscript where their course handicap index is handwritten. Extract that number as the "handicap" field for each player. If the box is blank or illegible, use null.
"""


def extract_scorecard(image_bytes: bytes, content_type: str) -> dict:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")

    client  = anthropic.Anthropic(api_key=api_key)
    b64     = base64.standard_b64encode(image_bytes).decode()

    # Normalise content type
    if content_type not in ("image/jpeg", "image/png", "image/gif", "image/webp"):
        content_type = "image/jpeg"

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": content_type, "data": b64},
                },
                {"type": "text", "text": EXTRACTION_PROMPT},
            ],
        }],
    )

    raw = message.content[0].text.strip()
    # Strip accidental markdown fences
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return json.loads(raw.strip())


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/extract", methods=["POST"])
def extract():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded."}), 400

    f = request.files["image"]
    if not f.filename:
        return jsonify({"error": "Empty filename."}), 400

    try:
        data = extract_scorecard(f.read(), f.content_type or "image/jpeg")
        return jsonify({"success": True, "data": data})
    except json.JSONDecodeError:
        return jsonify({"error": "Claude could not parse the scorecard into structured data. "
                                 "Try a clearer photo."}), 422
    except ValueError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Extraction failed: {e}"}), 500


@app.route("/calculate", methods=["POST"])
def calculate():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "No data provided."}), 400

    try:
        holes = [
            Hole(number=int(h["number"]), par=int(h["par"]),
                 handicap_rating=int(h["handicap_rating"]))
            for h in body["holes"]
        ]

        players = []
        for p in body["players"]:
            scores = [int(s) for s in p["scores"]]
            players.append(Player(name=p["name"], handicap=int(p["handicap"]),
                                  scores=scores))

        gross_skins = find_skins(players, holes, use_net=False)
        net_skins   = find_skins(players, holes, use_net=True)

        hole_results = []
        for hole in holes:
            player_scores = []
            for p in players:
                gross  = p.scores[hole.number - 1]
                shots  = strokes_received(p.handicap, hole.handicap_rating)
                player_scores.append({
                    "name": p.name, "gross": gross,
                    "net": gross - shots, "strokes": shots,
                })
            hole_results.append({
                "number":          hole.number,
                "par":             hole.par,
                "handicap_rating": hole.handicap_rating,
                "scores":          player_scores,
                "gross_winner":    gross_skins[hole.number],
                "net_winner":      net_skins[hole.number],
            })

        tally = {p.name: {"gross": 0, "net": 0} for p in players}
        for hole in holes:
            gw = gross_skins[hole.number]
            nw = net_skins[hole.number]
            if gw:
                tally[gw]["gross"] += 1
            if nw:
                tally[nw]["net"] += 1

        return jsonify({"success": True, "holes": hole_results, "tally": tally})

    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": f"Invalid data: {e}"}), 422


@app.route("/calculate_quota", methods=["POST"])
def calculate_quota():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "No data provided."}), 400

    try:
        holes = [
            Hole(number=int(h["number"]), par=int(h["par"]),
                 handicap_rating=int(h["handicap_rating"]))
            for h in body["holes"]
        ]
        players = []
        for p in body["players"]:
            scores = [int(s) for s in p["scores"]]
            players.append(Player(name=p["name"], handicap=int(p["handicap"]),
                                  scores=scores))

        if len(players) < 2:
            return jsonify({"error": "At least 2 players are required."}), 422

        result = quota_scores(players, holes)
        return jsonify({"success": True, **result})

    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": f"Invalid data: {e}"}), 422


@app.route("/calculate_vegas", methods=["POST"])
def calculate_vegas():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "No data provided."}), 400

    try:
        holes = [
            Hole(number=int(h["number"]), par=int(h["par"]),
                 handicap_rating=int(h["handicap_rating"]))
            for h in body["holes"]
        ]

        players = []
        for p in body["players"]:
            scores = [int(s) for s in p["scores"]]
            players.append(Player(name=p["name"], handicap=int(p["handicap"]),
                                  scores=scores))

        if len(players) != 4:
            return jsonify({"error": "Vegas requires exactly 4 players."}), 422

        result = vegas_scores(players[:2], players[2:], holes)
        return jsonify({"success": True, **result})

    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": f"Invalid data: {e}"}), 422


@app.route("/calculate_nassau", methods=["POST"])
def calculate_nassau():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "No data provided."}), 400

    try:
        holes = [
            Hole(number=int(h["number"]), par=int(h["par"]),
                 handicap_rating=int(h["handicap_rating"]))
            for h in body["holes"]
        ]
        players = []
        for p in body["players"]:
            scores = [int(s) for s in p["scores"]]
            players.append(Player(name=p["name"], handicap=int(p["handicap"]),
                                  scores=scores))

        if len(players) != 4:
            return jsonify({"error": "Nassau requires exactly 4 players."}), 422

        result = nassau_scores(players[:2], players[2:], holes)
        return jsonify({"success": True, **result})

    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": f"Invalid data: {e}"}), 422


@app.route("/calculate_better_ball", methods=["POST"])
def calculate_better_ball():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "No data provided."}), 400

    try:
        holes = [
            Hole(number=int(h["number"]), par=int(h["par"]),
                 handicap_rating=int(h["handicap_rating"]))
            for h in body["holes"]
        ]

        teams      = []
        team_names = []
        for t in body["teams"]:
            team_names.append(t.get("name", f"Team {len(teams) + 1}"))
            players = []
            for p in t["players"]:
                scores = [int(s) for s in p["scores"]]
                players.append(Player(name=p["name"], handicap=int(p["handicap"]),
                                      scores=scores))
            teams.append(players)

        if len(teams) < 2:
            return jsonify({"error": "At least 2 teams are required for Better Ball."}), 422

        result = better_ball_scores(teams, holes)
        return jsonify({"success": True, "team_names": team_names, **result})

    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": f"Invalid data: {e}"}), 422


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


if __name__ == "__main__":
    ip = _local_ip()
    print("\n  Golf Skins Web App")
    print("  ==================")
    print(f"  Local:  http://localhost:5000")
    print(f"  Phone:  http://{ip}:5000  (must be on same Wi-Fi)\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
