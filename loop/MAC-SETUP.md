# Run the prospect loop on your Mac with Poolday (webhook mode)

Poolday calls you back at a public address, so the loop runs on your Mac with a free Cloudflare tunnel. Time: ~15 minutes.

## 0. One-time install
```bash
# Homebrew, if you don't have it: https://brew.sh
brew install cloudflared python
git clone -b claude/compassionate-cerf-1jgdrj https://github.com/sol-boop-ti/trial.git ~/poolday-trial
```

## 1. Terminal 1: open the tunnel (leave it running)
```bash
cloudflared tunnel --url http://localhost:8765
```
Copy the `https://….trycloudflare.com` address it prints.

## 2. Terminal 2: settings
Create the file `~/secrets/poolday-webhook.env` with this content (TextEdit, plain text), pasting your tunnel address:
```
POOLDAY_API=webhook
PUBLIC_BASE_URL=https://PASTE-THE-TRYCLOUDFLARE-ADDRESS
POOLDAY_WEBHOOK_SECRET=PASTE-A-LONG-RANDOM-STRING
POOLDAY_WEBHOOK_SECRET_HEADER=X-Webhook-Secret
REFERENCE_VIDEO=https://www.instagram.com/reels/DdERJulgHrV/
POOLDAY_WEBHOOK_URL=
```
Get a random secret with `openssl rand -hex 24`. Then:
```bash
set -a; . ~/secrets/poolday-webhook.env; set +a
cd ~/poolday-trial/loop
python3 -m prospect_loop callback-url       # → your <CALLBACK_URL>
echo "$POOLDAY_WEBHOOK_SECRET"              # → your <SECRET>
```

## 3. In Poolday: new conversation "Prospect video webhook" (Align)
Paste the message from `README.md` → "Poolday via webhook", replacing `<CALLBACK_URL>` and `<SECRET>`. Poolday answers with a **webhook URL**. Put it after `POOLDAY_WEBHOOK_URL=` in the env file, then:
```bash
set -a; . ~/secrets/poolday-webhook.env; set +a
make seed serve          # dashboard at http://localhost:8765 (next times: make serve)
```

## 4. Terminal 3: test
```bash
cd ~/poolday-trial/loop && set -a; . ~/secrets/poolday-webhook.env; set +a
curl -s $PUBLIC_BASE_URL/api/poolday/callback            # {"ok": true…} means the tunnel works
python3 -m prospect_loop webhook-test --domain wisprflow.ai --brand-kit "Wispr Flow"
```
Watch the dashboard: the lead shows "waiting for Poolday". When Poolday calls back, it lands in **Review** with the video. Approve it, and the email draft appears.

## Notes
- The tunnel address changes each time cloudflared restarts. Update `PUBLIC_BASE_URL`, restart `make serve`, and give Poolday the new callback URL.
- Record your screen during step 4. That's the demo for the deliverable.
- The env file lives in `~/secrets`, outside the repo. Never commit it.
