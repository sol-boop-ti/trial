# D6: Video review (PostHog GenAI launch + Upflow faster payments)

Method: both videos analysed frame by frame (ffmpeg: a contact sheet at 1 frame/s, scene-cut detection, key frames at full size), then combined with the user's own viewing notes. Timestamps are approximate (±0.5s). Source files: `references/review-posthog.mp4` (24.4s) and `references/review-upflow.mp4` (23.3s).

---

## The editor's take (first watch, before any frame analysis)

**Upflow: great ideas, lost rhythm.**
- Most scenes run **1–2 seconds too long**, so the rhythm dies. Simply watching it at **1.5× speed** already makes it better (tested: `upflow-1.5x-quicktest.mp4`).
- Root cause: the agent doesn't know what a great SaaS-UI video *feels* like. Give it **more examples of the best videos in this style**, as references and as a saved pacing skill, so fast becomes the default.

**PostHog: beautiful, but not PostHog.**
- The visuals are great, but **not on brand**. PostHog is a **2D** brand (flat illustration, hand-drawn hedgehogs), so a 2D video would fit it far better than 3D clay renders.
- The **footer at the end looks like PowerPoint**, the typical "AI made this" slide: a static logo plus a web footer. It should be an animated sign-off.

**Is brand extraction the problem?** Poolday does have brand-kit extraction, and it's an important part of the job. It captured PostHog's logo, colours and fonts, but not its visual medium (2D illustration). Feeding the kit the brand's real illustration assets, plus a rule like "2D only", fixes that.

The frame-by-frame analysis below confirms each point with timestamps.

---

## 1. Upflow: "faster payments" (23.3s, 16:9)

**What works:** the idea is strong. It opens on one question typed into search ("Did Acme pay invoice #2041 yet?"), then it multiplies into dozens of questions in 5 languages. That captures the real chaos of accounts receivable in one image. The brand is tight: Upflow blue, the right font, a restrained palette.

**What breaks it:** the rhythm, plus the story never pays off.

| Time | What happens | Problem | Fix (mechanism) |
|---|---|---|---|
| 0:00–0:04 | A blank screen, a cursor, the question typed letter by letter | 4s on one sentence, and the first 1s is an empty frame: a weak hook | Start with the question already half typed. Type at ~25 characters/s (the full line in ~1.2s), cut on the "?" |
| 0:04–0:10 | The questions multiply across languages | A good beat, but it holds ~2s after the point has landed | Cut at 0:07. Speed up the swarm so it gets denser. Scale it up until it fills the frame, then hard cut |
| 0:10–0:13 | "something" / "simple" on blue, then on white | Two word cards take ~3s to say "something simple"; the white "simple" card repeats for 2s | One card, "Something simple.", 0.8s, synced to a beat |
| 0:13–0:15 | Outline of a laptop, then a dot on the screen | **The product never appears.** The setup ("did Acme pay?") is never answered | **The payoff:** the laptop fills with the real Upflow UI answering the question: invoice #2041 → "Paid · 3 days early", the status chip turning green. This is the missing beat |
| 0:15–0:19 | "upflow" typed on navy | 4s to type a 6-letter wordmark | Reveal the logo in ≤0.8s, or skip the typing and snap it in on the beat |
| 0:19–0:23 | End card: logo + "faster payments. stronger relationships." + proof line | The proof ("WorkMotion cut invoices 31+ days overdue by 79%") is micro-text at the bottom: unreadable on mobile, and it's the best line in the video | Make the 79% the hero of its own 1.2s card before the logo, as a big number with "WorkMotion" under it |

**The quick test:** `upflow-1.5x-quicktest.mp4` (in this folder) is the original sped up 1.5× (15.5s). It already feels much better, which confirms that holds, not ideas, are the main problem. But speeding up everything uniformly also rushes the swarm and the end card. The right fix is per-shot timing, as in the table above.

**Top 3 changes:**
1. **Show the product answering the question.** It's the payoff the whole setup promises.
2. **Cut every hold to reading time + ~0.3s.** Target length ~14–16s.
3. **Make the proof number a full card,** not a footer line.

---

## 2. PostHog: GenAI launch (24.4s, 16:9)

**What works:** high production value, and a clear arc: waiting for the launch → "Ship it" → "It's live" → too many tools → answers in one place → the product. The balloon-letter "many" with sticky notes ("so many logins / which dashboard? / another tool??") is funny and readable.

**What breaks it:**

