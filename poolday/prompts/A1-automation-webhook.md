# A1: Poolday Automation "Prospect video from pipeline" (Automations → New automation)
1. **Input:** click **Webhook** ("Any system that can POST").
2. **Prompt:** paste the text below. After you **save**, Poolday shows the **webhook URL and a secret**.
3. Put the secret into the prompt where it says `<SECRET>` (edit the automation), and give both the URL and the secret to the Mac script.

```
A lead from my prospect pipeline just arrived as JSON, with the fields: kind, lead_id,
token, version, company, website, brand_kit_name, angle, contact_name, contact_role,
reference_url, prompt, callback_url.

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
