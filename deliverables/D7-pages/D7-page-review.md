# D7. Page review: home, /solutions/b2b-startups, /pricing (goal: more demos booked)

poolday.ai was blocked from the build environment, so each BEFORE is a **reconstruction** from the brand kit's audit, the page text and the reported copy. It is not a capture. Grey bars stand for copy we didn't capture, and tile titles are illustrative. Every AFTER keeps Poolday's facts word for word. A **[verify]** tag marks anything we couldn't confirm.

Visuals: `compare/<page>-compare.png` (full page) and `compare/<page>-compare-fold.png` (first screen). Numbered callouts on the AFTER match the # column below (callouts follow page order; table rows are by impact on demos booked × effort). **Primary metric for every test: demo bookings per unique visitor** (completed calendar bookings, not clicks).

## Pricing (highest intent)

Principle (after user review): keep the original's simplicity. The first screen is still H1 + two plan cards side by side; every addition is one line. Heavier material sits below the fold.

| # | Problem → change (exact copy) | Why it books more demos | A/B test (guardrail) |
|---|---|---|---|
| 2 | "$1,250 of credits" means nothing to a buyer. → One line under each price: **"≈ 50–250 finished videos a month"** / **"≈ 100–500+ finished videos a month"** [verify]. | Answers "how much video do I get?" before the call, so the buyer arrives ready to book, not ready to email. | Line on vs off. Guardrail: share of sales calls where scope is disputed. Range = $1,250 ÷ ~$5–$25 per video [verify the figure and that Enterprise credits equal the price]. |
| 4 | "Your first month at $600" is small print. → Same spot, one line: **"First month $600 · a pilot, no lock-in"**. | Names the low-risk first step without adding a block; the call becomes "set up my pilot". | Copy swap. Guardrail: pilot → paid conversion at day 45. |
| 1 | The H1 has nothing under it. → **"Simple pricing."** + one line **"Pay for finished videos, not seats. ~$5–$25 per finished video."** [verify] | Sets the unit (per video) before the $1,250 anchor, so the price reads cheap per output. | Lede vs none. Guardrail: bounce rate on /pricing. |
| 3 | Both plans read alike. → Small caption under the plan name: **"For a startup team of 1–3 that ships every week."** / **"For teams that need SSO, an MSA and API access."** | Visitors pick themselves into a plan instead of stalling on the choice. | On vs off. Guardrail: Enterprise share of bookings. |
| 5 | No proof on the page. → **"Teams on Poolday"** logo row under the plans. | Proof where the decision is made. | On vs off. Guardrail: CTA click → booking completion. |
| 6 | $1,250 gets compared with a $30 SaaS seat. → Below the fold: **"Poolday vs the usual options. Priced per finished video."** Three rows only (how you pay, commitment, your brand) against agency / freelancer / in-house editor. | Moves the anchor to production spend, where $1,250 a month is small. | Table vs none. Guardrail: plan-card CTA clicks. Competitor cells stay qualitative; add costs only if sourced. |
| 7, 8 | Nothing for procurement or pre-call questions. → One line: **"Ready for procurement on Enterprise: SSO · MSA · private Slack · API access · unlimited users. Security documentation on request"** [verify], then a four-question FAQ (credit, the $600 month, running out, needing a designer). | Unblocks larger accounts and answers the questions that otherwise become an email instead of a booking. | Test as one "below-fold pack". Guardrail: booking completion. |

