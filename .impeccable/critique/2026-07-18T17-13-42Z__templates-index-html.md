---
target: templates/index.html
total_score: 26
p0_count: 1
p1_count: 2
timestamp: 2026-07-18T17-13-42Z
slug: templates-index-html
---
# Critique — templates/index.html (Golf Game Scorer)

Method: dual-agent (A: a497c04501ccb36f1 · B: ac22807b7067b3e5c)
Browser visualization unavailable — no browser automation tool exposed; deterministic CLI scan only.

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Good stepper + loading copy; no upload %, merged-scorecard append can land off-screen |
| 2 | Match System / Real World | 3 | Golf vocab solid; "HCP Rating" (hole stroke index) is jargon next to "Handicap Index" |
| 3 | User Control and Freedom | 3 | Back on every step; no undo on Remove Player, no re-crop, no un-merge |
| 4 | Consistency and Standards | 2 | Game is chosen twice (Step 0 picker AND Step 2 "Choose Game") with different visuals |
| 5 | Error Prevention | 2 | Validation blocks one hole at a time; no inline cell highlight; message can be off-screen |
| 6 | Recognition Rather Than Recall | 2 | Horizontal-scroll review table forces recall across 70+ cells |
| 7 | Flexibility and Efficiency | 3 | Add player/scorecard, drag-drop, numeric inputmode; no fast tab-order, no par presets |
| 8 | Aesthetic and Minimalist Design | 2 | Grain texture, rainbow header stripe, gold hairlines, serif + tracked eyebrows compete on a sunlit phone |
| 9 | Error Recovery | 3 | Plain, specific messages; banner never scrollIntoView |
| 10 | Help and Documentation | 3 | Excellent inline rule blurbs at results; no help for HCP vs Handicap fields |
| **Total** | | **26/40** | **Acceptable — real friction, clear fixes available** |

## Anti-Patterns Verdict

Not generic-SaaS slop — a committed, hand-tuned theme. But it trips Impeccable's specific bans and the ornateness now reads as "costume" that fights the stated sleek-modern goal.

Deterministic scan (detect.mjs, exit 2, 53 findings):
- side-tab (border-left >1px accent) — 5, lines 244, 452, 649, 1924 (×2). GENUINE; agrees with LLM review.
- broken-image — 1, line 845. FALSE POSITIVE (empty preview-img src populated by JS).
- design-system-font-size — 42 advisories; design-system-color — 4 (all rgba(0,0,0,…) shadows, false positives); design-system-radius — 1 (20px pill on badges). Advisory only.

## Priority Issues

[P0] Step 2 re-asks the game; primary action buried among 5 buttons (lines 877-896). Fix: use state.selectedGame → one primary "Calculate [Game]" button + a small change-game link. Command: distill.

[P1] Review/edit table is the "cluttered spreadsheet" anti-reference at the highest-stakes moment on a phone (44px inputs, .82rem cells, 70+ cells horizontal-scroll; lines 464-528). Fix: per-player card/accordion, ≥48px inputs ≥1rem, surface low-confidence cells first. Command: layout.

[P1] Primary actions not in thumb zone; error banner fires off-screen (showError lines 1071-1075 never scrollIntoView). Fix: scrollIntoView in showError; sticky bottom action bar for Calculate. Command: optimize.

[P2] Contrast failures on secondary text/eyebrows (measured): --ink-dim #8a7d6b on magnolia 3.80:1, on linen 3.57:1; .section-label gold-dk #a68a3a on magnolia 3.14:1; badge-net ~2.89:1. Below 4.5:1. Fix: darken --ink-dim to ~#6f634f, promote section labels off gold. Command: harden.

[P3] Ornate theme fights sleek-modern target (leather grain 52-62, rainbow header stripe 80, gold card hairlines 173-180, serif + gold eyebrows, 4× border-left stripes). Fix: strip grain/stripe, retire border-left, reduce serif to winner name + one display headline, flatten eyebrows, green as accent not flood. Command: quieter.

## Persona Red Flags

The Banker (55, parking lot): squints at 3.80:1 sub-scores in sun; asked to pick game twice; Skins ends with no winner banner and no "X owes Y $Z" summary.
Casey (mobile): off-screen error → double-taps Calculate; 44px cells fat-finger hazard; staggered fade-up delays first tap.
Sam (a11y): sub-4.5:1 tones; maximum-scale=1.0 (line 5) blocks pinch-zoom; outline:none focus replaced by low-contrast glow.

## Minor Observations

maximum-scale=1.0 blocks zoom; Skins (flagship) is the only game with no win-banner; leather-grain body::before z-index 9999 paints over the loading modal (z-index 99); "HCP Rating" vs "Handicap Index" adjacent with no tooltip; result show/hide is manual per-calc-fn and fragile.

## Questions to Consider

1. Why does the most-played game (Skins) end on a spreadsheet, and why does no result screen state "who owes whom, how much"?
2. What is the Step 2 "Choose Game" block for when Step 0 already captured the game?
3. Claude read the card — which cells was it unsure about? Flag the 3 that matter instead of re-verifying all 70.
4. Does the clubhouse costume build trust for a 55-year-old settling $40, or would a Stripe-clean receipt read as more authoritative?
5. If you deleted the serif, grain, and every border-left stripe, would anyone settle a bet worse?
