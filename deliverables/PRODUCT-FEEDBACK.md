# Product feedback on Poolday (from using it during the assignment)

## Bug: the "Upload your assets" modal clips its content
- **Where:** Assets → My Assets → Upload.
- **What:** the modal's drop zone and the accepted-file-types text are cut off on the right edge. The dashed border and the end of each format line (".otio, …", "…) f") are clipped. It looks like the text container is wider than the modal, with overflow hidden.
- **Screenshot:** `assets/poolday-feedback/ui-bug-upload-modal.webp`.
- **Severity:** cosmetic, but it's the first thing a new user sees when uploading brand assets. Likely fix: `max-width: 100%` plus wrapping on the formats line, or a shorter "Video, audio, image, text, font, 3D · max 1 GB" summary with a "see all formats" tooltip.

## What felt great
- The UI and UX feel premium and consistent with the "superintelligence" positioning.
- Align mode's structured questions: options as cards, an "Awaiting your input" state, "Let agent decide", free text. It feels like briefing a creative director.
- Asking the agent "do you have an API?" produced a precise, honest answer: public API, keys/docs/playground/webhooks under Capabilities → Integrations, a lighter Automation + inbound-webhook option, and "I won't guess the paths". Screenshots: `assets/poolday-feedback/api-answer.webp`, `api-question.webp`.

## Friction: the agent offers "Create an API key", but the feature is locked
- **Where:** in chat, the agent answered "Yes, your code can start a production…" with a **Create an API key** button pointing to Capabilities → Integrations. That page says **"Integrations Not Enabled. API integrations are not enabled for this organization. Contact your administrator."**
- **Screenshot:** `assets/poolday-feedback/integrations-not-enabled.webp`.
- **Suggestion:** the agent should know the org's entitlements. It should say "API access is available on your plan once enabled; here's how to request it", with a one-click "Request access" instead of a dead end. For a trial or enterprise evaluation, API access is exactly what a technical buyer wants to test.

## Pacing: videos are too slow for social (high impact)
It shows in all three videos I looked at: the PostHog and Upflow reviews, and a post picked at random from the CEO's LinkedIn ("Businesses have no excuse left for not making…", linkedin.com/posts/alexeichemenda_…). **The scenes are too slow, and the first 3 seconds are wasted.** In the LinkedIn one, the first 3s are just a blur clearing. People decide to scroll in about 3 seconds.
- **The fix, as a default:**
  - something meaningful on screen in frame 1: the product, a claim, a face, or a number;
  - no blur-in or fade-in openers;
  - average shot ≤1.2s;
  - text holds for reading time + 0.3s;
  - the hook is fully stated by 2s.
- **How to ship it:** a built-in "social pacing" preset/skill that is on by default for social formats. My D6 remakes show the difference side by side: Upflow reaches the product at 4s instead of never, and the original still hasn't shown it at 8.5s.

