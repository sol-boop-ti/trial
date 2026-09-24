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
