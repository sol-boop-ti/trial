# Applying the brand

Specs for assets beyond the website, derived from the tokens. The site does not show these formats; they are the system applied consistently.

## Proportional type scale

Scale the website sizes to any canvas by width: headline ≈ 6% of canvas width, section title ≈ 3%, lede ≈ 1.9%, caption ≈ 0.9%, all with the site's tracking. Keep `display-hero` weight 500 and everything else 400.

| Format | Canvas | Margin | Headline | Support line | Wordmark |
|---|---|---|---|---|---|
| OG / link preview | 1200 × 630 | 64px | 72px | 24px | 24px, top-left |
| LinkedIn / X post | 1200 × 1200 | 80px | 88px | 28px | 28px, top-left |
| Instagram portrait | 1080 × 1350 | 72px | 84px | 30px | 28px, top-left |
| Story / Reel / TikTok | 1080 × 1920 | 72px sides, 240px top/bottom safe zones | 96px | 34px | 32px, top centre |
| Video end card 16:9 | 1920 × 1080 | 120px | 120px | 38px | 36px, centred above |
| Slide 16:9 | 1920 × 1080 | 120px | 96px | 32px | 24px, bottom-left |

## Layout recipes

**Announcement (funding, launch).** `bg` ground, halftone ellipse centred at 60% height, headline centred in `ink` ending with a period, one support line, wordmark top-left. Example headline: "Poolday raised $11M." Support: "To build the Media Superintelligence."

**Customer proof.** The customer's video frame fills the canvas edge to edge at `radius-card` scaled up (12px at 1080 wide → 2.4% of the short side), with a recipe caption in a `surface-glass` pill bottom-left: "Screen recording to pixel-perfect video". Customer logo top-right in white.

**Stat card.** One number in `display-hero` ("100M+"), one line in `ink-quiet` underneath, nothing else.

**Video end card.** 1.5s hold: wordmark, the definition line in `lede`, then a `cta` pill "Book a 15 min demo" and the domain poolday.ai in `ink-muted` caption.

**Slides.** Black background, one statement per slide as a two-tone `section-title`, product video or customer video as the only image, page number and wordmark in `ink-muted` at 16px.

## Do

- Keep the black; let customer video provide colour.
- Use real product captures and customer output only.
- Put one pill CTA per asset, off-white `cta`.
- End every headline with a period.

## Don't

- Place the wordmark on white or on a photograph without a black field.
- Use gradients, glows, glassmorphism beyond the tab pill, or neon.
- Use brand-cyan as a background, in more than one element, or for text below 16px on grey.
- Show AI-generic imagery (brains, robots, sparkles) or stock photos.
- Stack more than two lines of headline.
