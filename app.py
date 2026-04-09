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
