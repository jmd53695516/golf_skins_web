---
name: Golf Game Scorer
description: A sleek, phone-first scoreboard for settling golf side-games from a photo.
colors:
  green: "#0a7d54"
  green-deep: "#096b48"
  green-bright: "#12a06d"
  green-tint: "#e7f3ee"
  slate: "#5b6b7a"
  slate-ink: "#3f4b57"
  slate-tint: "#eef1f4"
  red: "#c8324b"
  red-ink: "#9a1b32"
  red-tint: "#fdecef"
  surface: "#ffffff"
  bg: "#f6f7f9"
  inert: "#eaedf1"
  ink: "#14181c"
  ink-mid: "#4a5560"
  ink-dim: "#5f6b78"
  border: "#dfe3e8"
  border-soft: "#e8ebef"
typography:
  display:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "1.9rem"
    fontWeight: 800
    lineHeight: 1.1
    letterSpacing: "-0.03em"
  heading:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "1.15rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "0.95rem"
    fontWeight: 400
    lineHeight: 1.55
  data:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "1.05rem"
    fontWeight: 600
    fontFeature: "tnum"
  label:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "0.68rem"
    fontWeight: 700
    letterSpacing: "0.06em"
rounded:
  sm: "6px"
  md: "10px"
  lg: "14px"
  pill: "20px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
components:
  button-primary:
    backgroundColor: "{colors.green}"
    textColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: "15px"
  button-primary-hover:
    backgroundColor: "{colors.green-deep}"
    textColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: "15px"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.green-deep}"
    rounded: "{rounded.md}"
    padding: "15px"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: "24px"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "0"
  score-input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "7px"
    height: "46px"
  game-btn:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "16px 18px"
  stake-field:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "8px"
    height: "44px"
---

# Design System: Golf Game Scorer

## 1. Overview

**Creative North Star: "The Pocket Scoreboard"**

This is a premium sports/finance app that happens to score golf bets — the feel of Apple Sports or a Stripe receipt, not a country-club interior. Surfaces are near-white, text is a near-black ink, and a single restrained green is the only real color: it appears on the primary action, the current step, and the moment someone wins or gets paid. Everything else is quiet neutral. There is one typeface (Inter) in a range of weights, with tabular figures so scores and dollars line up like a real scoreboard.

The system is calm, fast, and authoritative. The organizer — the "banker" — is settling money in a parking lot on a phone in bright sun, often with older eyes, wanting the math done before people scatter. So the design earns trust through legibility and restraint, not decoration. The screen's job runs to a payoff: a clean winner, then the exact dollars owed between players. When that lands it reads like an official ruling — a number, stated plainly, with the winner and the settlement given the one green moment of emphasis.

This explicitly rejects three things named in PRODUCT.md: the "free scorecard app" look (cartoon mascots, clip-art, novelty type), the cold blue-and-gray SaaS dashboard, and the cluttered gridline spreadsheet. It also rejects its own former self — the ornate Augusta/Masters treatment (deep-green flood, antique gold, Cormorant serif, leather texture) this rebuild deliberately replaced.

**Key Characteristics:**
- Near-white surfaces on a light neutral field; near-black ink
- One green accent, held to ~10% of any screen
- One sans (Inter), all weights, tabular numerals for every score and dollar
- Flat and quiet at rest; the winner banner is the single saturated moment
- Phone-first, one-column, generously sized for arm's-length reading
- The result is a payoff: winner, then a plain-language "who owes whom"

## 2. Colors

A neutral system with one green accent and one slate secondary — color is a signal here, never a texture.

### Primary
- **Green** (`#0a7d54`): The single accent. Primary buttons, the active step, focus rings, selection, gross wins, and the "collects" side of a settlement. Held to roughly 10% of any screen. **Green-Deep** (`#096b48`) is its hover/pressed and small-text tone; **Green-Bright** (`#12a06d`) opens the winner-banner gradient.
- **Green Tint** (`#e7f3ee`): Faint green wash for selected/gross-win cells, the current-step disc, and pressed Nassau bet cards.

### Secondary
- **Slate** (`#5b6b7a`) / **Slate-Ink** (`#3f4b57`) / **Slate-Tint** (`#eef1f4`): The quiet second signal, reserved for *net* results so they never blur with green *gross* results. Slate is the only non-green hue allowed in the data layer.

### Tertiary
- **Red** (`#c8324b`) / **Red-Ink** (`#9a1b32`) / **Red-Tint** (`#fdecef`): Destructive actions (remove player), error banners, invalid-input borders, and the "owes" side of a settlement. Never a solid-red fill.

