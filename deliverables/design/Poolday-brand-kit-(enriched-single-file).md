# Poolday brand kit (enriched, verified against poolday.ai on 2026-09-24)
    
    This is the single-file export of the kit package at `/storage/org/brand-kits/poolday/` (specVersion 3). It supersedes the earlier single-file kit (asset:40b1ad0c-9c0f-4f5a-98a1-ec90a0eb0bf4). Values come from the live site's authored CSS/HTML (`browser dump`), the site's own font files, pixel samples, and the site's own videos. Anything not observed is listed under **Unverified**. Nothing is invented.
    
    Contents: 1. Brand rules · 2. Foundations (retained, unaudited) · 3. Website UI audit (corrected) · 4. Applying the brand · 5. Design tokens (DESIGN.md + styles.css) · 6. Components · 7. Reference assets · 8. Unverified · 9. Icons
    
    ## 1. Brand rules
    
    The three rules, kept verbatim:
    
    1. **Black ground.** Every view starts on `ground` #000000 (the body underlay is `charcoal` #08090A; the caption bar and the observed end card sit on #161616).
    2. **One bright element per view.** On the page that element is the cream pill. The light closing panel (#EEE at 85%) is the bright element of its own view, so its CTA inverts to a dark pill.
    3. **The videos carry the colour.** Chrome is greyscale. Customer hues stay in the customer videos.
    
    Corrections to the earlier kit's rules, based on the live code:
    - Headlines are **Inter 400** (`font-normal`), not 500. The site's `font-serif` class is mapped to Inter.
    - Media cards are **16px** radius (`rounded-2xl`), not 12px. The inner step-video frames are 12px and the closing panel is 24px.
    - Borders, shadows and glass **do exist**: 10% white hairlines, a card drop shadow + inner vignette, 5–15% white glass with a 12px backdrop blur. The earlier "no borders, no shadows" rule is wrong.
    - Tracking is `-0.025em` (Tailwind `tracking-tight`), not -0.03em / -0.02em.
    - CTA hover is `opacity: .9`, not a lift to #fff. The focus ring is the site's own `--ring` #2389E2 at 60%, not cyan.
    - Testimonial quotes use **Fraunces** (a serif), the site's second loaded family.
    - Lucide icons are drawn at **stroke-width 1.75** on the site, not 2.
    
    
## 2. Foundations (retained from the earlier kit, not audited)

This strategy/positioning content was not re-verified. The copy lines match the live homepage. Pricing differs: the live /pricing page says "Your first month at $500", while the homepage closing panel still says "First month $600" (the site is inconsistent).


### Snapshot

| | |
|---|---|
| Company | Poolday AI Inc., San Francisco. Formerly "Viraaal UGC". Founded 2023 ("© 2023 – 2026 Poolday AI"). |
| Founder & CEO | Alexei Chemenda (previously CRO / MD USA at Adikteev, co-founder of MotionLead; founder of Skaalx app studio). |
| Product | An AI agent that edits, generates and assembles on-brand videos. |
| Category claim | "The Media Superintelligence." |
| Proof headline | 100M+ video edits made by Poolday. |
| Funding | $11M raise (as briefed; not yet visible in public databases, which list a $4.9M seed in June 2025 and ~$8.7M total). Known investors: Daphni, Quonota, CASSIUS, Dastore, Financière Saint James; LocalGlobe and Daphni also appear on the site logo wall. |
| Team | ~16 people. |

### Positioning journey

The brand has moved up the stack in three steps, and the current site only makes sense with that history in mind.

1. **Viraaal UGC (2023).** AI actors that generate TikTok-style UGC ads for mobile apps and games. Buyer: user-acquisition managers.
2. **Poolday.ai, AI video editor (2024–25).** Prompt-based editor, AI UGC, voice localisation, integrations with Runway and Veo. Buyer: performance marketers and creative teams.
3. **The Media Superintelligence (2026).** An autonomous agent that learns a brand once and produces any video format: launch films, feature videos, podcast clips, testimonials, explainers. Buyer: marketing and product-marketing leads at tech companies, apps & games, and podcasts.

What stayed constant: speed and volume of production, performance marketing DNA, pricing by output. What changed: from "AI actors" to "the whole production", from gaming UA to tech launches, from self-serve tool to demo-led, configured agent.

### Audience

Three verticals, exactly as the filter tabs name them:

- **Tech Industry** — B2B SaaS and AI startups shipping features weekly (PostHog, Lovable, ClickUp, Dust, Marblism, FullEnrich). Job: launch and feature videos on brand without a motion designer.
- **Apps & Games** — mobile publishers (Unity, Stillfront, Wildlife Studios, WeWard). Job: many ad variants for UA testing.
- **Podcasts** — shows turning full episodes into clips and edited episodes. Job: repurposing at volume.

### Messaging architecture

**Promise:** Finished, on-brand video from a prompt.

**Four pillars** (the "Meet Poolday" sequence, in order):

| Pillar | Site line | What it proves |
|---|---|---|
| Brand once | Teach it your brand once: logo, fonts, colors and Lottie, pixel-exact in every video. | Consistency without a designer |
| Prompt anything | Prompt it with a storyboard, a URL, clips or an idea. It asks what it needs, then finishes the job. | Autonomy: it is an agent, not a tool |
| Point to edit | Click the exact element you want changed. Only that changes, nothing else. | Control: the fear of AI video is losing it |
| Infinite outputs | One prompt, infinite outputs: hooks, actors, styles, key moments, languages and sizes. | Scale: the performance-marketing heritage |

**Proof stack:** volume (100M+ edits) → named customer videos → logo wall → testimonials from a CRO, a head of partnerships, a product designer, a marketing director → price per video.

**Price as message.** "~$5–$25 per finished video", "Month-to-month, no lock-in", "First month $600". Business $1,250/month, Enterprise from $2,500/month, both paid in credits. Price is framed per output, not per seat: keep it that way in all materials.

### Brand attributes

| Is | Is not |
|---|---|
| Confident | Hype-y |
| Compressed | Vague |
| Proof-led | Feature-listy |
| Cinematic | Flashy |
| Operator-built | Corporate |

### Copy bank

Approved lines taken from the live site, to reuse verbatim:

- The Media Superintelligence.
- An AI agent that edits, generates and assembles on-brand videos.
- 100M+ video edits made by Poolday.
- Meet Poolday.
- It asks what it needs, then finishes the job.
- Only that changes, nothing else.
- One prompt, infinite outputs.
- See Poolday in action, live on a call.
- Book a 15 min demo
- Month-to-month, no lock-in.

Recipe caption formula: `<input> + <input>` ("Founder photos + voice") or `<input> to <output>` ("Full episode to snackable content for social").


    ## 3. Website UI audit (corrected against the authored CSS)
    
    | Element | Earlier kit | Live code (2026-09-24) |
    |---|---|---|
    | Page gutter | 48px | 48px (`lg:px-12`) ✓ |
    | Header | 88px | `py-6` + 43px nav CTA ≈ 91px |
    | Wordmark | 24/400 | 24px (`text-2xl`) 400, tracking -0.025em ✓ (live text, no logo file) |
    | Nav links | 15px #ddd, 32 apart | **16px** (`text-base`), foreground/90 (#ddd on black), 32px apart at xl ✓ |
    | Nav CTA | 190×40, 15/500, 24px pad | 15px/500, `px-6 py-2.5` (~43px tall), cream / cream-foreground ✓ |
    | Headline | 88/500, lh .94, −0.03em, #f5f5f5 | 88px, **400**, lh **0.95**, **−0.025em**, #f5f5f5 |
    | Headline → lede | ~30px | 32px (`lg:mt-8`) |
    | Lede | 28/400 #f5f5f5 | 28px, lh 1.3, 400 ✓ |
    | Lede → CTA | ~43px | 40px (`lg:mt-10`) |
    | Hero CTA | 206×50, 32px pad | `px-8 py-3.5`, 15px/500 → ~50px ✓ |
    | Section title | 45/400, −0.02em, tail #878787 | **46px**, lh 1.08, −0.025em; tail = foreground/55 (#878787 on black) ✓ |
    | Filter tabs | 38px, 16px label, inactive #939393, active white 15% | `px-4 py-2`, **15px/500**, gap 4px; inactive foreground/60 (#939393) ✓; active white/15 ✓; hover white/10 |
    | Video grid | 5 cols, 10px gap, radius 12 | 5 cols (lg), **12px gap**, radius **16px**, lead tile 2×2, 56px caption bar #161616 + hairline, bottom fade mask from 68% |
    | Card chrome | "no border/shadow" | ring white/10, shadow `0 10px 30px rgba(0,0,0,.45)`, inset vignette 28px, hover scale 1.015 / 300ms |
    | Halftone | 4px dots / 8px rows, #101012→#2d2d32 | canvas-drawn (source unreadable); 4px / 8px pitch confirmed from pixels; brightest dot samples **#2A–#2E neutral** (not cool) |
    | Grain | not mentioned | `/v2/grain.jpg` fixed overlay, 10% screen, 320px tile; loads (200) but no visible lift in pixel samples |
    | Eyebrows | not measured | 12px uppercase, +0.18em, foreground/55 |
    | Step cards | not measured | glass `rounded-2xl`, border white/10, bg white/5, blur-md, `p-2`, inner video `rounded-xl` |
    | Testimonials | not measured | glass cards, Fraunces 20–22px quote in foreground/90, 44px round avatar with white/15 ring, carousel 600ms `cubic-bezier(.22,1,.36,1)` |
    | Logo marquee | not measured | 30px row height, logos at 1.15em, edge fade mask 12%, linear loop 80s |
    | Closing CTA | "never on light" | **light panel** `bg-panel/85` (#EEE), `rounded-3xl`, text #060606, dark pill `#050505`/cream |
    | theme-color | #06b6d4 | #06b6d4 ✓ (browser chrome only) |
    | Declared, unused on homepage | none noted | `--brand` #305880, `--brand-foreground` #F8F8F8, `--secondary` indigo-500 |
    
    ## 4. Applying the brand
    
    The earlier kit's format table and layout recipes (OG, social, story, slides, end card) are **system extensions, not observed on the site**. Keep them only as suggestions. One conflict: its "video end card" recipe (wordmark + CTA pill + domain) does **not** match the only Poolday end card observed. That end card is a charcoal #161616 kinetic tagline with an iris-gradient rule and no wordmark, CTA or URL (§7 End cards). Don't present the recipe as brand fact.
    
    ## 5. Design tokens
    
    ### DESIGN.md (canonical)
    
    ```markdown
    
---
name: Poolday
version: "2026-09"
specVersion: 3
description: "Poolday's marketing brand (poolday.ai): a black page, one off-white sentence, one off-white pill and a wall of real customer videos. The chrome is greyscale Inter on black, separated by white-alpha hairlines and faint glass, with a procedural scan-dot halftone behind the hero. The only saturated colour on screen comes from the customer videos."
colors:
  ground: "#000000"
  charcoal: "#08090A"
  ink: "#F5F5F5"
  ink-nav: "rgba(245,245,245,0.90)"
  ink-muted: "rgba(245,245,245,0.60)"
  ink-quiet: "rgba(245,245,245,0.55)"
  cream: "#F2F2F2"
  on-cream: "#050505"
  panel: "#EEEEEE"
  on-panel: "#060606"
  glass-active: "rgba(255,255,255,0.15)"
  glass-hover: "rgba(255,255,255,0.10)"
  glass-chip: "rgba(255,255,255,0.08)"
  glass-card: "rgba(255,255,255,0.05)"
  hairline: "rgba(255,255,255,0.10)"
  hairline-strong: "rgba(255,255,255,0.15)"
  surface-bar: "#161616"
  scrim: "rgba(0,0,0,0.70)"
  halftone-dot: "#2E2E2E"
  ring: "#2389E2"
  brand-blue: "#305880"
  on-brand-blue: "#F8F8F8"
  theme-cyan: "#06B6D4"
  og-tile-blue: "#2284DC"
typography:
  display-hero: { fontFamily: Inter, fontSize: 88px, fontWeight: 400, lineHeight: 0.95, letterSpacing: -0.025em, font: fonts/inter.json }
  section-title: { fontFamily: Inter, fontSize: 46px, fontWeight: 400, lineHeight: 1.08, letterSpacing: -0.025em, font: fonts/inter.json }
  lede: { fontFamily: Inter, fontSize: 28px, fontWeight: 400, lineHeight: 1.3, font: fonts/inter.json }
  step-title: { fontFamily: Inter, fontSize: 22px, fontWeight: 400, lineHeight: 1.375, letterSpacing: -0.025em, font: fonts/inter.json }
  wordmark: { fontFamily: Inter, fontSize: 24px, fontWeight: 400, lineHeight: 1, letterSpacing: -0.025em, font: fonts/inter.json }
  nav: { fontFamily: Inter, fontSize: 16px, fontWeight: 400, lineHeight: 1.5, font: fonts/inter.json }
  button: { fontFamily: Inter, fontSize: 15px, fontWeight: 500, lineHeight: 1.5, font: fonts/inter.json }
  tab: { fontFamily: Inter, fontSize: 15px, fontWeight: 500, lineHeight: 1.5, font: fonts/inter.json }
  eyebrow: { fontFamily: Inter, fontSize: 12px, fontWeight: 400, letterSpacing: 0.18em, font: fonts/inter.json }
  card-title: { fontFamily: Inter, fontSize: 13px, fontWeight: 500, lineHeight: 1.25, font: fonts/inter.json }
  card-meta: { fontFamily: Inter, fontSize: 11.5px, fontWeight: 400, lineHeight: 1.25, font: fonts/inter.json }
  quote: { fontFamily: Fraunces, fontSize: 22px, fontWeight: 400, lineHeight: 1.375, font: fonts/fraunces.json }
spacing:
  xs: 4px
  sm: 8px
  grid-gap: 12px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 40px
  gutter: 48px
  section: 80px
rounded:
  chip: 8px
  media-inner: 12px
  card: 16px
  panel: 24px
  pill: 9999px
references:
  logo: references/logos/wordmark-rendered.png
  font: fonts/inter.json
components:
  button-primary: { backgroundColor: "{colors.cream}", textColor: "{colors.on-cream}", typography: "{typography.button}", rounded: "{rounded.pill}", padding: "14px 32px", height: 50px }
  button-nav: { backgroundColor: "{colors.cream}", textColor: "{colors.on-cream}", typography: "{typography.button}", rounded: "{rounded.pill}", padding: "10px 24px", height: 43px }
  button-on-panel: { backgroundColor: "{colors.on-cream}", textColor: "{colors.cream}", typography: "{typography.button}", rounded: "{rounded.pill}", padding: "14px 32px" }
  filter-tab: { backgroundColor: "{colors.glass-active}", textColor: "{colors.ink}", typography: "{typography.tab}", rounded: "{rounded.pill}", padding: "8px 16px" }
  video-card: { backgroundColor: "{colors.glass-card}", rounded: "{rounded.card}", captionBar: "{colors.surface-bar}", captionBarHeight: 56px }
  closing-panel: { backgroundColor: "{colors.panel}", textColor: "{colors.on-panel}", rounded: "{rounded.panel}", padding: 64px }
motion:
  easings:
    ui: "cubic-bezier(.4,0,.2,1)"
    carousel: "cubic-bezier(.22,1,.36,1)"
    marquee: linear
  durations:
    ui: 150ms
    card-hover: 300ms
    carousel: 600ms
    marquee-loop: 80s
    endcard-hold: 1100ms
audio:
  voice: { tone: unverified, gender: unverified, pace: unverified }
  music: { mood: unverified, tempo: unverified, lyrics: false }
  sfx: { ui: none-observed }
spatial:
  gridUnit: 4px
  safeZones: { top: 8%, bottom: 8%, sides: 6% }
  pacing: snappy
---

## Overview
Poolday puts the work on stage and keeps the brand itself quiet. The page is pure black, the text is off-white Inter at regular weight, and there is one off-white pill CTA ("Book a 15 min demo"). The proof is a grid of real customer videos. Depth comes from white-alpha hairlines and faint glass, never from colour. **The videos carry the colour.**

## Do / Don't
- **Black ground, always.** Every view starts on `ground` (#000). `charcoal` is only the body underlay; `surface-bar` (#161616) is the caption bar and the observed end-card ground.
- **One bright element per view.** The cream pill is it. The closing light `panel` counts as the one bright element in its view, so it has no cream pill: its CTA inverts to `on-cream` fill with `cream` label.
- **The videos carry the colour.** UI chrome stays greyscale. Customer hues are never lifted into Poolday chrome.
- Do use regular weight (400) for all headlines. Hierarchy comes from size and tone (`ink` → `ink-quiet`), not weight.
- Do end headlines and section titles with a period: "The Media Superintelligence." "Meet Poolday."
- Do use one CTA verb only: "Book a 15 min demo".
- Don't use bold display type. The one extra-bold word observed is the end-card keyword, and it lives inside a video.
- Don't use `theme-cyan`, `brand-blue` or `ring` as fills or text. `ring` is the focus ring only; the cyan tints mobile browser chrome only.
- Don't invent a secondary/ghost button, a caption style, a lower-third or a branded end-card lockup (see "Unverified").

## Colors
- The ink ladder is one hue at falling alpha: `ink` (headlines, lede, active tab) → `ink-nav` 90% (nav links) → `ink-muted` 60% (inactive tabs) → `ink-quiet` 55% (the second sentence of a section title, eyebrows, card meta). On black these read #ddd / #939393 / #878787.
- Glass is white-alpha over black: `glass-active` 15% (the selected tab), `glass-hover` 10%, `glass-chip` 8% (icon chips), `glass-card` 5% (cards, step frames, testimonial cards). Glass cards pair with `hairline` 10% and `backdrop-filter: blur(12px)`.
- `panel` #eee at 85% opacity is the only light surface: the closing CTA block. Text on it is `on-panel`, and its secondary text is `on-panel` at 70% / 60%.
- `halftone-dot` is the brightest scan-dot, sampled neutral. The dots fade to black at the edge.

## Typography
- One family: **Inter** (variable 100–900, the site's own self-hosted file pinned at `fonts/inter.json`). The site's `font-serif` class is actually mapped to Inter, so the display face is Inter, not a serif.
- **Fraunces** (`fonts/fraunces.json`) is used for one job only: testimonial quote text (`quote`), set in `ink-nav`. Never use it for headlines.
- JetBrains Mono is loaded but not used on the homepage, so it's not part of the brand.
- Tracking: `-0.025em` on the wordmark, hero, section and step titles. UI text has no tracking. Eyebrows are 12px uppercase at `+0.18em` in `ink-quiet`.

## Logo
- The wordmark is live type: "Poolday.ai" in `wordmark` style, `ink` on `ground`, top-left, with no symbol beside it. Set it with `fonts/inter.json`. The raster fallback is `references/logos/wordmark-rendered.png`.
- `references/logos/og-p-tile.png` (blue "P" tile) appears only on the OG card. `references/logos/favicon.ico` is an island emoji. Neither is a video brand mark. Read `references/logos/INDEX.md`.

## Signature elements
- **Two-tone section title**: the claim in `ink` + follow-up in `ink-quiet`, same line, 46px/400 (`components/SectionTitle.tsx`).
- **Pill CTA**: cream, 15px/500, `hover: opacity .9` (`components/Button.tsx`).
- **Video card**: `rounded.card` 16px, `glass-card` fill, 1px `hairline` ring, drop shadow `0 10px 30px rgba(0,0,0,.45)` + inner vignette `inset 0 0 28px rgba(0,0,0,.45)`, and a 56px `surface-bar` caption bar with a `hairline` top border. The bar holds an icon chip, a title (13px/500) and a recipe caption (11.5px, `ink-quiet`). On hover, a `scrim` 70% + 2px blur overlay shows the recipe caption and "Watch with sound". Grid: 5 columns, `grid-gap` 12px, the lead tile spans 2×2, and the grid fades out at the bottom (mask from 68%) (`components/VideoCard.tsx`).
- **Halftone**: a procedural scan-dot ellipse behind the hero: 4px dot pitch, 8px rows, dots swelling toward the centre, always behind type (`components/Halftone.tsx`). There is no image asset.
- **Film grain (authored, effect unconfirmed)**: the site's markup layers `references/textures/grain.jpg` as a fixed overlay (10% opacity, `screen`, 320px tile), and the file loads (HTTP 200). But open areas of the live page sample as pure #000 in both a headless capture and the annotated screenshot, so its visible effect is unconfirmed. Applied as authored on a plain page, it lifts `ground` to about #121212, which breaks "black ground". It's off by default: use `.brand-grain` only as a subtle film texture over video, never over the page ground.
- **Recipe captions**: `<input> + <input>` or `<input> to <output>` ("Screen recording to pixel-perfect video"). See `references/video-examples/INDEX.md`.

## Motion
- UI state changes are colour/opacity only, at `ui` 150ms. Cards scale to 1.015 over `card-hover` 300ms. The testimonial carousel slides at `carousel` 600ms with the `carousel` ease. The logo marquee loops linearly every `marquee-loop` 80s (inline override of the 40s class default).
- The observed Poolday end card (`references/end-cards/`) uses a vertical slot-machine roll with motion blur for the keyword, then an iris-gradient hairline grows to full width, holds `endcard-hold`, and collapses to a centre dash as the text fades.

## Audio
- Not observed. Every homepage video preview is silent, so the `audio` tokens are placeholders marked `unverified`. Confirm them with the brand before use.

## Spatial & Timing
- The page gutter is 48px, header padding is 24px vertical, and nav links are 32px apart. The hero stack is headline → 32px → lede → 40px → CTA. Sections are 80px apart, separated by a `hairline` top border.
- Video safe zones aren't specified by the brand. The `spatial.safeZones` values are conservative defaults, not observed values.

## Unverified (do not invent)
- A Poolday caption/subtitle style (three customer videos show three different styles).
- A branded end-card lockup with wordmark, CTA or URL (the one observed end card has none).
- Lower-thirds (only one customer-styled example was observed), voice, music and SFX.
- The halftone canvas source: its exact colours and falloff curve were measured from pixels, not code.

```

### styles.css

```css
/* Poolday — LOOK-primitives sheet. Raw CSS (no Tailwind import, no @apply).
   :root is a projection of DESIGN.md tokens; DESIGN.md is canonical.
   Fonts: load fonts/inter.json (and fonts/fraunces.json for quotes) via the surface's font loader,
   registering them as family names "Inter" / "Fraunces". */
:root {
  /* colour */
  --brand-ground: #000000;
  --brand-charcoal: #08090a;
  --brand-ink: #f5f5f5;
  --brand-ink-nav: rgba(245, 245, 245, 0.9);
  --brand-ink-muted: rgba(245, 245, 245, 0.6);
  --brand-ink-quiet: rgba(245, 245, 245, 0.55);
  --brand-cream: #f2f2f2;
  --brand-on-cream: #050505;
  --brand-panel: #eeeeee;
  --brand-on-panel: #060606;
  --brand-glass-active: rgba(255, 255, 255, 0.15);
  --brand-glass-hover: rgba(255, 255, 255, 0.1);
  --brand-glass-chip: rgba(255, 255, 255, 0.08);
  --brand-glass-card: rgba(255, 255, 255, 0.05);
  --brand-hairline: rgba(255, 255, 255, 0.1);
  --brand-hairline-strong: rgba(255, 255, 255, 0.15);
  --brand-surface-bar: #161616;
  --brand-scrim: rgba(0, 0, 0, 0.7);
  --brand-halftone-dot: #2e2e2e;
  --brand-halftone-dot-dim: #0a0a0a;
  --brand-ring: #2389e2;
  --brand-ring-soft: rgba(35, 137, 226, 0.6);
  --brand-blue: #305880;
  --brand-on-blue: #f8f8f8;
  --brand-theme-cyan: #06b6d4;
  /* observed only on the Poolday end-card rule (matches the platform iris) */
  --brand-iris-rule: linear-gradient(90deg, #8ec5ff 0%, #b8a9ff 20%, #f5a8f0 42%, #ffd2a8 64%, #a8f0d8 84%, #8ec5ff 100%);

  /* type */
  --brand-font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --brand-font-quote: "Fraunces", Georgia, serif;
  --brand-tracking-tight: -0.025em;

  /* space / radius */
  --brand-space-xs: 4px;
  --brand-space-sm: 8px;
  --brand-space-grid: 12px;
  --brand-space-md: 16px;
  --brand-space-lg: 24px;
  --brand-space-xl: 32px;
  --brand-space-2xl: 40px;
  --brand-gutter: 48px;
  --brand-section: 80px;
  --brand-radius-chip: 8px;
  --brand-radius-media: 12px;
  --brand-radius-card: 16px;
  --brand-radius-panel: 24px;
  --brand-radius-pill: 9999px;

  /* elevation */
  --brand-shadow-card: 0 10px 30px rgba(0, 0, 0, 0.45);
  --brand-shadow-vignette: inset 0 0 28px rgba(0, 0, 0, 0.45);
  --brand-blur-glass: 12px;
  --brand-caption-bar: 56px;

  /* halftone (procedural — read by components/Halftone.tsx) */
  --brand-halftone-pitch: 4px;
  --brand-halftone-row: 8px;
}

/* ground + texture */
.brand-ground { background: var(--brand-ground); color: var(--brand-ink); font-family: var(--brand-font-sans); }
.brand-grain {
  position: absolute; inset: 0; pointer-events: none;
  opacity: 0.1; mix-blend-mode: screen;
  background-size: 320px 320px; background-repeat: repeat;
  /* set background-image to the re-materialized references/textures/grain.jpg url */
}

/* type scale */
.brand-display-hero { font-family: var(--brand-font-sans); font-size: 88px; font-weight: 400; line-height: 0.95; letter-spacing: var(--brand-tracking-tight); color: var(--brand-ink); }
.brand-section-title { font-family: var(--brand-font-sans); font-size: 46px; font-weight: 400; line-height: 1.08; letter-spacing: var(--brand-tracking-tight); color: var(--brand-ink); text-align: center; text-wrap: balance; margin: 0; }
.brand-section-title__tail { color: var(--brand-ink-quiet); }
.brand-lede { font-family: var(--brand-font-sans); font-size: 28px; font-weight: 400; line-height: 1.3; color: var(--brand-ink); }
.brand-step-title { font-family: var(--brand-font-sans); font-size: 22px; font-weight: 400; line-height: 1.375; letter-spacing: var(--brand-tracking-tight); color: var(--brand-ink); }
.brand-wordmark { font-family: var(--brand-font-sans); font-size: 24px; font-weight: 400; line-height: 1; letter-spacing: var(--brand-tracking-tight); color: var(--brand-ink); }
.brand-nav { font-family: var(--brand-font-sans); font-size: 16px; font-weight: 400; line-height: 1.5; color: var(--brand-ink-nav); }
.brand-eyebrow { font-family: var(--brand-font-sans); font-size: 12px; font-weight: 400; letter-spacing: 0.18em; text-transform: uppercase; color: var(--brand-ink-quiet); }
.brand-quote { font-family: var(--brand-font-quote); font-size: 22px; font-weight: 400; line-height: 1.375; color: var(--brand-ink-nav); }

/* surfaces */
.brand-card { background: var(--brand-glass-card); border: 1px solid var(--brand-hairline); border-radius: var(--brand-radius-card); backdrop-filter: blur(var(--brand-blur-glass)); }
.brand-panel { background: color-mix(in srgb, var(--brand-panel) 85%, transparent); color: var(--brand-on-panel); border-radius: var(--brand-radius-panel); backdrop-filter: blur(4px); }
.brand-hairline-top { border-top: 1px solid var(--brand-hairline); }

/* actions */
.brand-btn {
  display: inline-flex; align-items: center; justify-content: center; white-space: nowrap;
  border: 0; border-radius: var(--brand-radius-pill); cursor: pointer; text-decoration: none;
  font-family: var(--brand-font-sans); font-size: 15px; font-weight: 500; line-height: 1.5;
  transition: opacity 150ms cubic-bezier(.4, 0, .2, 1);
}
.brand-btn:hover { opacity: 0.9; }
.brand-btn:focus-visible { outline: 2px solid var(--brand-ring-soft); outline-offset: 2px; }
.brand-btn--primary { background: var(--brand-cream); color: var(--brand-on-cream); }
.brand-btn--on-panel { background: var(--brand-on-cream); color: var(--brand-cream); }
.brand-btn--lg { padding: 14px 32px; }
.brand-btn--md { padding: 10px 24px; }
.brand-tab {
  display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px;
  border-radius: var(--brand-radius-pill); font-family: var(--brand-font-sans); font-size: 15px; font-weight: 500; line-height: 1.5;
  color: var(--brand-ink-muted); background: transparent; transition: background-color 150ms, color 150ms;
}
.brand-tab:hover { background: var(--brand-glass-hover); color: var(--brand-ink); }
.brand-tab--active { background: var(--brand-glass-active); color: var(--brand-ink); }

/* video card */
.brand-video-grid { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: var(--brand-space-grid); -webkit-mask-image: linear-gradient(to bottom, #000 68%, transparent 100%); mask-image: linear-gradient(to bottom, #000 68%, transparent 100%); }
.brand-video-card {
  position: relative; display: flex; flex-direction: column; overflow: hidden; height: 100%;
  border-radius: var(--brand-radius-card); background: var(--brand-glass-card);
  box-shadow: 0 0 0 1px var(--brand-hairline), var(--brand-shadow-card);
  transition: transform 300ms cubic-bezier(.4, 0, .2, 1);
}
.brand-video-card--lead { grid-column: span 2; grid-row: span 2; }
.brand-video-card:hover { transform: scale(1.015); }
.brand-video-card__media { position: relative; flex: 1 1 auto; min-height: 0; overflow: hidden; }
.brand-video-card__media > * { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.brand-video-card__vignette { position: absolute; inset: 0; pointer-events: none; box-shadow: var(--brand-shadow-vignette); }
.brand-video-card__hover {
  position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: flex-end; gap: 8px; padding: 12px;
  background: var(--brand-scrim); backdrop-filter: blur(2px); opacity: 0; transition: opacity 300ms;
  font-family: var(--brand-font-sans); font-size: 15px; line-height: 1.375; color: rgba(245, 245, 245, 0.9);
}
.brand-video-card:hover .brand-video-card__hover, .brand-video-card--reveal .brand-video-card__hover { opacity: 1; }
.brand-video-card__sound { font-size: 12px; font-weight: 500; color: rgba(245, 245, 245, 0.7); }
.brand-video-card__bar {
  display: flex; align-items: center; gap: 10px; height: var(--brand-caption-bar); flex-shrink: 0; padding: 0 10px;
  background: var(--brand-surface-bar); border-top: 1px solid var(--brand-hairline);
}
.brand-video-card__chip {
  display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; flex-shrink: 0;
  border-radius: var(--brand-radius-chip); background: var(--brand-glass-chip); box-shadow: 0 0 0 1px var(--brand-hairline); color: rgba(245, 245, 245, 0.85);
}
.brand-video-card__title { display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-family: var(--brand-font-sans); font-size: 13px; font-weight: 500; line-height: 1.25; color: var(--brand-ink); }
.brand-video-card__recipe { display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-family: var(--brand-font-sans); font-size: 11.5px; line-height: 1.25; color: var(--brand-ink-quiet); }

/* halftone host */
.brand-halftone { position: absolute; inset: 0; pointer-events: none; }
.brand-halftone > canvas { width: 100%; height: 100%; display: block; }
```

## 6. Components

These are the signature four, styled only by `styles.css`. Assets are injected, never resolved inside the component. NavBar, FilterTabs, Hero and Icon from the earlier kit were not carried over: FilterTabs lives on as `.brand-tab` atoms, and Hero is a composition of the pieces below.


### Button.tsx

```tsx
import React from "react";

/**
 * Poolday pill CTA. Styled only by styles.css (.brand-btn*).
 * One per view. The site has no secondary/ghost variant, so don't add one.
 * variant "on-panel" = the inverted pill used inside the light closing panel.
 */
export type ButtonProps = {
  children?: React.ReactNode;           // default label: "Book a 15 min demo"
  size?: "md" | "lg";                   // md = nav (10px 24px), lg = hero/closing (14px 32px)
  variant?: "primary" | "on-panel";
  href?: string;
  className?: string;
  style?: React.CSSProperties;
};

export const Button: React.FC<ButtonProps> = ({ children = "Book a 15 min demo", size = "lg", variant = "primary", href, className = "", style }) => {
  const cls = `brand-btn brand-btn--${variant} brand-btn--${size} ${className}`.trim();
  return href ? <a className={cls} href={href} style={style}>{children}</a> : <button type="button" className={cls} style={style}>{children}</button>;
};
export default Button;
```


### SectionTitle.tsx

```tsx
import React from "react";

/**
 * Two-tone section title: the claim in ink + the follow-up in ink-quiet, on one line.
 * 46px / 400 / -0.025em. Both sentences end with a period. Never bold, never more than two sentences.
 * e.g. lead="100M+ video edits made by Poolday." tail="Some examples here."
 */
export type SectionTitleProps = {
  lead: React.ReactNode;
  tail?: React.ReactNode;
  as?: "h1" | "h2" | "h3";
  className?: string;
  style?: React.CSSProperties;          // pass fontSize here to scale for a canvas
};

export const SectionTitle: React.FC<SectionTitleProps> = ({ lead, tail, as = "h2", className = "", style }) => {
  const Tag = as;
  return (
    <Tag className={`brand-section-title ${className}`.trim()} style={style}>
      {lead}
      {tail ? <> <span className="brand-section-title__tail">{tail}</span></> : null}
    </Tag>
  );
};
export default SectionTitle;
```


### VideoCard.tsx

```tsx
import React from "react";

/**
 * Poolday proof-grid tile: 16px glass card, hairline ring + drop shadow, inner vignette,
 * a 56px #161616 caption bar (icon chip + title + recipe), and a hover scrim that
 * reveals the recipe caption and "Watch with sound".
 * The video is INJECTED (Remotion: <AssetVideo …/> / <OffthreadVideo/>; web: <video muted autoPlay loop/>),
 * because the component never resolves assets itself. Example sources: references/video-examples/*.mp4.
 * Place inside a .brand-video-grid (5 cols, 12px gap). The lead tile uses lead={true} (2x2).
 */
export type VideoCardProps = {
  media?: React.ReactNode;
  title: string;                         // "Dust - Agent demo video"
  recipe?: string;                       // "Screen recording to pixel-perfect video"
  icon?: React.ReactNode;                // 16px Lucide line icon (stroke 1.75), e.g. clapperboard
  lead?: boolean;
  reveal?: boolean;                      // force the hover overlay (for video/stills)
  soundLabel?: string | null;            // default "Watch with sound"; null hides
  className?: string;
  style?: React.CSSProperties;
};

export const VideoCard: React.FC<VideoCardProps> = ({ media, title, recipe, icon, lead, reveal, soundLabel = "Watch with sound", className = "", style }) => (
  <div className={`brand-video-card${lead ? " brand-video-card--lead" : ""}${reveal ? " brand-video-card--reveal" : ""} ${className}`.trim()} style={style}>
    <div className="brand-video-card__media">
      {media}
      <div className="brand-video-card__vignette" aria-hidden />
      {recipe ? (
        <span className="brand-video-card__hover" aria-hidden>
          <span>{recipe}</span>
          {soundLabel ? <span className="brand-video-card__sound">▶ {soundLabel}</span> : null}
        </span>
      ) : null}
    </div>
    <span className="brand-video-card__bar">
      <span className="brand-video-card__chip">{icon}</span>
      <span style={{ minWidth: 0, flex: 1 }}>
        <span className="brand-video-card__title">{title}</span>
        {recipe ? <span className="brand-video-card__recipe">{recipe}</span> : null}
      </span>
    </span>
  </div>
);
export default VideoCard;
```


### Halftone.tsx

```tsx
import React, { useLayoutEffect, useRef } from "react";

/**
 * Procedural scan-dot halftone (no image asset; the live site draws it on a canvas).
 * Measured: dots on a 4px pitch (--brand-halftone-pitch), rows every 8px (--brand-halftone-row),
 * dots swell toward the ellipse centre and brighten from --brand-halftone-dot-dim to --brand-halftone-dot.
 * Always behind type; keep it a texture (brightest dot ≈ #2e2e2e).
 * Remotion: pass `phase` from useCurrentFrame() for a slow drift; omit it for a static field.
 * Put it inside a positioned parent; width/height = the canvas backing size in px.
 */
export type HalftoneProps = {
  width: number;
  height: number;
  centerX?: number;   // 0..1, default 0.48 (the site sits slightly left of centre)
  centerY?: number;   // 0..1, default 0.55
  radiusX?: number;   // fraction of width, default 0.34
  radiusY?: number;   // fraction of height, default 0.42
  phase?: number;     // drift driver (e.g. frame); 0 = static
  className?: string;
};

const readVar = (el: Element, name: string, fallback: number | string) => {
  const v = getComputedStyle(el).getPropertyValue(name).trim();
  return v || String(fallback);
};
const hexToRgb = (hex: string) => {
  const h = hex.replace("#", "");
  const n = parseInt(h.length === 3 ? h.split("").map((c) => c + c).join("") : h, 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
};

export const Halftone: React.FC<HalftoneProps> = ({ width, height, centerX = 0.48, centerY = 0.55, radiusX = 0.34, radiusY = 0.42, phase = 0, className = "" }) => {
  const ref = useRef<HTMLCanvasElement>(null);
  useLayoutEffect(() => {
    const c = ref.current; if (!c) return;
    const ctx = c.getContext("2d"); if (!ctx) return;
    const pitch = parseFloat(readVar(c, "--brand-halftone-pitch", 4));
    const row = parseFloat(readVar(c, "--brand-halftone-row", 8));
    const hi = hexToRgb(readVar(c, "--brand-halftone-dot", "#2e2e2e") as string);
    const lo = hexToRgb(readVar(c, "--brand-halftone-dot-dim", "#0a0a0a") as string);
    ctx.clearRect(0, 0, width, height);
    const cx = width * centerX + Math.sin(phase / 90) * pitch * 2;
    const cy = height * centerY + Math.cos(phase / 120) * row;
    const rx = width * radiusX, ry = height * radiusY;
    for (let y = row / 2; y < height; y += row) {
      for (let x = pitch / 2; x < width; x += pitch) {
        const d = Math.hypot((x - cx) / rx, (y - cy) / ry);
        if (d >= 1) continue;
        const t = Math.pow(1 - d, 0.8);                 // 1 at centre → 0 at edge
        const h = 1 + t * 2;                            // 1px → 3px tall
        const w = t > 0.5 ? 2 : 1;                      // 1px → 2px wide
        const r = Math.round(lo[0] + (hi[0] - lo[0]) * t), g = Math.round(lo[1] + (hi[1] - lo[1]) * t), b = Math.round(lo[2] + (hi[2] - lo[2]) * t);
        ctx.fillStyle = `rgb(${r},${g},${b})`;
        ctx.fillRect(Math.round(x - w / 2), Math.round(y - h / 2), w, h);
      }
    }
  }, [width, height, centerX, centerY, radiusX, radiusY, phase]);
  return (
    <div className={`brand-halftone ${className}`.trim()} aria-hidden>
      <canvas ref={ref} width={width} height={height} />
    </div>
  );
};
export default Halftone;
```


## 7. Reference assets

All assets are materialized as org assets. Resolve them by assetId (`assets get <id> --materialize`). Sidecars live under `references/<category>/`.

| Path | assetId |
|---|---|

| `references/end-cards/one-prompt-endcard-still.png` | asset:f6bd71c3-2bea-4e31-83b9-ab95b053f0b7 |
| `references/end-cards/one-prompt-endcard.mp4` | asset:3244c494-a748-45bc-acf2-7a06d80ec50a |
| `references/logos/favicon.ico` | asset:417d7740-5896-4b1c-8657-7f4e6ca3452e |
| `references/logos/og-p-tile.png` | asset:36da74e3-f35c-490f-b4fd-fc8e9ae974e5 |
| `references/logos/wordmark-rendered.png` | asset:fcdfcadc-b62f-4efc-9e22-1ec909bc431d |
| `references/social/og-card.png` | asset:e8e824e9-8346-4183-b205-87febe1eee1e |
| `references/textures/grain.jpg` | asset:454f70bf-88da-4f21-a312-ce6be300f06e |
| `references/video-examples/clickup-ai.mp4` | asset:94eac023-3cc2-4635-aa82-13f9770b95f3 |
| `references/video-examples/dust-agent-demo.mp4` | asset:d651981f-02dd-43e7-a044-a81390e3e2e9 |
| `references/video-examples/fullenrich-explainer.mp4` | asset:789d542b-d9e6-49e4-947d-a0f8f33a6659 |
| `references/video-examples/lovable-ig-pitch.mp4` | asset:225af9b5-bd7b-4091-a36a-3fcf44a83155 |
| `references/video-examples/marblism-launch-film.mp4` | asset:5de03ff1-5a0a-467a-8b2b-cde6349b9aa1 |
| `references/video-examples/podcast-social-clips.mp4` | asset:0dd72351-54fa-485d-ad2f-27aa884b2205 |
| `references/video-examples/posthog-genai-launch.mp4` | asset:c05fd86d-21db-4bcb-8c1f-822d4f010cef |
| `references/video-examples/smart-reframe.mp4` | asset:fe05cd10-c211-4e94-a58a-71eca42daa69 |
| `fonts/fraunces.json` | asset:9facf9b9-7388-4cd1-9b90-014d6a886b88 |
| `fonts/inter.json` | asset:523c0306-df75-4ff2-a353-722ac1b0eb65 |


### Logos

The site has no logo file. The logo is the live-type wordmark "Poolday.ai": Inter 400, 24px in the nav, tracking -0.025em, `--brand-ink` on black. Prefer live type set with `fonts/inter.json` over any raster.

- `wordmark-rendered.png`: "Poolday.ai" rendered at 240px from the site's own Inter file (fonts/inter.json), #f5f5f5 on #000, 1600×480. Use it only where live type can't be set. It is a faithful re-render, not a file published by Poolday.
- `favicon.ico`: the live /favicon.ico. It is a multi-size ICO (16/32/48) of a desert-island emoji glyph on black. Treat it as a browser-tab icon only, never as a brand mark in video.
- `og-p-tile.png`: a 48×48 crop of the blue rounded-square "P" tile from the live /api/og card (blue gradient ~#2284dc→#1b6fbe, white P). It appears ONLY on the OG card. It is low-res and has no source file, so don't scale it up or use it as a primary mark.

Rules: never recolour, outline or stretch the wordmark. Never invent a symbol. On a light fill (the closing panel), use the dark label colour.


### Social

- `og-card.png`: the live og:image (https://poolday.ai/api/og), 1200×630. It shows the blue "P" tile + "poolday.ai" lowercase top-left, "The Media Superintelligence." headline, the definition lede in grey, and stats "100M+ video edits made" / "700k+ agent runs" with superscript labels. "Poolday" sits bottom-right. The background is near-black with two soft blue radial glows (~#0f324f).

The OG card is the ONE place the site uses blue glows and the P tile. The card's type looks like the OG renderer default (Noto/Open-Sans-like), not Inter, so don't copy its type. The static /og.png is a legacy light/mono site capture that was rejected (see research ledger).


### Textures

- `grain.jpg`: the live film-grain tile (/v2/grain.jpg, 583×360 light-grey noise). The site lays it over the whole page as a fixed overlay: `opacity: 0.1; mix-blend-mode: screen; background-size: 320px 320px; repeat`. That is `.brand-grain` in styles.css. **Status: authored, effect unconfirmed.** The file loads (HTTP 200), but open areas of the live page sample as #000000 in both a headless capture and the user's annotated screenshot. Applied as authored on a plain page, it lifts black to ~#121212 (checked in a test render). Keep it off by default. If used, keep it at 10% or less and only over video, never on the page ground.

The hero **halftone** has no asset: it is drawn live on a full-viewport `<canvas>` (source not readable; it doesn't render headless). It is procedural, so use `components/Halftone.tsx`. The parameters were measured from a screenshot: dots on a 4px pitch, rows every 8px, sampled dot colour ≈ #2a2a2a–#2e2e2e (neutral), fading to black at the ellipse edge.


### Video examples: customer output from the homepage proof grid

These are 10.0s silent previews from the site's own grid (`videos/previews/*.mp4`). None has an audio track, an end card or a Poolday watermark. Their colours belong to the customers: they are what "the videos carry the colour" means. Never sample them as Poolday colours. Title / recipe caption / vertical are verbatim from the site.

- `marblism-launch-film.mp4`: 640×360. "Marblism - Product Launch Video" / "Made with brand kit + single prompt" / Tech. This is the lead tile (2×2). It has kinetic uppercase type, gold/red/green, and no captions.
- `posthog-genai-launch.mp4`: 640×360. "PostHog - AI Feature Launch" / "Imported Lottie files for motion graphics + brand kit" / Tech. Cream + amber, chat bubbles, "WAIT IS OVER / IT'S LIVE".
- `lovable-ig-pitch.mp4`: 480×854 (9:16). "Lovable - Instagram Ad" / "Made with founder photo + voice clone + brand kit" / Tech. Split screen, founder talking head, captions in UPPERCASE bold white sans, no box, 1–3-word chunks, mid-frame.
- `clickup-ai.mp4`: 640×360. "ClickUp - Product Feature Video" / "Automated video update from roadmap" / Tech. Indigo/violet/pink gradients, "ask anything".
- `dust-agent-demo.mp4`: 640×360. "Dust - Agent demo video" / "Screen recording to pixel-perfect video" / Tech. The only lower-third observed: a white rounded box with name (bold) over role (regular), in the customer's style.
- `smart-reframe.mp4`: 480×854. "Smart Reframe Highlights" / "Auto-reframed highlights (16:9 and 9:16)" / Podcasts. Bold white sans captions mid-frame; the yellow emphasis is uncertain.
- `podcast-social-clips.mp4`: 480×854. "Podcast to 8 Social Clips" / "Full episode to snackable content for social" / Podcasts. French captions, extra-bold lowercase white, active word turns yellow (~#ffdd00), lower area.
- `fullenrich-explainer.mp4`: 640×360. "FullEnrich - Explainer Video" / "Knowledge base to paper-craft explainer" / Tech. Paper-craft beige, black info pills.

Rule: the three caption styles above are CUSTOMER styles. They differ from each other, and none is a Poolday caption style.


### End cards

This is the only Poolday-authored end card observed (from the homepage "Meet Poolday" step video).

- `one-prompt-endcard.mp4`: 1920×1080, 30fps, 17.47s, silent. The end card runs ~10.5s→17.4s.
- `one-prompt-endcard-still.png`: frame at 16.3s (the hold).

What the frame shows:
- A flat `--brand-surface-bar` (#161616, pixel-sampled) ground. It is NOT pure black and has no halftone.
- A centred two-line stack. The top line, "One prompt to get all of your", is Inter-like regular in grey (~#bdbdbd→#808080). Under it, a cycling keyword in extra-bold lowercase near-white (translations → … → music → "anything").
- The keyword rolls in vertically with motion blur (slot-machine) and settles at ~15.5s.
- A 1–2px iris-gradient rule (blue→lilac→pink→peach→mint) sits under the word and grows to full frame width by ~15.9s.
- It holds ~1.1s. Then the text fades while the rule collapses to a centre dash. The last frame is dark.

What the frame does NOT have: no wordmark, logo, CTA or URL. Don't add a CTA pill or wordmark and call it "the Poolday end card". That would be an unverified extension.


    ## 8. Unverified (and why)
    
    - **Poolday caption style.** Only 3 of the 8 previews have captions, and they use three different customer styles. No Poolday caption spec exists.
    - **Branded end card** (wordmark/CTA/URL lockup). Not observed. The one Poolday end card has none, and the customer previews are 10s excerpts that cut mid-action.
    - **Lower-thirds.** One customer-styled example (Dust). There is no Poolday lower-third.
    - **Audio** (voice, music, SFX). Every fetched video is silent (the previews have no audio track), so this can't be verified.
    - **Halftone exact colours and falloff.** It is canvas-drawn, the JS bundle wasn't retrievable, and it doesn't paint in headless capture. Values come from pixel samples of a JPEG screenshot.
    - **Grain effect.** The file loads, but its visible effect isn't confirmed.
    - **Logo file / symbol.** None is published. The wordmark is live type, the favicon is an emoji, and the P tile appears only on the OG card.
    - **Company facts in §2** (funding, team size, founder history). Not re-checked against external sources.
    
    
## 9. Icons

Lucide (ISC), drawn with `currentColor`. **The live site uses `stroke-width="1.75"`**, so set that when you use the files below (they ship at 2).

**layout-grid.svg**

```svg
<svg
  class="lucide lucide-layout-grid"
  xmlns="http://www.w3.org/2000/svg"
  width="24"
  height="24"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <rect width="7" height="7" x="3" y="3" rx="1" />
  <rect width="7" height="7" x="14" y="3" rx="1" />
  <rect width="7" height="7" x="14" y="14" rx="1" />
  <rect width="7" height="7" x="3" y="14" rx="1" />
</svg>
```

**briefcase.svg**

```svg
<svg
  class="lucide lucide-briefcase"
  xmlns="http://www.w3.org/2000/svg"
  width="24"
  height="24"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
  <rect width="20" height="14" x="2" y="6" rx="2" />
</svg>
```

**gamepad-2.svg**

```svg
<svg
  class="lucide lucide-gamepad-2"
  xmlns="http://www.w3.org/2000/svg"
  width="24"
  height="24"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <line x1="6" x2="10" y1="11" y2="11" />
  <line x1="8" x2="8" y1="9" y2="13" />
  <line x1="15" x2="15.01" y1="12" y2="12" />
  <line x1="18" x2="18.01" y1="10" y2="10" />
  <path d="M17.32 5H6.68a4 4 0 0 0-3.978 3.59c-.006.052-.01.101-.017.152C2.604 9.416 2 14.456 2 16a3 3 0 0 0 3 3c1 0 1.5-.5 2-1l1.414-1.414A2 2 0 0 1 9.828 16h4.344a2 2 0 0 1 1.414.586L17 18c.5.5 1 1 2 1a3 3 0 0 0 3-3c0-1.545-.604-6.584-.685-7.258-.007-.05-.011-.1-.017-.151A4 4 0 0 0 17.32 5z" />
</svg>
```

**mic.svg**

```svg
<svg
  class="lucide lucide-mic"
  xmlns="http://www.w3.org/2000/svg"
  width="24"
  height="24"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="M12 19v3" />
  <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
  <rect x="9" y="2" width="6" height="13" rx="3" />
</svg>
```

**chevron-down.svg**

```svg
<svg
  class="lucide lucide-chevron-down"
  xmlns="http://www.w3.org/2000/svg"
  width="24"
  height="24"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="m6 9 6 6 6-6" />
</svg>
```

**volume-2.svg**

```svg
<svg
  class="lucide lucide-volume-2"
  xmlns="http://www.w3.org/2000/svg"
  width="24"
  height="24"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="M11 4.702a.705.705 0 0 0-1.203-.498L6.413 7.587A1.4 1.4 0 0 1 5.416 8H3a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2.416a1.4 1.4 0 0 1 .997.413l3.383 3.384A.705.705 0 0 0 11 19.298z" />
  <path d="M16 9a5 5 0 0 1 0 6" />
  <path d="M19.364 18.364a9 9 0 0 0 0-12.728" />
</svg>
```