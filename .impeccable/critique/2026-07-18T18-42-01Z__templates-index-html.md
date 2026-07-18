---
target: templates/index.html
total_score: 29
p0_count: 0
p1_count: 1
timestamp: 2026-07-18T18-42-01Z
slug: templates-index-html
---
# Critique — templates/index.html (Golf Game Scorer)

Method: dual-agent (A: a66012e2184c35019 · B: a015324831e70e5c5)
Browser visualization unavailable — no browser automation tool exposed; deterministic CLI scan only.

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Step rail + loading + sticky Calculate clear; no per-field validation state |
| 2 | Match System / Real World | 4 | Golf vocab correct; banner speaks plainly ("Wins the day") |
| 3 | User Control and Freedom | 3 | Back/Change everywhere; no undo on Remove Player; re-analyze replaces silently |
| 4 | Consistency and Standards | 3 | Strong tokens; Step-3 tables use heavy inline styles that bypass the system |
| 5 | Error Prevention | 2 | Submit-time, first-error-only; no inline cell flagging |
| 6 | Recognition Rather Than Recall | 3 | Hole-numbered boxes win; mid-flow game identity only on the button label |
| 7 | Flexibility and Efficiency | 3 | inputmode numeric, collapsible course, merge; no fast tab-order |
| 8 | Aesthetic and Minimalist | 3 | Sleek overall; Step-3 hole tables still trend to "wall of numbers" |
| 9 | Error Recovery | 3 | Specific copy + scrollIntoView; one-at-a-time, no link to field |
| 10 | Help and Documentation | 2 | Rule blurbs post-hoc on results; no help at Step 2, no SI/handicap tooltip |
| **Total** | | **29/40** | **Good — ship-worthy with fixes (up from 26)** |

## Anti-Patterns Verdict

Largely clean. Absolute bans respected: no side-stripe border-left accents (all removed), no gradient text, no eyebrow-on-every-section, no numbered markers, no text-overflow. Light+green system reads as premium sports/finance, NOT cold-blue SaaS — green is genuinely scarce. Passes the two-altitude category-reflex check. Two faint tells remain: the `.picker-divider` "games" pill (line 941, pure ornament) and repeated inline-styled `.8rem` blurb blocks on Step 3.

Deterministic scan (detect.mjs, exit 2, 58 findings): 48 font-size + 6 radius + 2 color = 56 advisory; 2 warnings. Font-size advisories are expected micro-UI text against a role-based type ramp (not drift). Both warnings are false positives: "Inter overused" (user's explicit choice), broken-image (empty preview-img filled by JS). The 2 color findings are standard rgba(0,0,0) shadows.

## Priority Issues

[P1] First-error-only validation on a 72-cell grid. Each calculate fn returns on the first bad field (e.g. 1510, 1660, 1840); banker fixes one, re-taps, hits next. Fix: collect ALL invalid fields in one pass, red-border each, one summary banner, scroll to first. Command: harden.

[P2] The job ends at "points," not "money." No result screen shows dollars/units owed between players, though PRODUCT.md's success metric is "who owes what." Fix: optional "$ per skin/bet" input + a "Settle up" line under the banner. Command: layout (after scope decision).

[P2] Step-3 hole-by-hole tables re-approach the "cluttered spreadsheet" anti-reference (.8rem cells, multi-line inline-styled, overflow-x scroll; ~2259-2311, 1715-1766). The edit screen was fixed, the results tables weren't. Fix: lead with summary cards; make the raw hole grid a collapsible "Show hole-by-hole". Command: distill then layout.

[P3] Heavy inline styles in Step-3 render functions bypass the design system (e.g. 2211-2306, 1597-1619). Fix: extract to classes. Command: optimize.

[P3] Course-setup opens by default with 36 tiny par/SI inputs ABOVE the scores (details open, line 1391; 40px inputs). Reintroduces the dense grid the collapsible was meant to hide. Fix: ship collapsed by default (drop open), or auto-open only when par/SI missing; bump inputs to 44px. Command: polish.

## Persona Red Flags

The Banker (55, parking lot): first-error loop + open 36-input course grid at top of Step 2 is the biggest friction; app never states the dollar outcome.
Casey (mobile): sticky Calculate + scrollIntoView good; but "Remove player" is instant/silent with no undo — a stray tap loses an 18-score card.
Sam (a11y): well served — aria-labels, focus-visible, reduced-motion, >=4.9:1 muted text, pinch-zoom restored. Gap: #error divs have no aria-live/role=alert, so errors are silent to screen readers.

## Minor Observations

No aria-live on #error-1/2/3; error-3 element is never written to (dead); picker-divider "games" pill is ornament; maxlength=3 allows 999 with no clamp; loading-card shadow rgba(0,0,0,.3) is pure-black (off the ink-tinted shadow rule); 3-dot rail omits the game-pick step.

## Questions to Consider

1. Why does the peak celebrate points and never name a dollar figure, when success = "who owes what"?
2. Why is the least-edited course grid open by default and sitting above the scores?
3. On a 4-player card with several misreads, how many Calculate taps to surface all errors?
4. Is the "games" divider pill earning its place?
5. Is one silent tap deleting 18 verified scores (Remove player, no undo) acceptable one-handed?
