# Poolday API: what we need from the docs, and how to plug them in

> **Update: the webhook is the path now.** Poolday's CEO says the public API is being
> deprecated. Instead, the Poolday agent creates an inbound webhook that triggers a saved
> prompt, and calls a URL of ours back with the outputs when the conversation is done. The
> loop supports this as `POOLDAY_API=webhook`. For the setup, the message to paste into Poolday,
> the env vars and a 5-step test, see **README.md → "Poolday via webhook (current recommended
> path)"**.
>
> The rest of this page (the `http` mapping) stays for reference, in case a documented API
> comes back. Webhook mode needs none of it: no API key, no endpoint mapping, no polling.
>
> What webhook mode does and does not assume about Poolday:
> - It assumes only that Poolday's webhook accepts a JSON POST with a secret header, and that
>   the agent can POST JSON to our callback URL. Both come from what we ask the agent to do in
>   the pasted message, not from Poolday docs.
> - Our outbound field names are ours (documented in the README). The callback parser accepts
>   many shapes (`video_url`, `url`, `outputs[].url`, `result.video`, `assets[]`, envelopes like
>   `data` or `payload`, lookup by `token` alone). More key paths can be added with
>   `POOLDAY_CALLBACK_KEYS` or `[webhook.keys]` in `poolday_api.toml`, without code changes.
> - Still to confirm on the first real run: the header name Poolday's webhook feature really
>   uses (`POOLDAY_WEBHOOK_SECRET_HEADER`), whether it answers synchronously with a run id
>   (logged if so), the real callback shape (check `api-log`), and whether the video link is
>   shareable and stable (the email needs that).

The loop already drives Poolday through an API. Every Poolday-specific detail (host, auth
header, endpoint paths, field names, status strings) sits in one mapping file. Right now that
file is a template of `TODO`s, because we don't have the docs yet. Nothing in the code is a
guessed Poolday endpoint.

Until the docs arrive, the same code path runs against a **local fake Poolday API**
(`prospect_loop/poolday_fake.py`). The fake deliberately uses its own paths, nested fields,
status strings and auth header, so the mapping machinery is exercised exactly as it will be
with the real one.

```
pipeline ──▶ PooldayClient ──┬─ WebhookPooldayClient ──POST──▶ Poolday inbound webhook
                             │     ▲ POST /api/poolday/callback (server.py) ◀── Poolday agent
                             ├─ HttpPooldayClient ◀── poolday_api.toml (filled from the docs; API being deprecated)
                             ├─ FakePooldayClient  ◀── FAKE_MAPPING ──▶ local fake server
                             └─ ManualPooldayClient   (copy/paste fallback)
```

`POOLDAY_API=webhook|manual|fake|http` picks the client. The default is `webhook` when
`POOLDAY_WEBHOOK_URL` is set, else `http` when `poolday_api.toml` and `POOLDAY_API_KEY` both
exist, otherwise `manual`.

## What the loop needs from Poolday (the interface)

| Operation | Used for | Mapping keys |
|---|---|---|
| `start_production(prompt, attachments, reference_url, settings)` | **Send to Poolday**: a new conversation with the `/prospect-video` prompt (or the fallback kickoff + skill file) in Align mode at a given tier | `endpoints.start`, `request.prompt/mode/tier/attachments/reference_url`, `response.id` |
| `send_message(id, text)` | **Regenerate with note**: revision in the **same** conversation | `endpoints.message`, `request.message_text` |
| `get_status(id)` | Background poller: queued / running / needs_input / done / failed, plus the agent's question | `endpoints.status`, `response.status/question/question_id`, `status_map` |
| `answer_question(id, answer, question_id)` | The human answers the Align-mode question from the dashboard | `endpoints.answer` (or falls back to `message`), `request.answer_text/question_id` |
| `get_result(id)` | Video URL, preview, thumbnail, dropped into the human gate | `endpoints.result` (or the status response), `response.video_url/preview_url/thumbnail_url` |
| upload (inside start) | The Reference Teaser skill file, or a reference video file | `endpoints.upload`, `request.upload_file`, `response.upload_id` |
| `credits()` | Header badge: credits left out of the $2,000 | `endpoints.credits`, `response.credits_remaining/used` |

## Questions to answer from the docs (checklist)

