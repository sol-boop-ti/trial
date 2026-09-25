# D7. Page review: home, /solutions/b2b-startups, /pricing (goal: more demos booked)

**Round 4.** Each BEFORE is now the **live page itself**: screenshots the user captured (`real/`). Each AFTER is rebuilt on the live structure and changes only the numbered items. Everything without a number is the live page, kept.

Visuals:
- `compare/<page>-compare.png` (full page) and `compare/<page>-compare-fold.png` (first screen).
- `video/`: MP4s of the animated sections.

Callouts follow page order. Rows are ranked by impact on demos booked × effort. **Primary metric for every test:** completed demo bookings per unique visitor. Each row names a guardrail.

## Verified by the live screenshots

- **"~$5–$25 per finished video"**, **"Month-to-month, no lock-in"** and **"First month $600"** all appear on the home CTA card. The [verify] tag is dropped.
- **Enterprise credits = plan price.** The card reads "Includes $2,500/mo in credits".
- **Yearly plans exist.** The pricing sub reads "Month-to-month plans, or yearly plans for discounts."
- **"95% of your videos need zero edits from your team"** is Poolday's own copy on the B2B page ("95% autonomy after 2 weeks … Two weeks in, 95% of your videos need zero edits"). Our earlier critique called that wording a changed claim. It isn't: both phrasings are Poolday's.
- **The home logo wall mixes investors and customers.** LocalGlobe and daphni sit in the same marquee as Unity, Stillfront and WeWard.
- **The live site uses more than one CTA label.** Pricing says "Book a call to get your agent configured" and B2B adds a second button, "View examples". Both are kept on pricing; "View examples" is replaced on B2B (see below).

## Pricing

The page stays as simple as the live one: H1, sub, a light Business card and a dark Enterprise card, with their real items and CTAs.

| # | Problem → change (exact copy) | Why it books more demos | A/B test (guardrail) |
|---|---|---|---|
| 1 | "Includes $1,250/mo in credits" doesn't say what that buys. → A framed credits box inside each card, Submagic-style: **"$1,250 in credits · ≈ 50–250 finished videos"** / **"$2,500 in credits · ≈ 100–500 finished videos"**. It replaces the credits bullet. | It answers "how much video do I get?" at the price, so the buyer books to set up rather than to ask. The range is derived from the verified ~$5–$25 per video. | Box vs the bullet. Guardrail: share of sales calls where scope is disputed. |
| 2 | "Your first month at $600" doesn't name the risk. → **"Your first month at $600 · no lock-in"** | It moves the verified "no lock-in" from the home page to the point where the price is read. | Copy swap. Guardrail: pilot → paid at day 45. |
| 3 | No proof on the page. → Real customer logos under the plans (CREDITS.md). | Proof sits where the decision is made. | On vs off. Guardrail: plan-card CTA clicks. |
| 4 | $1,250 gets compared with a SaaS seat. → **"Poolday vs the usual options. Priced per finished video."** Three rows against agency / freelancer / in-house editor. | It moves the anchor to production spend. | Table vs none. Guardrail: plan-card CTA clicks. The competitor cells stay qualitative. |
| 5 | Questions become emails, not bookings. → Four FAQs: credit, the $600 month, running out, yearly plan. Every answer uses live facts only. | It removes the last objection before the call. | On vs off. Guardrail: booking completion. |

Dropped: the one-line procurement note, because the live Enterprise card already lists "SSO, MSA & redlines", a private Slack channel and invoicing.

## Home

