# D3: the agent loop, run live (26 Sep 2026)

**The CEO's brief:** find new leads → qualify → build the videos with Poolday → human validation → draft the email he sends.

| Step | What happened | Screenshot |
|---|---|---|
| Find | 37 Series B companies ingested from the dataset (fresh rounds, named buyers) | `screenshots/03-dashboard-leads.jpg` |
| Qualify | 5 qualified (Flam 99, TwelveLabs 83, Blacksmith 79, Wispr Flow 73, Convex 73), 32 disqualified with reasons. Each lead gets a video angle and a buyer | `03` |
| Build with Poolday | The pipeline POSTed the lead to a **Poolday Automation webhook** (HTTP 202 accepted) → Poolday made a 22s 16:9 Wispr Flow teaser, reusing the approved v3 composition | `04`, `05`, `06` |
| Return | Poolday's agent has **no outbound network**, so it couldn't call back and printed the result JSON instead. The Automation's Output only offers app connectors (Airtable, Apollo…), no webhook. The link was pasted into the dashboard at the human gate (one paste) | `07`, `08`, `09`, `12`, `13` |
| Human validation | Approve / Regenerate with a note / Reject | `10` |
| Email draft | Drafted for the named buyer (Carolyn, VP of Product Marketing, from the dataset). Exported as `.eml`, where `[VIDEO THUMBNAIL]` becomes a **clickable 3-second animated preview** of the video (`wispr-flow-preview.gif`) | `11`, `wispr-flow-email-preview.png`, `wispr-flow-email-sample.eml` |

**Where "Carolyn" comes from:** the lead dataset (`data/series-b-bay-area.csv`). For Wispr Flow it lists "Carolyn [last masked], VP of Product Marketing" as contact 1. The dataset has no email addresses, so "To" is left for the sender to fill in.

**Next (with API access or an Output webhook):** Poolday calls back on its own, and the paste step disappears. The loop already handles signed callbacks (`POST /api/poolday/callback`), revisions, and agent questions.

## How the leads are qualified, and how we know it's any good
**Two stages.**
1. **A rule-based pre-score (code, 0–100)**: freshness of the round 40 + named buyer 25 + B2B 15 + video fit 20. Under 45 = cut without further work (10 of 37).
2. **A 5-criterion rubric, 0–20 each** (B2B, freshness, buyer, visual product, video need), answered per lead with a 2–3 sentence justification that cites only dataset facts.
   - The code enforces freshness from the date bands, total = sum, **no named buyer = knocked out**, and keep ≥ 70.
   - Without an API key, I answered the rubric in Claude Code (`loop/answers/`).

**What "qualified" means:** worth making a free video for, because a fresh round (budget, launch, announcement), a named marketing/creative buyer and a visual product make a personalized video most likely to land.

**Evidence it's coherent (26 Sep, 27 scored leads):**
- Rank correlation 0.83 with the deterministic pre-score and 0.71 with the offline mock scorer. 4 of 5 qualified leads are the same as the mock's.
- It agrees with the manual D2 picks made before the loop existed: Flam #1 and Wispr Flow #2 both qualify; backup Blacksmith qualifies; backup Convex is a close call (67).
- The disagreements are explained:
  - Convex drops because the contact is a marketing manager and the product is a backend.
  - Delightree comes in: fresh round and a Head of Marketing.
  - Flex scores +15 over the mock because it has a Creative Director.
  - Consensus scores −12: mixed audience, HQ unverified.

**Limits:**
- One rater.
- The dataset only: no live check of sites, LinkedIn or HQ (network blocked here; last names masked).
- 5 coarse criteria and a round-number threshold.

**How we'll actually know: outcomes.**
- Send the 5 qualified leads plus 3–5 close calls (65–69) as a control.
- Track video clicks, replies and booked demos by score band. After 20–30 sends, re-weight the criteria and move the threshold to what books.
- Cheap extra check: the CEO scores 10 leads blind, and we compare (agreement between raters).
- With an API key, the same rubric can run automatically as a second opinion (`LLM_MODE=api`).

