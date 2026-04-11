# Golf Skins Web App — CLAUDE.md

## Project Overview
Flask + Claude vision web app for scoring golf games from scorecard photos. Users upload a photo, Claude extracts the scorecard data, they review/edit it, then calculate results.

## Stack
- **Backend**: Python / Flask (`app.py`)
- **Frontend**: Single HTML file (`templates/index.html`) — vanilla JS, no framework
- **AI**: Anthropic Claude API (vision) for scorecard extraction
- **Deploy**: Gunicorn (Procfile present)

## Running Locally
```bash
pip install flask anthropic gunicorn
set ANTHROPIC_API_KEY=your_key_here   # Windows
python app.py
```
Opens on `http://localhost:5000`. Also prints the local network IP for phone access.

## Architecture
Everything lives in two files:
- `app.py` — all Python logic and Flask routes
- `templates/index.html` — all HTML, CSS, and JS in one file

There is no build step, no bundler, no database.

## Games Implemented
| Game | Route | Players |
|------|-------|---------|
| Skins | `/calculate` | 2+ |
| 2 Net Better Ball | `/calculate_better_ball` | Teams of 2+ |
| Vegas | `/calculate_vegas` | Exactly 4 |
| Quota | `/calculate_quota` | 2+ |
| Nassau | `/calculate_nassau` | Exactly 4 (2v2) |

## Nassau Rules (important)
- 2v2 best-ball match play, 3 bets: front 9, back 9, total 18
- **Match-play handicapping**: strokes based on difference from the lowest handicap player among all 4. The lowest handicap plays off scratch (0 shots), everyone else gets `their handicap - min handicap` distributed across 18 holes by hole handicap rating.
- **Presses (autos)**: when a team goes exactly 2 down in an active match within a 9-hole segment, a new independent match opens on the next hole. Presses can stack. Front and back 9 have presses; total 18 does not.
- Strokes are always distributed across all 18 holes (not per-9), so a player with 10 shots gets ~5 per nine.

## Key Functions (app.py)
- `strokes_received(handicap, hole_rating)` — distributes handicap strokes across holes
- `find_skins()` — gross and net skins
- `vegas_scores()` — Vegas with birdie flip logic
- `quota_scores()` — Quota (36 − handicap = target)
- `better_ball_scores()` — 2 net better ball
- `nassau_scores()` — Nassau with press logic
- `extract_scorecard()` — Claude vision API call

## UI Flow (index.html)
Step 0 (game picker) → Step 1 (upload) → Step 2 (review/edit table) → Step 3 (results)

The review table is editable — users can fix any values Claude misread. Multiple scorecards can be merged (for multi-team games).

## Style Conventions
- Keep all Python logic in `app.py`, all UI in `templates/index.html`
- No new files unless absolutely necessary
- CSS uses CSS variables defined in `:root` — use `var(--green)`, `var(--gold)`, `var(--red)`, etc.
- JS uses `escHtml()` for any user-supplied strings rendered into HTML
- Error display via `showError(id, msg)` / `clearError(id)`