| Time | What happens | Problem | Fix (mechanism) |
|---|---|---|---|
| Whole film | Soft 3D clay renders, a warm beige studio, a 3D hedgehog | **Off-brand.** PostHog's identity is 2D: flat hand-drawn hedgehog illustrations, bold flat colour, a playful, dense, slightly retro, "OS window" website. The 3D look reads as a generic AI render, not PostHog | Rebuild in 2D: flat PostHog-style illustrations, their hedgehog art, flat colour blocks, and their UI windows as the stage |
| 0:02–0:03 | Close-up of a laptop, then a white flash | The blurred text "where is the launch?" and the white frame at ~0:03 are dead air | Cut the flash and hard cut on the notification |
| 0:08 | "WAIT IS OVER / IT'S LIVE" in a letterbox | It's the climax, but it's the smallest text in the film and it's gone in <1s | Give "It's live" a full-frame kinetic moment (0.8–1s) |
| 0:17–0:19 | UI tabs: "Product Analytics / Session Replay / Feature Flags", "Go beyond dashboards." | The only product moment is ~2s of tiny, low-contrast UI | Show the real PostHog UI at full frame: one insight chart drawing itself, one session replay |
| 0:19–0:21 | "start!!!!", then "Building Real…" | Unclear copy: "start!!!!" and a half-seen "Building Real" don't read as a message | One clear line, e.g. the launch's actual claim, held for reading time |
| 0:21–0:24 | End card: a static logo, then a grey footer with 6 icons, "available now", a URL, 3 lines of description, a pill with 6 product names, "Get started – free" | **It looks like a slide.** It's static for ~3.5s, has 4 levels of text hierarchy, and the body copy is unreadable at video size. This is the "PowerPoint / looks like Claude made it" feeling: a web page footer pasted into a film | A 1.5s animated end card: logo + one line + URL, entering on the last beat. Drop the icon row, the paragraph and the pill |

**Top 3 changes:**
1. **Match the brand's medium:** 2D, PostHog's own illustration style and hedgehogs, not 3D renders.
2. **Replace the slide-style end card** with a short animated sign-off (logo + one line + URL).
3. **Real product proof** at full frame, instead of 2s of tiny tabs.

---

## 3. What both videos teach us about the agent (the root cause)

1. **Pacing defaults are too slow for SaaS UI.** Fix it once with a Poolday **skill** (the guide: "skills are knowledge you teach the agent about your preferences"):
   > *SaaS UI pacing: hook 1.5–2.5s; average shot ≤1.2s (fast montage 0.4–0.8s); a text card holds for reading time (~0.25s/word) + 0.3s; typing ~1.5 frames per glyph; the logo lockup 2–3s in total, including a ≥0.6s hold once landed, and alive (slow push/drift), never a static slide; cut on the beat; nothing fully still during holds. Always pay off the opening question with the real product UI.*

   These numbers are aligned with `poolday/motion-design-for-agents.md` (the user's motion-design manual, distilled from analysing many great motion pieces), which should be given to Poolday as a skill too.

   Attach 3–5 reference SaaS launch videos with great pacing to the skill. That's the user's idea, and it fits the guide's "drop in inspiration, name what you like about each reference".
2. **The brand kit captured the identity (logo, colours, font) but not the brand's visual *medium*.** PostHog = 2D illustration.
   - **Does Poolday have brand extraction?** Yes. The guide documents "web research & brand-asset extraction from any site" and "Create a brand kit for [brand]" from a website, guidelines or Figma. The ref-teaser skill also calls a `brand-kit-authoring` flow.
   - **The fix:** feed the kit the brand's **illustration style and mascot assets** (the "asset library" and "Video DNA" layers), not just the website. Add a usage law: *"PostHog videos are 2D, flat, illustrated. No 3D renders."*
   - PostHog publishes its brand assets and hedgehog art publicly [verify the URL]; those go into the kit as real files.
3. **End cards need a rule too:** a sign-off is motion, not a web footer.

## 4. The extra step: remake them in Poolday
Show, don't only tell: remake the first ~8s of each with the fixes (Align mode, the video attached as the reference):
```
Attached: the original Upflow video. Remake it as a ~15s cut with these changes:
the question types in ~1.2s; cut the swarm at 0:07; one "Something simple." card;
then the laptop fills with the Upflow UI answering it (invoice #2041 → Paid,
status chip turns green); then the "79%" proof as its own card; the logo in ≤0.8s.
Keep the brand exactly as is. Show me 3 options for the UI payoff shot first.
```
```
Attached: the original PostHog GenAI launch video. Remake the same story in 2D,
in PostHog's own illustrated style (flat colour, their hedgehog art, UI windows
as the stage). No 3D renders. Replace the end card with a 1.5s animated sign-off:
logo + one line + posthog.com. First show me 3 style frames for approval.
```
Then put before/after side by side in the deliverable.
