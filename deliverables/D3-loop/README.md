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