Dropped after review: the big pilot band (it made the page feel less simple and pushed the prices down) and the long top-up paragraph (the card keeps Poolday's original "Extra credits at 2× the included rate"; the honest wording lives in the FAQ).

## Home

The hero stays as clean as the original: after user review, the price facts under the hero CTA were removed (noise). They stay in the closing section, where the original has them.

| # | Problem → change (exact copy) | Why it books more demos | A/B test (guardrail) |
|---|---|---|---|
| 1 | Demo is the only path, and visitors not ready to call just leave. → Secondary text link **"Watch a 2-min build"** next to the CTA and again at the close. It plays a real run, ending on "Book a 15 min demo". | It keeps the not-ready visitors, and the video pre-sells the call. | Link on vs off. Guardrail: hero CTA click rate must not fall more than 10%. Watch it: of the ideas here, this one is the most likely to eat into CTA clicks. |
| 2 | No CTA between the 18 videos and the page's end, which is where interest peaks. → After the grid: **"Your brand, in videos like these. It learns your brand once."** + **Book a 15 min demo**. | It asks at the moment of peak interest. | On vs off. Guardrail: scroll depth to Meet Poolday. |
| 5 | "See Poolday in action, live on a call." doesn't say what happens on the call. → Three cards: **Minute 1: "You share your website." · Minutes 2–10: "It builds your brand kit live and drafts a first video." [verify] · Minutes 10–15: "You leave with a plan and your $600 first month."** | It lowers the fear of a sales call. The visitor knows they will leave with something. | On vs off. Guardrail: demo no-show rate. Only ship this if sales can deliver the live build. |
| 3 | "Superintelligence" is never defined. → **"Meet Poolday. Not a tool you operate: an agent that plans, makes and fixes the whole video."** | It earns the headline and sets Poolday apart from editors (Descript, Kapwing), which justifies a call over a free trial. | Copy swap. Guardrail: time on page. |
| 4 | Investors sit among customers under "Trusted by leaders". → Customer logos only, then a quiet line: **"Backed by Daphni, LocalGlobe"**. | It protects credibility with sharp buyers, even if the booking effect is small. | Ship it without a test (low risk). Track bookings before and after. |
| — | 18 autoplaying videos plus four 1080p videos make a heavy load. → Poster frames, lazy-load everything below the first row. | Faster mobile loads mean more visitors reach the CTA. | Measure LCP; test bookings on mobile only. |

## /solutions/b2b-startups

| # | Problem → change (exact copy) | Why it books more demos | A/B test (guardrail) |
|---|---|---|---|
| 1 | The H1 "On-brand videos of any kind" says what the product is, not who it's for. → **"Every feature you ship, on video."** Poolday's own subhead stays below it. | It passes the 5-second test for a B2B startup: it is for us, and it matches our weekly release rhythm. | H1 swap. Guardrail: bounce rate. |
| 2 | Same all-or-nothing demo gate as home. → Secondary field **"Paste your URL"** + **"Not ready for a call? Paste your site and get a free launch video made from it, by email."** (the D5 growth idea), tagged with a tiny brand-cyan pill **"Free · limited"**, the only accent on the page (the kit reserves cyan as a signal colour). The video ends with the booking offer. | Visitors get value before any call. A lead who has seen their own brand in a Poolday video books at a far higher rate. | Field on vs off, qualified domains only. Primary: bookings within 14 days. Guardrails: credit cost per booked demo (D5 estimate ~$380 [est.]), and hero CTA clicks. |
| 4 | The nine use cases are listed as bare names. → Section title **"Merge a PR. Get a launch video. Eight more videos your team never has time to make."**, with the launch video tile first and large. Each tile keeps its name and gains a recipe chip, e.g. **"Changelog to monthly recap"**, **"CRM list to one demo per account"**, **"Job description to recruiting video"**. | Tying input to output makes the effort look tiny ("I already have that"), and the most frequent startup job leads. | Recipe chips + order vs original. Guardrail: clicks into each use case. |
| 3, 5 | "Indistinguishable from human-made" is a claim with nothing under it, and the page shows no B2B proof. → Logos in the first screen (PostHog, Lovable, ClickUp, Dust, Marblism, FullEnrich). The claim becomes **"Indistinguishable from human-made. Judge for yourself: videos made for startups like yours."** over five named customer videos. | Proof from peers, placed where the claim is made. | Test as one proof pack. Guardrail: page load time. [verify the customer videos can be shown on this page] |
| 6 | "White-glove onboarding" and "95% autonomy after 2 weeks" are headings with body text under them. → Three stat cards: **1-1** onboarding · **95%** autonomy after 2 weeks (Poolday's wording kept) · **$600** your first month. | It turns the time objection ("how much of MY time?") into facts. | On vs off. Guardrail: scroll depth. |
| 7 | The final CTA doesn't say what happens. → **"Bring your website. Watch Poolday make your video, live."** [verify] + price microline. | The call itself becomes the instant value. | Copy swap. Guardrail: no-show rate. |

"X in. Y out." style lines are used twice in total (the b2b section title and the closing line).

## What I kept

- **The restraint.** Black ground, one off-white pill, no borders, shadows or gradients, the halftone behind the hero. Every change reuses the kit's own parts: SectionTitle, the pill, the glass tab fill, 12px frames.
- **"Book a 15 min demo" as the only CTA verb.** It stays on every page. The only secondary actions are "Watch a 2-min build" (home, pricing) and "Paste your URL" (b2b), one per page.
- **Recipe captions.** They are the site's best idea, and b2b now uses them on every use case.
- **The facts, word for word:** "The Media Superintelligence.", the definition line, "100M+ video edits made by Poolday.", "95% autonomy after 2 weeks", all prices.

## Unverified [verify]

~$5–$25 per finished video (on the live home page?) · the videos-per-month ranges built on it · Enterprise credits = price · credits included in the $600 month · whether the demo includes a live brand-kit build · security documentation · rights to the output · whether the customer videos can be shown on b2b · every BEFORE layout detail (reconstruction). Screenshot the three live pages to close these before any test.
