# Brand kits used for the two remakes

## PostHog: from PostHog's own public sources
**Sources:** the `PostHog/posthog.com` repo (handbook → brand: `visual-identity.md`, `assets.md`) and the `PostHog/brand` package (the official logo geometry, the color tokens, the RoundHog font files and 171 hedgehog SVGs). Both were cloned on 2026-09-26.

| | Value |
|---|---|
| Background | `#EEEFE9` (light mode, the default). Solid, never a gradient |
| Text | `#151515` at 90% opacity |
| Accent / window chrome | `#E5E7E0`, divider `#D0D1C9` (dashed) |
| Brand colors | Red `#F54E00` (also links; never used for errors), Yellow `#F1A82C` / `#DC9300`, Blue `#1D4AFF`, Gray `#BFBFBC` |
| Primary font | **RoundHog**: Bold for titles, Semibold for large paragraphs, Regular for body. Sentence case |
| Display font | **Squeak** Bold, always uppercase, only next to hedgehog art |
| Logo | The 2026 lockup: gradient spikes, no gap between the body parts. Never recolor it, never spin, bounce or glitch it |
| Logo motion | The app's own **logomark jump**: easing `cubic-bezier(.6,0,.2,.8)`, the head jumps first, then the spikes, with a stagger of airtime/15 |
| Illustration | Max the hedgehog and friends: hand-drawn, thick outlines, flat color. **No AI-generated hogs, no 3D, no blobs** |
| Motion rules | Understated; puppet-rigged characters; shadows move with the character; animate in, then ease out to a still final frame |
| UI | "PostHog OS": windows with a title bar and – □ × controls |
| Screenshots | Real product UI with synthetic data that tells a story (the handbook's own example is a user clicking "Upgrade" 47 times) |

**Rights:** the PostHog brand assets are under the PolyForm Strict license, and the hedgehogs can't be used in marketing without PostHog's permission. This remake is a **private spec piece** for the Poolday application. The asset files stay outside the repo (`remake/src/_assets`, git-ignored; `fetch-assets.sh` rebuilds them). Don't publish the video without PostHog's OK.

## Upflow: from the original video (upflow.io is blocked from this environment)
**Sources:** frames of Upflow's own video (Poolday built it from Upflow's brand kit) and a web search. The site and its `/brand` page couldn't be reached from here.

| | Value |
|---|---|
| Brand blue | `#3936DC` (sampled) |
| Navy | `#191A4C` (sampled) |
| Paper | `#FAFAF7` (sampled) |
| Wordmark | "upflow." in lowercase with a round period. **Vectorized** from the 1080p end card (potrace, 6× supersampled), with the period kept as a separate path so it can land on its own |
| Type | A geometric grotesk. The closest free match is **Figtree** (compared against 13 Google fonts on the tagline) |
| Voice | Lowercase and calm: "faster payments. stronger relationships." |
| Proof point | "WorkMotion cut invoices 31+ days overdue by 79%" (from Upflow's own video) |
| Product | Accounts receivable: customers, invoices, automated reminder workflows, a payment portal, reconciliation. The UI in the remake is a **plausible reconstruction** with brand-consistent styling, not a capture of the real app. Swap in real screenshots before any public use |