### Neutral
- **Surface** (`#ffffff`): Cards, inputs, header, step rail.
- **Background** (`#f6f7f9`): The page, secondary panels, and total rows.
- **Inert** (`#eaedf1`): Empty/"no winner" badge fill.
- **Ink** (`#14181c`): Primary text — a near-black, never pure `#000`.
- **Ink-Mid** (`#4a5560`) / **Ink-Dim** (`#5f6b78`): Secondary and tertiary text. Both clear 4.5:1 on white and on the background.
- **Border** (`#dfe3e8`) / **Border-Soft** (`#e8ebef`): Hairlines and dividers.

### Named Rules
**The Green-Is-The-Ruling Rule.** Green is reserved for four things: the primary action, the current step, a win, and money collected. It is never a page or card background and never decoration. Its scarcity is what makes a green cue read as "this is the answer."

**The Gross-Green / Net-Slate Rule.** Gross results tint green; net results tint slate. This is the only place a second color enters the data layer, and it exists so the two scoring categories are never confused at a glance.

**The Money-Has-A-Sign Rule.** In a settlement, "collects" is green (`green-deep`), "owes" is red (`red-ink`), "even" is ink-dim. The color carries the direction of the money before the reader parses the number.

## 3. Typography

**Family:** Inter (with `system-ui` / `-apple-system` fallback). One family, no pairing.

**Character:** A neutral, highly legible humanist-adjacent sans that disappears into the task. Hierarchy comes from weight and size, not from a second face. Headings run tight (negative tracking) and heavy (700–800); body stays comfortable; data runs in tabular figures.

### Hierarchy
- **Display** (800, ~1.9rem, tracking −0.03em): The game-picker headline. The one big statement.
- **Heading** (700, ~1.15rem, tracking −0.01em): Card titles, the collapsible "hole-by-hole" summary, and the app title.
- **Body** (400, ~0.95rem, line-height 1.55): Descriptions and helper copy. Cap prose at 65–75ch.
- **Data** (600, ~1.05rem, tabular): Score inputs, tallies, result numbers, settlement amounts.
- **Label** (700, ~0.68rem, tracking 0.06em, UPPERCASE): Step labels, table headers, the Nassau bet-segment labels. Used sparingly.
- **Caption** (~0.72–0.82rem): The dense results-table micro-text (hole detail, status chips, running score). Deliberately small for data density; never used for prose.

### Named Rules
**The Tabular-Figures Rule.** All numerals are tabular (`font-variant-numeric: tabular-nums`) so scores, points, totals, and dollars align in columns like a scoreboard. Proportional figures in a score grid or a settlement are prohibited.

**The One-Voice Rule.** One typeface, differentiated by weight. No serif, no display face, no second family anywhere.

## 4. Elevation

A light, mostly-flat system. Depth comes from soft, ink-tinted (never gray-black) shadows and from tonal layering — white cards on the `#f6f7f9` field. Surfaces rest quietly and lift a little on hover. The winner banner is the one element allowed real presence: a saturated green gradient with a deeper drop shadow.

### Shadow Vocabulary
- **Resting** (`0 1px 2px rgba(20,24,28,.04), 0 2px 8px rgba(20,24,28,.05)`): Cards, buttons, game rows at rest.
- **Lifted** (`0 4px 16px rgba(20,24,28,.08), 0 12px 28px rgba(20,24,28,.06)`): Hover elevation.
- **Green CTA** (`0 2px 16px rgba(10,125,84,.14)`): The primary green button, so the main action sits slightly proud.
- **Ceremonial** (`0 8px 30px rgba(10,125,84,.28)`): The winner banner only.

### Named Rules
**The Flat-By-Default Rule.** Surfaces are flat at rest. Elevation is a response to interaction (hover) or to importance (the winning banner) — never ambient decoration.

**The Ink-Tinted-Shadow Rule.** Shadows use the ink hue (`rgba(20,24,28,…)`), never pure black (`rgba(0,0,0,…)`). Pure-black shadows read as the 2014-app default; the ink tint keeps depth soft and on-system.

## 5. Components

Quiet, familiar, and consistent — the tool should disappear into the task.

### Buttons
- **Shape:** 10px radius, full-width, ~15px padding.
- **Primary / Emphasis CTA** (`.btn-primary`, `.btn-gold`): Solid green, white text, subtle green shadow; hover deepens to Green-Deep. The one obvious next step per screen.
- **Secondary:** White fill, neutral border, green-deep text; hover brings a green border and faint green tint.
- **Danger:** White fill, red text, soft red border; hover deepens. Never a solid-red fill.
- **Text link** (`.btn-link`): Underlined ink-mid, turns green on hover — for low-stakes escapes like "Change game" and "Undo."

