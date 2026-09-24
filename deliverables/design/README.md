# Design system: Poolday's brand kit

**The design system is now Poolday's own kit: [`poolday-brand-kit/`](poolday-brand-kit/README.md).** It was built from the live poolday.ai site (tokens, components, rules, copy bank, reference screenshots). Read its README before building anything.

The invented v1 system ("Horizon": the horizon arc, cyan accent, Inter Tight + Geist Mono, circle logo, `tokens.css`, `brand/`) is **retired and deleted**. Nothing references it any more.

## What lives here

| Path | What |
|---|---|
| `poolday-brand-kit/` | Source of truth. `tokens.css` / `tokens.json`, `components/` (bundle.css, Halftone, Button, FilterTabs, VideoCard...), `brand/` (foundations, UI audit, applications), `assets/Reference/`. |
| `fonts/inter-latin-wght-normal.woff2` | Inter (SIL OFL), bundled because the kit loads Inter from Google Fonts and our render environment is offline. Declared with `@font-face { font-family: "Inter" }` next to the kit's tokens. |

## How the D5 mockups use it (`../D5-mockups/src/app.css`)

- `@import` of `poolday-brand-kit/tokens.css`; only kit tokens (`--bg`, `--ink`, `--ink-nav`, `--ink-muted`, `--ink-quiet`, `--cta`, `--cta-hover`, `--on-cta`, `--surface-glass`, `--surface-raised`, `--halftone-dot*`, `--brand-cyan`, spacing, `--radius-card`, `--radius-pill`, control heights).
- Pure black ground; ink type; the "Poolday.ai" live-type wordmark in Inter; one off-white `cta` pill per view; `surface-glass` for the selected tab and chips; 12px frames for media, pills for controls; no borders, shadows or gradients in the chrome; Lucide 2px icons; two-tone titles (ink + ink-quiet) ending with a period; `brand-cyan` at most once per view (the active step dot while generating).
- The halftone scan-dot ellipse (logic ported from the kit's `Halftone` component) is the only texture. It moves between screens, drifts slowly, runs inside the "Poolday AI does it for you" pill as a shimmer, and ripples once when that pill or "Book a 15 min demo" is pressed.
- Colour lives only inside media: the style previews, the video frames, the fictional Northwind SaaS inside the recorder.
- Copy follows the kit's voice: confident, compressed, no exclamation marks or emoji, recipe captions (`<input> + <input>`, `<input> to <output>`), and one CTA verb: "Book a 15 min demo".

## Open points (not in the kit)

- The kit has no progress bar, drop zone or choice screen; these were derived from its rules (thin ink line, `surface-raised` 12px frame, one cta pill).
- "1,284 videos made here today" on step 1 is an **illustrative number**. Wire it to a real count or remove it.
- The podcast style names (Hormozi, Diary of a CEO, MrBeast, Ali Abdaal, Iman Gadzhi) name well-known looks; get a legal check before shipping them publicly.
- Northwind, Lumen and "The Operator Hour" are fictional.
