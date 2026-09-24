# Poolday design system: "Horizon" (v1)

Built for the D5 lead-magnet mockups (`../D5-mockups/`). The same tokens will be reused when we rebuild Poolday's website pages.

**Idea:** a dark canvas lit by one source of light. The signature is the *horizon*: a planet-scale arc at the bottom of the page whose rim catches a cool cyan light, like the surface of a pool at dawn. Everything else stays quiet, so the product and the one action on each screen stand out.

## Files
- `tokens.css`: every token as a CSS custom property (`--pd-*`), plus the bundled `@font-face` rules.
- `fonts/`: Inter, Inter Tight, Geist Mono (variable woff2, SIL OFL). Bundled so pages render offline.
- Components as used: `../D5-mockups/src/app.css` (horizon, top bar, buttons, segmented tabs, chips, steps).

## Rules
1. **One light per screen.** `--pd-light*` (cyan) is for focus, progress, the selected card and the live state. Never for large fills or body text. The main CTA is white (`--pd-text-1` on dark), not cyan.
2. **Type does the work.** Display text uses Inter Tight 400–500 with tight tracking (−0.03 to −0.045em). Put the second half of a headline in `--pd-text-3` ("Paste a link. *Watch the video.*"). UI text is Inter 14–15px. Mono (Geist Mono, uppercase, +0.08em) is only for machine facts: timestamps, hex values, frame counters, agent status.
3. **Surfaces are light, not shadow.** Cards are `--pd-glass` with a `--pd-line-1/2` hairline and an inset top highlight (`--pd-edge`). Selected state adds a 4px outer halo and a soft cyan glow.
4. **Space:** 4px base; page gutter 40px on desktop and 16px on mobile. Keep one idea per screen with lots of empty canvas.
5. **Radii scale with size:** 6 (chips), 10–14 (buttons, inputs), 20–22 (cards, media), 24–28 (hero input, player). Pills are for tabs and buttons.
6. **Motion:** `--pd-ease-out` for entering and settling, `--pd-ease-in-out` for screen crossfades (700ms with a 6px blur and 2% scale). Ambient loops run at 6s. Honor `prefers-reduced-motion`.
7. **Customer brand colors live inside media only** (the video frames and brand-kit swatches). This keeps Poolday's UI neutral next to any brand.

## Not copied from anyone
Other AI-lab launch pages show the same general mood: dark canvas, restrained type, one glow. Nothing is taken from a specific brand: no asterisk or star marks, no orange, no purple-to-pink gradients. The wordmark glyph (a circle half filled with light) is a placeholder until Poolday's real logo is dropped in.

## Placeholders to replace before launch
- "1,284 videos made today" is an illustrative number. Wire it to a real count or remove it.
- The podcast style names (Hormozi, Diary of a CEO, Modern Wisdom, Ali Abdaal) name well-known looks. Get a legal check before shipping them, or rename them (e.g. "Bold caps", "Moody", "Highlight", "Friendly").
- Northwind, Lumen and "The Operator Hour" are fictional.
