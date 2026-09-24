# Website UI audit

Measured from a 2× screenshot of poolday.ai at a 1470px-wide viewport, plus the page source text of the homepage and pricing page. Values are CSS px. See the annotated image in the Reference assets.

## Stack signals

- Next.js on Vercel: videos are served from Vercel Blob storage (`*.public.blob.vercel-storage.com`), OG image from a dynamic `/api/og` route.
- `meta theme-color: #06b6d4` → Tailwind's cyan-500, which suggests Tailwind CSS. The sampled greys also sit on Tailwind's neutral scale (#f5f5f5 = neutral-100, #262626 = neutral-800 / white 15%).
- SEO keywords: AI video editor, autonomous video editing, video AI agents, AI video production, media superintelligence, generative video.

## Page anatomy (homepage, top to bottom)

1. **Nav** — wordmark left, five links centred (Home, Solutions ▾, Integrations, Pricing, Resources ▾), white pill CTA right.
2. **Hero** — halftone ellipse behind a centred two-line headline, one-line lede, one CTA.
3. **Proof grid** — two-tone title "100M+ video edits made by Poolday. Some examples here.", filter tabs (All / Tech Industry / Apps & Games / Podcasts), then 18 autoplaying customer videos, each with a title, a recipe caption and "Watch with sound".
4. **Meet Poolday** — four steps, each a sentence plus a 1080p product video (brand scan, clarifying questions, point-to-edit, one-prompt grid).
5. **Logo wall** — "Trusted by leaders worldwide in every category", marquee of 22 logos (duplicated for looping).
6. **Testimonials** — "From the teams running it", five quotes with photo, name, role and company logo, looping.
7. **Closing CTA** — "See Poolday in action, live on a call." + sub-copy + CTA + three price facts.
8. **Footer** — © line, Privacy Policy, Terms of Service.

## Measurements

| Element | Value |
|---|---|
| Page gutter | 48px left and right (container 1374px) |
| Nav height | 88px (24 + 40 + 24) |
| Wordmark | 24px, weight 400, cap height 17px, ~107px wide |
| Nav links | 15px, weight 400, #dddddd, 32px apart, chevron after dropdown items |
| Nav CTA | 190 × 40px, label 15px/500, 24px side padding, fill #f2f2f2, label #050505 |
| Nav → headline | 72px |
| Headline | 88px, weight 500, line-height 0.94 (line pitch 83px), tracking −0.03em, #f5f5f5, line 2 is 698px wide |
| Headline → lede | ~30px |
| Lede | 28px, weight 400, #f5f5f5, 868px wide on one line |
| Lede → CTA | ~43px |
| Hero CTA | 206 × 50px, label 15px/500, 32px side padding |
| CTA → section title | ~55px |
| Section title | 45px, weight 400, tracking −0.02em; #f5f5f5 then #878787 |
| Filter tabs | 38px tall pills, label 16px, 16px icon, 16px side padding, ~4px apart; active fill white 15% (#262626 on black), inactive text #939393 |
| Video grid | 5 columns of 267px, 10px gutters, lead tile spans 2 (544px), tiles radius 12px |
| Halftone | dots every 4px on rows every 8px; dot 1–2px wide, 1–3px tall; #101012 → #2d2d32; ellipse ~980 × 650px, centred slightly left of the page axis |

## Component inventory

| On site | In this system |
|---|---|
| Wordmark (live text) | `wordmark` style, inside `NavBar` |
| Nav with dropdown triggers | `NavBar` |
| Pill button, 2 sizes | `Button` (md 40px, lg 50px) |
| Filter tabs with icons | `FilterTabs` |
| Video tile with recipe caption | `VideoCard`, `VideoGrid` |
| Two-tone section title | `SectionTitle` |
| Halftone field | `Halftone` |
| Hero composition | `Hero` |
| Step block, logo marquee, testimonial card, pricing card | Documented here only: not visible in the captured screenshot, so their exact styling was not measured |

## What the UI does well

- **Radical restraint.** Two text colours, one button colour, zero borders. Nothing competes with the videos, which is the right call for a video product.
- **Proof above the fold's edge.** The first scroll lands directly on real customer output with named brands (PostHog, Lovable, ClickUp), not on feature icons.
- **Recipe captions.** "Founder photo + voice clone + brand kit" teaches the product's inputs while the video shows the output. It does the job of a features section without one.
- **A single CTA verb.** "Book a 15 min demo" appears four times and nowhere competes with it; the "15 min" lowers the commitment.
- **An ownable texture.** The scan-dot halftone is the only decorative element and reads as screen, signal and media at once.

## Friction and opportunities

- **Cyan is declared but unused.** The one brand hue only tints mobile browser chrome. Either commit to it as a signal colour (live, generating, focus) or drop it; right now the brand has no colour memory beyond black and white.
- **No symbol.** The wordmark is plain type, so avatars, favicons and video watermarks have nothing distinctive to carry. A mark built from the halftone dot would travel well.
- **"Superintelligence" is a big word with no definition on the page.** The lede defines the product, not the category claim. One line on why it is more than an editor would earn the headline.
- **Demo-only conversion.** With no trial, every visitor must commit to a call. A "watch a 2-minute build" video next to the CTA would serve people not ready to talk.
- **Logo wall mixes investors and customers.** Daphni and LocalGlobe (investors) sit beside Unity and Stillfront (customers) under "Trusted by leaders". Split or label them to protect credibility.
- **Dark-only and video-heavy.** 18 autoplaying videos plus four 1080p step videos make a heavy first load; poster frames and lazy loading matter for mobile.
- **Contrast is healthy.** Every sampled text pair passes WCAG AA on black (lowest: #878787 at 5.8:1).