### Cards / Containers
- **Corner Style:** 14px radius.
- **Background:** White surface on the `#f6f7f9` field.
- **Shadow:** Resting only; a single hairline border (`#e8ebef`). No top-edge accent line.
- **Internal Padding:** 24px. Never nest a card inside a card.

### Inputs / Fields
- **Style:** White fill, 1px neutral border, 6px radius. Score boxes are large (46px tall, ~1.05rem) and each is labeled with its hole number; par/SI and handicap fields are 44px.
- **Focus:** Border shifts to green with a soft green glow. No default outline.
- **Invalid:** Border shifts to red (`#c8324b`) with a soft red glow, until the value is corrected — set by a full-pass validation that flags every bad field at once.
- **Stake field:** A 44px field with a leading `$`; drives the live settlement on input.

### Navigation
- **Step rail:** A three-disc chrome band (Upload → Review → Results) under the header. Numbered discs are neutral; the current step fills green with white text; completed steps carry a green-tint fill. The selected game is named in green under the Step-2 heading ("Scoring Nassau"), so the banker always knows which game is live.

### Signature Components
- **Player card:** One card per player — name, handicap, and a wrapping grid of big hole-numbered score boxes. Remove is **undoable**: the card collapses to a quiet "Removed [name] — Undo" strip and the scores stay in the DOM (excluded from the calc) until the window elapses.
- **Course setup:** A collapsible `<details>` holding par and stroke index per hole. Opens by default **only** when par/SI are missing from the extraction; otherwise it stays tucked away above the scores.
- **Winner banner:** The payoff — a green gradient plaque, white heavy sans winner name, and a supporting detail line, revealed with a View Transition, a light sweep, and a count-up. The single saturated moment in the app.
- **Settle Up panel:** Directly under the winner banner, the money answer for every game. A stake field drives a live, zero-sum settlement: per-player "collects / owes" lines in green/red tabular figures, then minimal "A → B $X" pay-lines from a greedy pairwise settle-up.
- **Hole-by-hole disclosure:** The dense per-hole scorecard is a collapsed `<details class="reveal-table">` labeled "Show / Hide" with a rotating chevron. The summary (winner, settlement, standings/bets) is the default; the raw grid is a drill-down.
- **Result cells & badges:** Gross wins tint green, net wins tint slate, both-win splits the two diagonally; total rows tint the `#f6f7f9` field while letting win-cells keep their fill. Nassau bet cards tint green-tint when pressed.

### Named Rules
**The Settle-Up-First Rule.** Every game ends at money, not points. Directly beneath the winner banner, a Settle Up panel names who collects and who owes in exact dollars. The result screen's job is "who owes what," and that answer is the peak.

**The Hole-Grid-Is-A-Drill-Down Rule.** The dense per-hole scorecard is collapsed by default behind "Show hole-by-hole." The default view is the summary — winner, settlement, standings. The spreadsheet is one tap away, never the first thing the eye lands on.

**The Undoable-Destruction Rule.** Destructive actions never fire instantly. Remove Player collapses to an Undo strip and preserves its data until the window closes; a stray thumb tap never loses 18 verified scores.

## 6. Do's and Don'ts

### Do:
- **Do** keep green to ~10% of any screen: primary action, current step, wins, and money collected (the Green-Is-The-Ruling Rule).
- **Do** tint gross results green and net results slate (the Gross-Green / Net-Slate Rule).
- **Do** set every numeral — scores, points, totals, dollars — in tabular figures so they align.
- **Do** use one typeface (Inter) across the whole app, differentiated by weight.
- **Do** lead the results with the winner and the Settle Up payoff; collapse the raw hole grid behind "Show hole-by-hole."
- **Do** keep surfaces white on the `#f6f7f9` field, with near-black `#14181c` ink and ink-tinted shadows.
- **Do** keep it one-column and phone-first, with ≥44px tap targets for arm's-length, one-handed reading.
- **Do** make destructive actions undoable and flag every invalid field in one pass.

### Don't:
- **Don't** reintroduce the retired Augusta costume: no gold, no leather-grain texture, no Cormorant serif, no rainbow header stripe.
- **Don't** make it look like a "free scorecard app" — no cartoon mascots, clip-art, or novelty fonts.
- **Don't** drift toward a generic SaaS dashboard — no cold blue-and-gray, no could-be-any-B2B chrome.
- **Don't** present results as a cluttered spreadsheet — big labeled cells and a summary-first layout, not a wall of tiny gridlined numbers up front.
- **Don't** use a colored side-stripe (`border-left` > 1px) on cards, banners, or panels.
- **Don't** use pure-black shadows (`rgba(0,0,0,…)`); use the ink tint (`rgba(20,24,28,…)`).
- **Don't** use pure white pages or pure black text, and don't let green become a background flood.
- **Don't** end a game at "points" without naming the money.