**Auth**
- [ ] Base URL (and whether it's versioned, e.g. `/v1`).
- [ ] How the key is sent: `Authorization: Bearer <key>`, `X-API-Key`, or something else? Where to create a key? Is it per workspace?
- [ ] Any required extra headers (API version, workspace/org/project id)? → `[headers]` / `[request_extra]`.

**Create a conversation / job**
- [ ] Endpoint and method. Is the unit a "conversation", a "project", a "job", or a "run"?
- [ ] The field for the prompt text. Can the first message carry links (reference video, brand URL) as plain text, or is there a dedicated field?
- [ ] Mode: can we set **Align / Build / Clarify** through the API, and with what spelling? If not, does the API run like Build (no questions)?
- [ ] Tier: **Micro / Light / Standard / Max / Ultra** field and spelling. Is there a cost estimate before starting?
- [ ] Aspect ratio / output type fields (16:9 for prospect videos).
- [ ] Do saved **skills and `/commands`** (for example `/prospect-video`) work through the API, or only in the app? If only in the app, set `POOLDAY_PROMPT=fallback` so the kickoff and the skill file are sent instead.
- [ ] Does `brand:<name>` (brand kits) work through the API?
- [ ] The response: where the conversation/job id is.

**Messages (revisions, answers)**
- [ ] Endpoint to post a follow-up in the same conversation.
- [ ] Is answering the agent's question a separate call (with a question id) or just a message?

**Status and webhooks**
- [ ] Status endpoint, and the full list of status strings (map them in `[status_map]`).
- [ ] How a pending question shows up (field path for its text and id).
- [x] Webhooks: done differently from what we planned here. The agent-created webhook plus our `POST /api/poolday/callback` route (`pipeline.handle_callback` → the same `_record` / `submit_video` path) is built. See the README.
- [ ] Recommended polling interval (runs take ~1h; `POOLDAY_POLL_S` defaults to 5 s, which is too fast for real runs. Set 30-60 s.)

**Results**
- [ ] Where the final video URL is (status response or a separate outputs/assets call). Is it a shareable link or a signed URL that expires? The email needs a stable, shareable link.
- [ ] Preview and thumbnail URLs (the email's `[VIDEO THUMBNAIL]` line).
- [ ] Several outputs (variants, versions): which one is "the latest"? (Paths can index lists: `outputs.0.url` is the first, `outputs.-1.url` the last.)

**Files**
- [ ] Upload endpoint, multipart field name, size limits (the agent guide says files up to 1 GB), and how the returned file id is referenced in the start call.

**Limits and cost**
- [ ] Rate limits and the `429` / `Retry-After` behaviour (the poller already stops a pass on 429).
- [ ] Credits/usage endpoint, and how much a run costs per tier.
- [ ] Concurrency: how many conversations can run in parallel on our plan.

## Filling the mapping in 10 minutes

1. `cp poolday_api.example.toml poolday_api.toml` (the key is not in this file, so the file can be committed).
2. Replace every `TODO` from the checklist above. Paths are `"METHOD /path/{id}"`; request and response fields are dotted paths (`settings.mode`, `data.outputs.0.url`). Set optional things you don't have to `""`.
3. `export POOLDAY_API_KEY=...` (shell only; never in a file in the repo).
4. `POOLDAY_API=http python -m prospect_loop poolday-status` → it lists any `TODO` left, or shows the client and credits.
5. Smoke test on one lead with the cheapest tier and Build mode, so it doesn't wait on a question:
   `POOLDAY_API=http POOLDAY_TIER=micro POOLDAY_MODE=build python -m prospect_loop send <id>` then
   `python -m prospect_loop poll --watch --interval 30` and `python -m prospect_loop api-log <id>`.
   Check the raw responses in `api-log` / the dashboard's "Poolday API calls" panel against your
   `[response]` paths. A wrong status path shows as `running` forever. A wrong video path shows as
   `poolday:error done but no video URL`.
6. Then run normally: `POOLDAY_API=http make serve`.

`FAKE_MAPPING` in `prospect_loop/poolday_fake.py` is a fully filled example of the same structure.

## Safety rails that stay on with the API

- The human gate is mandatory. A finished video only moves the lead to **Review**. Approving, drafting the email and exporting are human actions, and nothing is ever emailed by the loop.
- With the real API, a prompt that still contains a `<...>` slot (for example `<REFERENCE VIDEO LINK>`) is refused before any credits are spent. Set `REFERENCE_VIDEO`, or edit the prompt.
- No double submission: "Send" is refused while a production is queued, running or waiting for an answer.
- Every HTTP call is logged in the `api_calls` table: op, method, path, status, latency, and truncated request and response bodies. The auth header is never logged. State changes also go to the lead's event log (`poolday:sent`, `poolday:needs_input`, `poolday:answered`, `poolday:done`, `poolday:revision_sent`, `video_submitted … (from Poolday API)`).
