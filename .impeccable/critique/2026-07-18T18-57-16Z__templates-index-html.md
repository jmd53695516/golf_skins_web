---
target: templates/index.html
total_score: 27
p0_count: 0
p1_count: 1
timestamp: 2026-07-18T18-57-16Z
slug: templates-index-html
---
# Critique — templates/index.html (Golf Game Scorer)

Method: dual-agent (A: af6cc1f76a65bf173 · B: a5019cae1c6bff067)
Browser visualization unavailable — no browser-automation tool exposed; deterministic CLI scan only.

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Step rail + loading + sticky Calculate clear; no per-field validation state |
| 2 | Match System / Real World | 4 | Golf vocab exact; banner + collects/owes copy speak plainly |
| 3 | User Control and Freedom | 2 | Remove Player is instant + silent, no undo — one tap destroys an 18-score card |
| 4 | Consistency and Standards | 3 | Excellent tokens; Step-3 render fns bypass them with pasted inline styles |
| 5 | Error Prevention | 2 | Submit-time, first-error-only; maxlength=3 lets "999" strokes through |
| 6 | Recognition Rather Than Recall | 3 | Hole-numbered boxes win; mid-flow game identity only on Calculate label |
| 7 | Flexibility and Efficiency | 3 | inputmode numeric, merge, sticky CTA; no fast tab order, course grid in the way |
| 8 | Aesthetic and Minimalist | 3 | Steps 0-2 sleek; Step-3 hole tables trend to "wall of numbers" |
| 9 | Error Recovery | 3 | Specific copy + scrollIntoView; not linked to field, silent to screen readers |
| 10 | Help and Documentation | 2 | Rule blurbs only post-hoc on results; no help at Step 2, no SI/handicap tooltip |
| **Total** | | **27/40** | **Acceptable (top of band) — down 2 from prior 29** |

## Anti-Patterns Verdict

Not slop, but a two-tier interface. Steps 0-2 (picker, upload, review) read as premium sports/finance: one scarce green accent, tabular figures, focus-visible rings, thumb-zone sticky Calculate, View-Transition win reveal. Step 3 drops a tier: render functions hand-write the same eyebrow recipe (font-size:.72rem;...uppercase;letter-spacing:.06em) pasted 5x instead of using .section-label. Nassau results table (8 cols of <br>-stacked micro-text, overflow-x:auto) is the "cluttered spreadsheet" DESIGN.md bans. Squint and the silhouette flips premium->scorecard exactly where the verdict lands.

Deterministic scan (detect.mjs, exit 2, 59 findings): 47 font-size + 6 radius + 2 color = 57 advisory drift; 2 warnings. Both warnings are noise: overused-font (Inter, line 9) is the deliberate single-family choice; broken-image (line 1039) is a FALSE POSITIVE (empty <img src=""> in a display:none wrapper, filled by JS at 1345). Advisories cluster in the inline <style> block and the Step-3 render region (.8rem blurbs 1138-1191, Nassau/results tables 1789-2412) — the same region the design review flagged. Detector and design director agree: Step 3 is where the system breaks down. One to eyeball: .74rem !important at line 423.

Visual overlays: none — no browser tool exposed, no rendered-contrast/overflow claims made.

## Overall Impression

Bones are premium and the team knows the target register — win-reveal choreography and the new Skins "Settle Up" panel prove it. But the prior critique's core issues are almost entirely unaddressed, and the money payoff that makes Skins sing is missing from the other four games. Biggest opportunity: close the gap between the premium front half and the under-designed Step 3, starting with the validation loop and money-settlement generalization.

## What's Working

