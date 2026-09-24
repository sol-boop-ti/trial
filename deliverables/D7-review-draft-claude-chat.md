# D7 draft from Claude chat (pricing addendum + copy), with our critique

Source: the user's Claude chat session (it browsed poolday.ai). The draft text is kept by the user; this file records the critique and what we keep.

## Verdict
- **The pricing-page part is the most impactful work so far.** Pricing is the highest-intent page, and these points directly move demo bookings:
  - translating credits into videos ("≈ 50–250 finished videos/month"),
  - turning "$600 first month" into a named, explained pilot,
  - a persona line per plan,
  - honest top-up wording instead of "2× rate",
  - a comparison against agency / freelancer / in-house editor,
  - a security & procurement strip, and an FAQ.
- **The copy table is about 50% good.** Keep the lines that tie tiny input to a finished output ("Merge a PR. Get a launch video.", "Paste the JD. Get the recruiting video.", "Bring your website. Watch Poolday make your video, live."). Drop the rest.

## Fix before using
1. **Never change a factual claim while rewriting.** "95% autonomy after 2 weeks" ≠ "95% need zero edits". Keep Poolday's own wording for numbers.
2. **The "X in. Y out." rhythm used 8+ times becomes a tic** and reads generic. Use it 2–3 times, max.
3. **"Human-grade. Agent-made." drops the proof.** A slogan never replaces evidence.
4. **Verify "~$5–$25 per finished video" is really on the home page** before building the pricing math on it. If it is, it's the strongest line on the site.
5. **"A third-party analysis couldn't find security documentation": cite it or drop it.**
6. **Missing:** the core review of the home and b2b-startups pages (above-the-fold 5-second test, CTA friction, proof placement). Bring back the main part of the chat answer, not only the addenda.
7. **Every recommendation needs an A/B test and a metric** (demo bookings), ranked by impact × effort.

## Next step: make it visual
Rebuild improved versions of the home, b2b-startups and pricing pages as real HTML in the same dark, minimal "superintelligence" design system (`deliverables/design/`), then render before/after screenshots side by side. This needs the current pages: either poolday.ai allowed in the environment's network settings (Claude Code then screenshots them itself), or the user saves each page (Save page as → complete) plus full-page screenshots.
