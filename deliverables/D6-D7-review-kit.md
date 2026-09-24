# D6 + D7 Review Kit: paste-ready prompts for Claude chat

Claude Code can't reach poolday.ai from its session, so you run both reviews in **Claude chat on claude.ai**, which can browse. This file has:

1. [How to run it](#1-how-to-run-it-checklist): a short checklist
2. [Prompt A](#2-prompt-a--page-reviews-d7): page reviews (poolday.ai + /solutions/b2b-startups), goal = more demos booked
3. [Prompt B](#3-prompt-b--video-review-d6): video review (PostHog GenAI launch **or** Upflow faster payments)

Both prompts tell the assistant to **review only what it can actually see** and to say when it can't see something, so nothing in the review is made up.

---

## 1. How to run it (checklist)

**Before you start (about 15 min, this is RUNBOOK step C2)**
- [ ] Full-page screenshots of `https://poolday.ai` and `https://poolday.ai/solutions/b2b-startups`, **desktop and mobile** (Chrome DevTools → Cmd+Shift+P → "Capture full size screenshot"; turn on device mode for mobile).
- [ ] Copy each page's visible text into a `.txt` file. A backup in case the chat's fetch misses JS-rendered content.
- [ ] Optional, for the speed section: run PageSpeed Insights (`pagespeed.web.dev`) on both URLs, mobile and desktop, and screenshot the scores plus the LCP/CLS/INP numbers.
- [ ] Optional: click the demo CTA on each page and screenshot every step up to the booking confirmation (form fields, calendar, redirects). Stop before you actually book.
- [ ] Pick the video: **PostHog GenAI launch** (`https://poolday.ai/#watch/posthog-genai-launch`) or **Upflow** (`https://poolday.ai/solutions/b2b-startups#watch/upflow-faster-payments`). Watch both once and review the one with more to fix.
- [ ] For that video: **screen-record it** (QuickTime / OBS, with sound) and also take **frame screenshots with the timestamp in the file name** (`0m03s.png`) at every cut or text change, plus one every 2s during the first 6s. Note the total length.

**Page reviews (D7)**
- [ ] New Claude chat, with web search/fetch turned on.
- [ ] Paste **Prompt A**. Attach the screenshots and text files in the same message.
- [ ] If it says it couldn't fetch a page or that the content looks empty (JS-rendered), reply "use the attached screenshots and text as the source of truth".
- [ ] Check every "problem" it lists against the screenshot. Delete anything it can't point to on the page.
- [ ] Ask a follow-up if needed: "Make the top 3 mockups more concrete: exact copy and position of each element."

**Video review (D6)**
- [ ] New Claude chat. Paste **Prompt B**, attach the frames (in time order) and the screen recording if the chat accepts video.
- [ ] Check its timestamps against the video. Fix any that are off.
- [ ] Optional proof: paste the Poolday follow-up prompt it writes into a new **Poolday** conversation (Align mode, Standard or Max tier) with the original video attached, and put the before/after in the deliverable.

**After**
- [ ] Save both outputs as `deliverables/D7-page-reviews.md` and `deliverables/D6-video-review.md` (or send them to Claude Code to format).
- [ ] Report to Claude Code: `done D6/D7 — video: <PostHog|Upflow>, took X min, fetch worked: yes/no, Poolday intro remake: yes/no ($__)`. It gets logged in METHODS.md.

---

## 2. Prompt A: page reviews (D7)

Paste everything inside the block.

````
You are a senior B2B SaaS conversion (CRO) strategist. I'm doing a growth
assignment for Poolday, an AI video production agent (you brief it like a
creative team: it builds brand kits from a website, then produces videos,
ads, UGC and launch films). The goal of this review is ONE metric:
MORE DEMOS BOOKED.

Pages to review:
1. https://poolday.ai (home)
2. https://poolday.ai/solutions/b2b-startups (segment page for B2B startups)

STEP 1: GET THE PAGES
- Fetch both URLs. For each, list what you actually retrieved: headline,
  subhead, every CTA (exact label + position on the page), section order,
  social proof elements, video/demo embeds, forms.
- I've also attached full-page screenshots (desktop + mobile) and the
  visible text of each page. If the fetch is incomplete (e.g. JS-rendered
  content missing), treat the attachments as the source of truth.
- Hard rule: only critique what you can see in the fetch or attachments.
  If something can't be verified (e.g. what happens after the CTA click,
  real load time, video content you can't play), say "not verifiable from
  what I have" and tell me what to capture. Don't guess.

STEP 2: EVALUATE EACH PAGE WITH THIS FRAMEWORK
For each criterion, give a verdict (strong / OK / weak) and the evidence
(quote the copy or name the element and its position).
1. 5-second test, above the fold: in 5 seconds, can a visitor tell
   (a) WHAT it is, (b) WHO it's for, (c) WHY NOW / why switch,
   (d) the NEXT STEP? Name the missing ones.
2. Value proposition clarity: is the outcome concrete (time, cost,
   quality, volume) or generic ("AI-powered", "create stunning videos")?
   Is it clear how it differs from an agency, a freelancer and other AI
   video tools?
3. ICP / segment fit (b2b-startups page only): does it speak to a B2B
   startup's real jobs (launch videos, product demos, funding
   announcements, paid social, sales outreach, a marketing team of 1–3)?
   Does it use their words? Is it actually different from the home page,
   or a re-skin?
4. Social proof: placement (above/below the fold, next to CTAs?),
   specificity (named people + titles + companies, or anonymous?),
   logos (recognisable to a B2B startup buyer?), metrics (numbers with
   context, e.g. "launch video in 2 days vs 3 weeks"), case studies.
5. The demo CTA: how many demo CTAs, where, labels, and whether they
   compete with other CTAs (sign up / try free / watch). Friction: calendar
   embed vs form, number and type of fields, redirects, qualification
   questions. If you can't see the booking flow, say so.
6. Objection handling: is each one answered on the page, and where?
   - Price ("is this cheaper than an agency / freelancer?")
   - Quality ("will it look like AI slop?")
   - Time ("how long until I have a video? how much of MY time?")
   - Brand fit ("will it match our brand / use our real product UI?")
   Also: security/data, rights to the output, who does the work.
7. "Instant value" entry points: can a visitor get value BEFORE booking
   (interactive demo, sample gallery by use case, "paste your URL → get a
   video/brand kit" lead magnet, template library, ROI calculator)?
   Context: my growth idea is "Enter your URL, watch your launch video",
   a URL-to-video lead magnet that emails the video and routes to a demo.
   Assess where such an entry point could live on these pages and how it
   would hand off to the demo CTA.
8. Video/demo content on the page: which videos are shown, where, do
   they autoplay, are they understandable with sound off, do they prove
   the product (the process and output) or only show output? Is there a
   short "how it works" video next to the demo CTA?
9. Page speed / mobile: if you have PageSpeed numbers (attached),
   interpret them (LCP, CLS, INP, weight of video embeds). On the mobile
   screenshots: is the CTA visible without scrolling, is the text legible,
   is there a sticky CTA, do the video embeds fit?
10. Analytics & experimentation: which events should be tracked to
   measure the demo funnel (CTA view → click → form start → booking →
   show-up), and which tools/setups you'd recommend. Only state what's
   currently installed if you can see it in the page source.

STEP 3: OUTPUT (in this order)
A. One-paragraph verdict per page: the single biggest reason it loses
   demo bookings today.
B. Prioritized change list (both pages, 10–15 items), as a table sorted
   by ICE score (Impact × Confidence × Ease, each 1–10). Columns:
   # | Page | Problem (with evidence) | The change | Why it increases
   demo bookings (the mechanism) | How to A/B test it (variant, primary
   metric, guardrail metric, rough sample size/duration at B2B traffic
   levels) | I | C | E | ICE
C. Top 3 changes as annotated mockup descriptions. For each: a BEFORE
   (current copy/layout, quoted) and AFTER (exact new copy, element order,
   position, what the visitor sees above the fold on desktop and on
   mobile), with numbered annotations explaining each change.
D. Rewritten hero section, 2 variants PER PAGE (4 total). Each: headline
   (≤10 words), subhead (≤25 words), primary CTA label, secondary CTA
   label, one line of proof under the CTA, and the hypothesis it tests
   (e.g. outcome-led vs speed-led vs proof-led).
E. Quick wins I could ship this week vs bigger bets.
F. Open questions: things you'd need data for (traffic, current
   conversion rate, booking show-up rate) before trusting the ICE scores.

Style: direct, specific, no generic CRO advice. Every recommendation must
point to a specific element on these pages.
````

---

## 3. Prompt B: video review (D6)

Fill in the two `<…>` lines, then paste everything inside the block. Attach the frames (and the screen recording if the chat accepts video).

````
You are a senior motion designer and performance-creative lead. Review
a Poolday showcase video and tell me exactly how to improve it. Poolday
is an AI video production agent. This video lives on Poolday's own site
as proof of what it can make, so it has two jobs: (1) work as a B2B
launch video for the featured company, and (2) make a Poolday visitor
think "I want that for my company" → book a demo.

Video: <PostHog GenAI launch: https://poolday.ai/#watch/posthog-genai-launch
       OR Upflow faster payments: https://poolday.ai/solutions/b2b-startups#watch/upflow-faster-payments>
Total length: <m:ss>. Platform(s) it would realistically run on:
<e.g. LinkedIn feed, X, website hero, sales email>.

IMPORTANT: you probably can't play video from a link. I've attached
frames with the timestamp in each file name (in time order), plus a
screen recording if possible. Base the review ONLY on what's in the
attachments. If you need a frame you don't have, list the timestamps
you need and I'll send them. Don't describe anything you can't see; for
audio (music, SFX, VO), rely only on what I describe below.
Audio notes from me: <e.g. "music starts at 0:00, drop at 0:07, no VO",
or "no audio notes">.

FRAMEWORK (evaluate each, citing timestamps):
1. Hook 0–3s: what's on screen at 0:00, 0:01, 0:02? Would it stop a
   scroll with the sound off? First-frame thumbnail strength.
2. The question the opening sets up: what does the viewer want to know
   after 3s? Is it answered, and when?
3. Value prop clarity: when (timestamp) does a first-time viewer
   understand what the product does and why it matters?
4. Story arc: map the beats (hook → problem/tension → reveal → proof →
   payoff/CTA). Where does it sag or repeat?
5. Pacing / cut rhythm: average shot length per section, where it
   drags, where it's too fast to read. Holds on key frames.
6. Text legibility on mobile: text size relative to frame height, on
   screen long enough to read (rule of thumb: ~3 words/sec + 0.5s),
   contrast, safe zones for 4:5 / 9:16 crops.
7. Sound-off viewing: does the story survive muted (captions, on-screen
   type carrying the message)?
8. Music/SFX sync: do cuts and motion accents hit the beat, are there
   sync points on the key reveals? (Only from my audio notes.)
9. Brand/product proof: is the real product UI shown, long enough and
   large enough to be believable? Logo placement and timing.
10. CTA: is there one, is it specific, how long is it on screen?
11. Length vs platform: is the length right for where it will run? What
   would the 15s and 6s cutdowns keep?

OUTPUT:
A. Timestamped notes, as a table: Timestamp | What happens | Issue or
   strength | Fix. Write every fix as a MECHANISM, never an adjective:
   cuts (hard cut / match cut / whip), holds (hold N frames / N s),
   easing (ease-out on entry, no linear moves), scale/position (type at
   X% of frame height), sync points (cut on the kick at 0:0X), timing
   (move beat B before beat A). Never write "make it punchier" or
   "more dynamic".
B. Top 3 changes, ranked by impact on (1) watch-through and (2) "I want
   this" intent. For each: what, where (timestamps), why (the mechanism).
C. A rewrite of the first 5 seconds as a shot list: time range | visual |
   on-screen text (exact words) | motion/transition | audio/sync point.
   Designed to be understood muted on a phone.
D. Optional Poolday follow-up prompt, which I'll paste into Poolday (an
   AI video agent: it can pull the original video from its link or an
   upload and re-edit it) to produce the improved intro as proof. Write
   it at INTENT level, not as an editing script: context (which video,
   attached), objective (a new first 5s that does X for audience Y),
   hard constraints (length, ratio, keep brand assets, muted-legible
   text), what to keep from the original, a validation step ("show me 3
   hook options as stills before rendering"), and where it has creative
   freedom. Under 120 words. Poolday decides the edit itself.

Style: specific, timestamped, no generic video advice.
````

---

## Notes for the deliverable (D6/D7 sections)

- **Method line:** "poolday.ai was unreachable from my build environment, so I ran the reviews in Claude chat with a fixed framework and my own screenshots and screen recordings as the source of truth. Every claim is tied to a visible element or a timestamp."
- **Link to the growth idea:** criterion 7 in Prompt A sets up D5 ("URL → launch video"). Use its placement recommendation in the D5 section.
- **Proof:** if the Poolday intro remake from Prompt B, part D, is run, show before/after side by side. It turns the review into a demonstration.