1. Skins settlement system (UI 1100-1110, logic 2020-2079) — greedy pairwise settle-up, tabular figures, correct green/red, plain collects/owes language, live recompute. The PRODUCT success metric ("who owes what") finally on screen. Best thing in the file.
2. Win-reveal choreography (907-915, 1267-1318) — View Transition + banner sweep + count-up + winning cells pulsing in reading order, all behind prefers-reduced-motion. Restrained, premium, on-brand.
3. Token + a11y foundation (11-89) — legacy "gold" remapped onto green, tabular-nums on body, focus-visible rings on every control, safe-area-inset on sticky bar. Base is well-built; problems are all in Step 3 ignoring it.

## Priority Issues

[P1] First-error-only validation across a 72-cell grid — still unfixed. Each calculate fn returns on the first bad field (1856, 1556, 1706, 2255) with one banner; no cell flagged. Banker may need 4-6 Calculate->scroll->fix round-trips. Fix: one pass collects ALL invalid fields, red-borders each, one summary, scroll to first. Command: harden.

[P2] Four of five games dead-end at "points," never money. Settlement exists only for Skins. Quota/Vegas/Better Ball/Nassau (3+ stacked money bets) show banner + tables, no dollars. Success = "who owes what." Fix: extract renderSettlement(nets, container), generalize stake-input + greedySettle. Command: layout.

[P2] Step-3 hole tables re-approach cluttered-spreadsheet anti-reference. .82rem/.8rem tables (498, 677) in overflow-x:auto, Nassau 8 cols of <br>-stacked cells (2371-2418). The verdict screen violates the explicit anti-reference. Fix: lead with a summary card, demote raw grid to collapsed <details> "Show hole-by-hole", bump type to >=.85rem. Command: distill then layout.

[P3] Step-3 render functions bypass the design system via inline styles. Nassau (2322-2417), Quota (1607, 1642-1652), Vegas (1789-1809), Better Ball (2202) hand-write styles; eyebrow recipe pasted 5x instead of .section-label. This is what the 47 font-size advisories are. Fix: extract .result-blurb/.seg-label/.bet-card/.status-chip, delete inline style=. Command: optimize.

[P3] Course setup opens by default — 36 sub-44px inputs above the scores. <details open> (1436) forces least-edited par/SI into first focus above player scores (1496); inputs 40px (573). Fix: drop open (or auto-open only when values missing); bump to 44px. Command: polish.

## Persona Red Flags

The Banker (55, parking lot, one hand): open 36-input course grid + 40px targets at top of Step 2 = fumbling before reaching scores; first-error loop = multiple squinting round-trips; Nassau never states a dollar figure, so he still does the math in his head.
Casey (mobile): Remove Player is instant + silent (1465->1511), no confirm/undo — one thumb tap deletes an 18-score card. Sharpest edge in the file.
Sam (a11y): #error-1/2/3 have no role=alert/aria-live (1029, 1067, 1120) — validation failures silent to screen readers; #error-3 is dead. Positives: aria-labels, focus-visible, reduced-motion, pinch-zoom intact.

## Minor Observations

- Score clamp missing: maxlength=3 (1455) + only s<1 check -> "999" accepted. Add upper bound.
- picker-divider "games" pill (973) is pure ornament — the tiny-uppercase-eyebrow tell. Remove.
- Loading-card shadow rgba(0,0,0,.3) (456) is pure black, off the ink-tinted convention. Retint.
- Step rail omits game-pick step (941-956); weak mid-flow "which game am I in" feedback.
- startOver() (2427) doesn't clear lastSkinsTally — stale settlement data lingers (latent).
- .74rem !important at line 423 — the one advisory using !important.

## Questions to Consider

1. Skins names dollars and it's the best moment — why does Nassau, the most money-driven game, still end at "wins 2 of 3 bets" with no figure?
2. Every banner sits above a gray .8rem overflow-scroll table. Should the raw grid be a "Show hole-by-hole" drill-down rather than the default?
3. On a 4-player card with 5 misreads, how many Calculate taps to surface all 5 errors?
4. What's the argument for the course grid being open by default, above the scores, when it's the data changed least?
5. Is one silent, unconfirmed tap deleting 18 verified scores (Remove Player) defensible on a money screen?
