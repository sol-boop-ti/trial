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
| Example event | Nothing to do | It is read-only: it only shows what an incoming request looks like (body, headers, files, query). |

## The prompt
Select everything in the Prompt box, delete, then paste this whole block. `{{event.body}}` is the only field needed: "Insert event field" offers body, files, headers and query, and body holds the whole lead JSON.

```
A lead from my prospect pipeline just arrived. Here is its JSON:
{{event.body}}

Its fields: kind, lead_id, token, version, company, website, brand_kit_name,
angle, contact_name, contact_role, reference_url, prompt, callback_url.

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
