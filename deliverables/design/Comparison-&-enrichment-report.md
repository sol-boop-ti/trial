# Poolday brand kit: comparison and enrichment report (2026-09-24)

**First, the kit you selected didn't exist.** There was no `/storage/org/brand-kits/poolday/` folder (the only kit in this org is `flam`). So your kit (asset:40b1ad0c-9c0f-4f5a-98a1-ec90a0eb0bf4 + screenshot asset:32f4cebf-c4f1-4e2d-a0b8-d3356d388a6a) was compared against the **live poolday.ai site**: its authored CSS/HTML (via `browser dump`), its own font files, pixel samples and its own videos. The in-product design language `/library/system/design/DESIGN.md` served as a secondary baseline. Then a new, verified kit was built at that path.

- Kit package: `/storage/org/brand-kits/poolday/` (specVersion 3), applied with `brand:poolday`
- Single-file export (your format, enriched): `/documents/poolday-brand-kit-enriched.md`
- Research ledger: `/storage/org/brand-kit-research/poolday/` (SOURCES.md, decisions.md, extraction/)

The three rules are kept verbatim: **black ground · one bright element per view · the videos carry the colour.**

## (a) Differences: your kit vs the live site

| Claim in your kit | Live site value | Verdict |
|---|---|---|
| Font Inter | Inter, self-hosted via next/font (variable 100–900). The `font-serif` class is mapped to Inter too | ✅ Confirmed (file now pinned) |
| Single family | A **second family, Fraunces**, is loaded and used for testimonial quotes. JetBrains Mono is preloaded but unused | ❌ Differs |
| Headline 88px / **500** / lh 0.94 / −0.03em | 88px / **400** (`font-normal`) / lh **0.95** / **−0.025em** | ❌ Differs |
| Section title 45px, −0.02em | **46px**, lh 1.08, −0.025em | ⚠️ Close |
| Lede 28/400 | 28px / 400 / lh 1.3 | ✅ |
| Wordmark live type, 24/400, no symbol | Live text "Poolday.ai", `text-2xl`, no logo file. The OG card alone uses a blue "P" tile; the favicon is an island emoji | ✅ Mostly (P tile and favicon added as notes) |
| bg #000 | Page wrapper `bg-black` #000, body underlay `charcoal` #08090A | ✅ (+ underlay) |
| ink #f5f5f5 | `--foreground: #f5f5f5` | ✅ |
| CTA #f2f2f2 / on-cta #050505 | `--cream #f2f2f2` / `--cream-foreground #050505` | ✅ |
| CTA hover → #fff | `hover:opacity-90` | ❌ Differs |
| Nav #dddddd, 15px | foreground/90 (#ddd on black) ✅; size is **16px** (`text-base`) | ⚠️ Size differs |
| Inactive tab #939393 | foreground/60 = #939393 on black | ✅ (it's an alpha) |
| Tab fill white 15% | `bg-white/15`; hover white/10; tabs are **15px/500** (not 16/400) | ⚠️ Label differs |
| Section-title tail #878787 | foreground/55 = #878787 on black | ✅ |
| theme-color #06b6d4 | #06b6d4 (both schemes), browser chrome only | ✅ |
| Focus ring = cyan (your addition) | The site defines `--ring: #2389E2`, used at 60% | ❌ Differs |
| Halftone #101012 → #2d2d32, 4px dots / 8px rows | 4px / 8px pitch confirmed from pixels. The brightest dots sample **#2A–#2E neutral** (not cool). It's drawn on a `<canvas>` with no image | ⚠️ Colour differs, pitch ✅ |
| Radius 12 on media | Cards **16px** (`rounded-2xl`), inner step-video frames 12px, closing panel 24px | ❌ Differs |
| 5 columns, 10px gap | 5 columns (lg), **12px gap** (`gap-3`), lead tile 2×2, 56px caption bar #161616 | ⚠️ Gap differs |
| "No borders, no shadows, no gradients" | Hairlines white/10 everywhere, card shadow `0 10px 30px rgba(0,0,0,.45)` + inset vignette, glass white/5 + blur, bottom fade masks | ❌ Differs |
| "Never on a light field" | The closing CTA is a **light panel** (#EEE at 85%, 24px radius) with a dark pill | ❌ Differs |
| Video tile overlay "inferred" | Real: hover scrim black/70 + 2px blur with the recipe caption + "▶ Watch with sound", and a caption bar with icon chip, title 13px/500, recipe 11.5px at 55% | ➕ Now verified |
| Lucide icons, 2px stroke | Lucide, but **stroke 1.75** | ⚠️ Differs |
| Videos on Vercel Blob | `ex0wdeclshou5was.public.blob.vercel-storage.com` | ✅ |
| Grain | Not in your kit. The site authors a `/v2/grain.jpg` overlay (10%, screen, 320px); the file loads, but no visible lift shows in pixel samples | ➕ New (off by default) |
| Undeclared tokens | `--brand #305880`, `--panel #eee`, `--secondary` indigo-500 are declared but unused on the homepage | ➕ New |
| Pricing "First month $600" | The homepage says $600, but /pricing says "**Your first month at $500**" | ⚠️ The site contradicts itself |
| Video end card recipe (wordmark + CTA + domain) | The only Poolday end card seen is a #161616 kinetic tagline ("One prompt to get all of your / anything") with an iris-gradient rule, and **no wordmark, CTA or URL** | ❌ The recipe is not brand fact |

**Library design language (`/library/system/design/DESIGN.md`).** This is the in-product Studio language (Geist, the iris palette), not the marketing brand. One overlap: the end-card rule gradient matches the iris gradient (blue → lilac → pink → peach → mint). It conflicts with the marketing site on the typeface (Geist vs Inter) and the ground (hsl 240 10% 3.9% vs #000).

## (b) Added (paths relative to `/storage/org/brand-kits/poolday/`)

| Path | What it is | assetId |
|---|---|---|
| `DESIGN.md` | Front-matter tokens: 25 colours, 12 type roles, spacing, radii, components, motion, audio, spatial. Rules, Unverified list | n/a |
| `styles.css` | `--brand-*` vars, type classes, surfaces, `.brand-btn*`, `.brand-tab*`, `.brand-video-card*`, `.brand-grain`, `.brand-halftone` | n/a |
| `components/Button.tsx`, `SectionTitle.tsx`, `VideoCard.tsx`, `Halftone.tsx` | The signature four. Styled only by the sheet; the halftone is procedural and the video is injected. Test-rendered cleanly | n/a |
| `fonts/inter.json` | Inter variable, the site's own file | asset:523c0306-df75-4ff2-a353-722ac1b0eb65 |
| `fonts/fraunces.json` | Fraunces variable (quotes only) | asset:9facf9b9-7388-4cd1-9b90-014d6a886b88 |
| `references/logos/wordmark-rendered.png` | "Poolday.ai" re-rendered from the site's Inter file (no logo file exists) | asset:fcdfcadc-b62f-4efc-9e22-1ec909bc431d |
| `references/logos/favicon.ico` | Live favicon (island emoji, tab-only) | asset:417d7740-5896-4b1c-8657-7f4e6ca3452e |
| `references/logos/og-p-tile.png` | Blue "P" tile cropped from the OG card (48px) | asset:36da74e3-f35c-490f-b4fd-fc8e9ae974e5 |
| `references/social/og-card.png` | Live og:image (/api/og, 1200×630) | asset:e8e824e9-8346-4183-b205-87febe1eee1e |
| `references/textures/grain.jpg` | Live grain tile | asset:454f70bf-88da-4f21-a312-ce6be300f06e |
| `references/end-cards/one-prompt-endcard.mp4` | Poolday step video with its end card | asset:3244c494-a748-45bc-acf2-7a06d80ec50a |
| `references/end-cards/one-prompt-endcard-still.png` | End-card frame at 16.3s | asset:f6bd71c3-2bea-4e31-83b9-ab95b053f0b7 |
| `references/video-examples/marblism-launch-film.mp4` | Marblism – Product Launch Video (lead tile) | asset:5de03ff1-5a0a-467a-8b2b-cde6349b9aa1 |
| `references/video-examples/posthog-genai-launch.mp4` | PostHog – AI Feature Launch | asset:c05fd86d-21db-4bcb-8c1f-822d4f010cef |
| `references/video-examples/lovable-ig-pitch.mp4` | Lovable – Instagram Ad (9:16, captions) | asset:225af9b5-bd7b-4091-a36a-3fcf44a83155 |
| `references/video-examples/clickup-ai.mp4` | ClickUp – Product Feature Video | asset:94eac023-3cc2-4635-aa82-13f9770b95f3 |
| `references/video-examples/dust-agent-demo.mp4` | Dust – Agent demo (lower-third) | asset:d651981f-02dd-43e7-a044-a81390e3e2e9 |
| `references/video-examples/smart-reframe.mp4` | Smart Reframe Highlights (Podcasts) | asset:fe05cd10-c211-4e94-a58a-71eca42daa69 |
| `references/video-examples/podcast-social-clips.mp4` | Podcast to 8 Social Clips (karaoke captions) | asset:0dd72351-54fa-485d-ad2f-27aa884b2205 |
| `references/video-examples/fullenrich-explainer.mp4` | FullEnrich – Explainer | asset:789d542b-d9e6-49e4-947d-a0f8f33a6659 |
| `references/*/INDEX.md` (5) | One line per asset, plus usage rules | n/a |

Each video's title and recipe caption were recorded verbatim. The full 18-video grid inventory is in the ledger (`extraction/video-grid-inventory.tsv`).

## (c) Could not verify, and why

- **A Poolday caption style.** Only 3 of the 8 previews have captions, and each uses a different customer style (Lovable: uppercase bold white; Podcast: extra-bold lowercase with the active word in yellow; Smart Reframe: bold white). None of them is a Poolday house style.
- **A branded end card** (wordmark, CTA or URL). The customer previews are 10s excerpts that cut off mid-action. The single Poolday end card carries no wordmark, CTA or URL, so I didn't create one.
- **Lower-thirds.** Only one example (Dust), and it's in the customer's styling.
- **Audio** (voice, music, SFX). None of the 9 videos has an audio track, so the audio tokens are marked `unverified`.
- **Halftone code.** The halftone is drawn on a canvas, and its JS bundle couldn't be fetched (non-media JS is blocked), and it doesn't paint in headless capture. The colours and falloff come from pixel samples of a JPEG, so they are approximate.
- **Grain effect.** The file loads (HTTP 200), but open areas still sample as #000. The overlay's visible effect is unconfirmed.
- **Official logo files, a symbol, and an SVG wordmark.** The site doesn't publish any. The raster wordmark is a faithful re-render, not an official Poolday file.
- **The "Apps & Games" vertical.** None of the homepage grid videos is tagged with it, so there is no example for that vertical.
- **Rejected legacy asset.** `/og.png` is an older, light-cream, monospace "Request access" site capture (asset:643b84a2-af04-43de-82ae-ee8d7b2860b3), so it wasn't pinned.
- **Company facts** in your Foundations section (funding, team, founder history). Not re-checked; I carried them over labelled "unaudited".
