# Credits

## Live-page screenshots (BEFOREs)

`real/poolday-home-fullpage-live.webp`, `real/poolday-b2b-startups-fullpage-live.webp` and `real/poolday-pricing-live.webp` were captured by the user from poolday.ai on 2026-09-24/25. The other two files, `real/poolday-home-meet-*.webp`, were used as reference for the Meet Poolday animations, and `real/submagic-pricing.webp` was used as inspiration for the credits box. `render.js` crops the screenshots into `renders/*-before-live*.png`.

## Customer logos (b2b-after callout 3, pricing-after callout 3, home logo wall)

These are Poolday's tech customers as named in the brand kit (`brand/01-foundations.md`). Files are in `src/logos/`. `src/build.js` inlines each one and recolours it to `currentColor` (#d4d4d4 on black), so every logo renders in one tone. Optical size: marks at 22px and wordmarks at 20–21px, with text at 23px.

The company websites and cdn.jsdelivr.net are blocked from this environment (the proxy returns 403). The npm registry is reachable, so every file below comes from a published npm package.

| Company | What is used | Source | License / provenance |
|---|---|---|---|
| PostHog | Official mark (`posthog.svg`) + the name set in Inter 700 | npm `simple-icons@16.32.0`, `icons/posthog.svg` | CC0-1.0 (simple-icons). Brand guidelines of the owner apply. The wordmark is approximated in Inter because simple-icons ships marks only. |
| ClickUp | Official mark (`clickup.svg`) + the name set in Inter 700 | npm `simple-icons@16.32.0`, `icons/clickup.svg` | CC0-1.0 (simple-icons). The wordmark is approximated in Inter. |
| Lovable | Heart mark + official wordmark (`lovable-mark.svg`, `lovable-wordmark.svg`) | npm `@lobehub/icons-static-svg@1.95.1`, `icons/lovable.svg` and `icons/lovable-text.svg` | MIT (LobeHub, github.com/lobehub/lobe-icons). Third-party redraw of the brand mark. |
| Dust | Official wordmark logo, mono white (`dust.svg`) | npm `@dust-tt/sparkle@0.7.7`, `src/logo/src/dust/Dust_Logo_MonoWhite.svg` | ISC. Published by Dust (Permutation Labs SAS) in its own design system, so it is first-party. |
| FullEnrich | Official icon (`fullenrich.svg`) + the name set in Inter 600 | npm `n8n-nodes-fullenrich@0.2.2`, `dist/nodes/fe-logo-light.svg` | MIT. Published by FullEnrich (author @fullenrich.com, github.com/FullEnrich), so it is first-party. The wordmark is approximated in Inter. |
| Unity (home logo wall) | Official mark + the name set in Inter | npm `simple-icons@16.32.0`, `icons/unity.svg` | CC0-1.0. The other names on the home wall (Wildlife, Stillfront, adikteev, WeWard, VERAXEN, LocalGlobe, daphni) are typed stand-ins, not logo files. |
| Marblism | **Fallback:** the name "Marblism" set in Inter 600, tracking −0.03em | none found (not in simple-icons, lobehub or any npm package we found) | No logo file. Replace it with the official SVG from Marblism's press kit before publishing. |

All logos are trademarks of their owners and are used here only to mock up a customer logo wall. Before this goes live, Poolday should confirm each customer allows its logo on the page.

The Meet Poolday "brand" animation redraws the live GIF's OpenAI card as a typed stand-in (a ◎ glyph plus the word "OpenAI"), not the OpenAI logo.
