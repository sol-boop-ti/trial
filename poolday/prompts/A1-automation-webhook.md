# A1: Poolday Automation "Prospect video from pipeline" (Automations → New automation)

## The form, section by section
| Section | What to set | Why |
|---|---|---|
| Input | **Webhook** | Our pipeline POSTs each lead as JSON. |
| Require HMAC signature | **Uncheck** | Our pipeline doesn't sign requests with HMAC. With it checked, Poolday would reject every lead. |
| Idempotency header | **Leave empty** | Optional; each lead already has its own id and version. |
| Attach files from events | Leave as is | We send no files, so it changes nothing. |
| Output | **Add nothing** | The prompt itself posts the result back to our pipeline (callback_url). |
| Prompt | **New conversation** | One conversation per lead, so a revision stays readable. |
| Example event | Paste the JSON below | This makes the fields appear in "Insert event field". |

## Example event (paste into "Example event")
```json
{"kind": "start", "lead_id": 1, "token": "test-token", "version": 1,
 "company": "Wispr Flow", "website": "https://wisprflow.ai", "brand_kit_name": "Wispr Flow",
 "angle": "Voice typing that is 4x faster than your keyboard",
 "contact_name": "Tanay Kothari", "contact_role": "CEO",
 "reference_url": "https://www.instagram.com/reels/DdERJulgHrV/",
 "prompt": "Make a 20s prospect teaser for Wispr Flow.",
 "callback_url": "https://example.trycloudflare.com/api/poolday/callback"}
```

## The prompt
Paste it, then replace each `[field]` with **Insert event field → field** (select `[kind]`, click Insert event field, choose kind, and so on). If the menu offers the whole event/body in one item, you can insert that once instead of the Lead block.

```
A lead from my prospect pipeline just arrived.
Lead:
- kind: [kind]
- lead_id: [lead_id]
- token: [token]
- version: [version]
- company: [company]
- website: [website]
- brand_kit_name: [brand_kit_name]
- angle: [angle]
- contact_name: [contact_name]
- contact_role: [contact_role]
- reference_url: [reference_url]
- prompt: [prompt]
- callback_url: [callback_url]

If kind is "start": make a ~20s 16:9 prospect teaser for the company with my
ref-teaser and motion-craft skills. Use the brand kit named brand_kit_name if it
exists; otherwise build one from the website first. Reference video: reference_url.
Angle: angle. It is for contact_name (contact_role). Don't wait for me at the
approval step: decide yourself, since a human reviews the video in my pipeline.
If kind is "revision": apply the note to the video you made for this lead_id and
re-render.

When the video is done, POST JSON to callback_url with the header
X-Webhook-Secret: <SECRET> and this body: {"lead_id": <as received>,
"token": "<as received>", "version": <as received>, "status": "completed",
"video_url": "<shareable link to the final video>",
"conversation_url": "<link to this conversation>"}.
If it fails, POST the same fields with "status": "failed" and "error": "<why>".
```

## `<SECRET>`
`bash ~/poolday-trial/loop/start-mac.command` puts your secret in the clipboard (step A). Paste it over `<SECRET>`, then save the automation. Never paste the secret in a chat.

## After saving
Copy the automation's **webhook URL** and paste it into the Mac script when it asks. The callback address travels inside each lead, so restarting the tunnel doesn't require any Poolday change.