| # | Problem → change (exact copy) | Why it books more demos | A/B test (guardrail) |
|---|---|---|---|
| 1 | Demo is the only path, and visitors not ready to call leave. → **"Watch a 2-min build"** next to the hero CTA, and again in the CTA card. | It keeps the visitors who aren't ready, and the video pre-sells the call. | Link on vs off. Guardrail: hero CTA clicks must not fall more than 10%. |
| 2 | The masonry feed (mixed heights, one huge yellow tile) reads as busy. → **Four use-case rows** (Launch films · Product demos & explainers · Ads & testimonials · Podcasts), four uniform 16:10 tiles each, with the live caption bar (brand – title, recipe, tag). Titles come from the live grid; the groupings are ours. | A visitor finds "their" use case in one glance, and that is what makes the call feel relevant. | Grouped vs masonry. Guardrails: plays with sound; LCP. |
| 3 | "Meet Poolday." has no definition, so "Superintelligence" is never explained. → **"Meet Poolday. An agent that plans, makes and fixes the whole video."** (second sentence in quiet grey). The four live features are recreated with their device frames, live copy and animated media (`video/home-meet-poolday.mp4`). | It earns the headline and frames Poolday as more than an editor. | Copy swap. Guardrail: scroll depth. |
| 4 | There is no CTA between the proof and the end of the page. → **"Book a 15 min demo"** directly under the four features. | It asks right after the product is understood. | On vs off. Guardrail: CTA-card clicks (cannibalisation). |
| 5 | Investors sit in the "Trusted by leaders" marquee. → Customers only, then **"Backed by LocalGlobe, daphni"**. | It protects credibility with careful buyers. | Ship without a test (low risk). |
| 6 | The CTA card says "walkthrough" but not what the visitor gets. → Three steps inside the live grey card: **"Minute 1: You share your website." · "Minutes 2–10: It builds your brand kit live and drafts a first video." [verify] · "Minutes 10–15: You leave with a plan for your first month."** | It lowers the fear of a sales call. | On vs off. Guardrail: demo no-show rate. Ship only if sales can do the live build. |
| — | 18 autoplaying videos plus the feature GIFs are heavy. → Poster frames; lazy-load below the first row. | Faster mobile pages mean more visitors reach the CTA. | Measure LCP; test bookings on mobile. |

Other ways to organise the feed (not built):
- **Rows that scroll sideways**, one per use case.
- **Rows ordered by the visitor's segment** (referrer, UTM or last tab clicked).
- **A single 30-second hero reel** cut from the best eight customer videos, with the grid below. It is the simplest first screen, but it gives up proof density.

## /solutions/b2b-startups

| # | Problem → change (exact copy) | Why it books more demos | A/B test (guardrail) |
|---|---|---|---|
| 1 | The H1 "On-brand videos of any kind" names the product, not the startup's job. → **"Every feature you ship, on video."** The live subhead stays. | It passes the 5-second test for a startup that ships weekly. | H1 swap. Guardrail: bounce rate. |
| 2 | "View examples" only scrolls the page. → **"Paste your URL"**: a free launch video made from your site, sent by email (D5), with a small tilted off-white **"NEW"** sticker. | It gives value before the call. A lead who has seen their own brand in a Poolday video books far more often. | Field vs "View examples", qualified domains only. Primary: bookings within 14 days. Guardrails: credit cost per booked demo (~$380 est., D5); hero CTA clicks. |
| 3 | No logos in the first screen. → Real logos: PostHog, Lovable, ClickUp, Dust, Marblism (type fallback), FullEnrich, monochrome at one optical size. | Peer proof before the scroll. | On vs off. Guardrail: none needed. Confirm logo permissions first. |
| 4 | The 9 use cases are text-only cards. → Each card gets a small animated preview in a device frame: the input builds (call waveform, merged PR, changelog, CRM list, transcript, help article, JD…), then an arrow, then the output video plays. The live titles and body copy are kept word for word (`video/b2b-use-cases.mp4`, `video/b2b-after-scroll.mp4`). | Seeing input become output makes each use case concrete ("we already have that"), the way Meet Poolday does on home. | Animated vs text cards. Guardrails: LCP; section scroll-through. |

Dropped since round 3, because the live page already has them: named proof videos ("Made in Poolday"), the "95%" and onboarding facts ("Why tech startups love Poolday"), and a rewritten closing line.

## What I kept

- **The restraint.** Black ground, off-white pills, the halftone, and the light-grey CTA card as the one bright block.
- **Caption bars with recipes** ("Made with brand kit + single prompt"). They teach the inputs while the video shows the output.
- **B2B "Tech startups use Poolday for".** Named customer videos with "See the prompt" is already strong proof: it shows the output and the prompt behind it.
- **"Why tech startups love Poolday".** It already answers quality, fit, team and time ("Ranked #1 worldwide in agentic video editing", "150+ connectors", "95% of your videos need zero edits").
- **"Book a 15 min demo"** as the main verb. The pricing CTA "Book a call to get your agent configured" is kept, because it describes the same call.

## Still unverified [verify]

- Whether the demo call includes a live brand-kit build (home callout 6).
- That each customer allows its logo on the page.
- The Marblism logo file (type fallback for now).
- Render time and cost of the free URL video (D5 pilot).
