Poolday sells one idea: an AI agent that produces finished, on-brand video. The website says it with almost nothing: a black page, one white sentence, one white button, and a wall of real videos. Build anything for Poolday the same way. Let the work carry the colour; the brand itself is black, off-white and restraint.

## The five rules

1. **Black ground, always.** Every surface starts on `bg` (#000000). There is no light theme. Never place Poolday on white or a coloured field.
2. **One bright thing per view.** Text is `ink`; the only filled object is the `cta` pill. If two things compete for brightness, demote one to `ink-muted` or `ink-quiet`.
3. **The videos are the colour.** Brand colour lives in customer output (the red, the purple, the photography in the grid). UI chrome stays greyscale. `brand-cyan` appears at most once per asset, never as a background wash.
4. **Pills and 12px frames.** Controls are fully rounded (`radius-pill`). Media is framed at `radius-card`. Nothing else has a corner radius, and nothing has a shadow or border.
5. **Say it in one sentence, end with a period.** Headlines are declarative statements: "The Media Superintelligence." "Meet Poolday."

## Content fundamentals

The voice is confident, compressed and specific. It sounds like a founder who has shipped rather than a marketer who is promising.

- **Headlines** are short noun phrases or claims, sentence case, closed with a period: "The Media Superintelligence.", "Simple pricing", "See Poolday in action, live on a call."
- **The definition line** never changes: "An AI agent that edits, generates and assembles on-brand videos." Three verbs, one object, one qualifier.
- **Proof before adjectives.** Lead with numbers and names: "100M+ video edits made by Poolday.", "~$5–$25 per finished video", logos of Unity, Stillfront, Wildlife Studios.
- **Recipe captions** show the input, not the magic: "Made with brand kit + single prompt", "Founder photos + voice", "Screen recording to pixel-perfect video". Pattern: `<inputs> + <inputs>` or `<input> to <output>`.
- **CTAs** say exactly what happens: "Book a 15 min demo". There is one CTA verb on the whole site. Do not introduce "Get started", "Try free" or "Sign up" unless self-serve launches.
- **Person:** "it" for the agent ("It asks what it needs, then finishes the job"), implied "you" for the reader. No "we" in headlines.
- **Casing:** nav and tabs in Title Case ("Apps & Games"); everything else sentence case. Brand name: "Poolday" in prose, "Poolday.ai" only as the wordmark and domain.
- **No emoji, no exclamation marks** in brand copy (a customer quote may keep its own).

## Visual foundations

**Color.** Neutral-first. `bg` ground, `ink` text, `cta` fill with `on-cta` label. Secondary text steps down in lightness, not hue: `ink-nav` for navigation, `ink-muted` for inactive and meta text, `ink-quiet` for the muted tail of a two-tone title. `surface-glass` is the only fill besides the CTA: a 15% white used for the selected tab, translucent so the halftone shows through. `brand-cyan` is declared in the site's theme-color and nowhere else visible: treat it as a reserved signal colour.

**Type.** One family, `sans` (Inter). Big and tight at the top (`display-hero` 88px, 500, −0.03em, line-height 0.94), neutral at UI sizes (`nav`, `button`, `tab`). Section titles are regular weight (`section-title`), never bold. Centre-align hero and section titles; left-align paragraphs.

**The two-tone title.** A section title is two sentences: the claim in `ink`, then a softer follow-up in `ink-quiet` on the same line. Use the `SectionTitle` component. Do not use it for anything longer than two short sentences.

**The halftone field.** The signature graphic: a large ellipse of scan-line dots behind the hero. Dots every 4px (`space-1`) on rows every 8px (`space-2`); each dot's height swells from 1px at the edge to 3px at the centre while its colour moves from `halftone-dot-dim` to `halftone-dot`. It is a texture, never an illustration: keep it below 20% perceived brightness and always behind type. Use the `Halftone` component rather than an image.

**Layout.** Content is centred with `space-12` gutters. The hero stack runs: nav (`nav-height`), `space-18`, headline, `space-8`, lede, `space-10`, CTA, `space-14`, section title. Video proof sits in a 5-column grid (`grid-columns`) with `gap-grid` gutters; the lead video spans two columns.

**Imagery.** Real customer videos, autoplaying and muted, framed at `radius-card`, edge to edge within their tile. No stock photography, no abstract AI imagery, no people-in-offices. If there is no video, show the halftone, not a placeholder illustration.

**Motion.** Videos autoplay. Button and tab states change colour only (about 150ms ease). The halftone may drift slowly; respect `prefers-reduced-motion` and stop it.

**States.** Hover lifts the `cta` to `cta-hover`; nav links go from `ink-nav` to `ink`; an inactive tab gains `ink`. Focus is a 2px solid `focus` ring at 3px offset (an intentional addition: the live site's focus style was not captured).

**Borders, shadows, gradients.** None. Separation comes from the black ground and spacing.

## Iconography

Line icons, 2px stroke, round caps and joins, 24px grid drawn at 16px (`icon`), coloured by the text they sit beside (`ink` when active, `ink-muted` when not). The tab icons match Lucide exactly (layout-grid, briefcase, gamepad-2, mic) and the nav dropdown uses chevron-down; the files in the Icons group are Lucide 1.48 (ISC). Treat Lucide as the icon system and keep to it. No emoji, no filled or duotone icons.

## Logo

The logo is the wordmark "Poolday.ai" set in live type: `wordmark` style, `ink` on `bg`. There is no symbol or monogram on the site, so none is included here. Keep at least `space-6` clear space, never recolour it except to `on-cta` on a light fill, never outline, stretch or add effects.

## Using the components

`window.Poolday` holds `Button`, `NavBar`, `FilterTabs`, `VideoCard`, `VideoGrid`, `SectionTitle`, `Halftone`, `Hero`, `Icon` (React 18). Load `tokens.css` and `components/bundle.css` first; the stylesheet pulls Inter from Google Fonts.

## Files in this kit

- `README.md` — these rules. Read first.
- `tokens.json` — every token with value and usage note (source of truth). `tokens.css` — the same as CSS custom properties plus one class per type style.
- `brand/01-foundations.md` — company, positioning, audiences, messaging pillars, copy bank.
- `brand/02-website-ui-audit.md` — page anatomy, every measurement, strengths and fixes.
- `brand/03-applications.md` — specs for OG images, social, Stories, video end cards, slides.
- `components/` — `bundle.js` (React 18 UMD, exposes `window.Poolday`), `bundle.css`, `index.d.ts` (props), and per component a `README.md` (guidelines) and `preview.html` (usage example).
- `assets/Icons/` — Lucide SVGs used on the site. `assets/Reference/` — the measured homepage screenshot and its annotated version.
- `demo.html` — open in a browser to see every component live.
