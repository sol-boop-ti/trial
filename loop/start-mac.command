#!/usr/bin/env bash
# One-click setup on a Mac: tunnel + settings + dashboard + the Poolday message, filled in.
# Run it with:  bash ~/poolday-trial/loop/start-mac.command
set -uo pipefail
cd "$(dirname "$0")"
ENV="$HOME/secrets/poolday-webhook.env"
LOG="/tmp/poolday-tunnel.log"
say() { printf "\n\033[1m%s\033[0m\n" "$*"; }

# 1. Tools
if ! command -v brew >/dev/null 2>&1; then
  say "Homebrew is missing. Install it first: open https://brew.sh, copy the line on the page into Terminal, then run this again."
  exit 1
fi
command -v cloudflared >/dev/null 2>&1 || { say "Installing cloudflared (one time)…"; brew install cloudflared; }
command -v python3 >/dev/null 2>&1 || { say "Installing Python (one time)…"; brew install python; }

# 2. Settings file with a random secret (created once, kept afterwards)
mkdir -p "$HOME/secrets"
if [ ! -f "$ENV" ]; then
  cat > "$ENV" <<CONF
POOLDAY_API=webhook
PUBLIC_BASE_URL=
POOLDAY_WEBHOOK_SECRET=$(openssl rand -hex 24)
POOLDAY_WEBHOOK_SECRET_HEADER=X-Webhook-Secret
REFERENCE_VIDEO=https://www.instagram.com/reels/DdERJulgHrV/
POOLDAY_WEBHOOK_URL=
CONF
fi
setvar() { # setvar KEY VALUE  (rewrites one line of the settings file)
  python3 - "$ENV" "$1" "$2" <<'PY'
import sys; p, k, v = sys.argv[1:]
lines = [l for l in open(p).read().splitlines() if not l.startswith(k + "=")]
lines.append(f"{k}={v}"); open(p, "w").write("\n".join(lines) + "\n")
PY
}

# 3. Tunnel: gives your Mac a public https address that Poolday can call back
say "Opening the tunnel…"
pkill -f "cloudflared tunnel --url http://localhost:8765" >/dev/null 2>&1
: > "$LOG"
cloudflared tunnel --url http://localhost:8765 >"$LOG" 2>&1 &
TUNNEL_PID=$!
URL=""
for _ in $(seq 1 40); do
  URL=$(grep -Eo 'https://[a-z0-9-]+\.trycloudflare\.com' "$LOG" | head -1)
  [ -n "$URL" ] && break; sleep 1
done
if [ -z "$URL" ]; then say "The tunnel didn't start. Details in $LOG"; exit 1; fi
setvar PUBLIC_BASE_URL "$URL"
set -a; . "$ENV"; set +a
echo "Tunnel: $URL"

# 4. The message for Poolday, filled in and copied to your clipboard
CALLBACK="$URL/api/poolday/callback"
MSG=$(cat <<TXT
I want to trigger my prospect-teaser flow from my own app through a webhook, and get the result posted back to me. Please set this up.

1. Create an inbound webhook endpoint that triggers a saved prompt for this flow. Only accept requests whose header X-Webhook-Secret equals $POOLDAY_WEBHOOK_SECRET. Reply with the webhook URL.

2. Each request is a JSON POST with these fields. Accept all of them and ignore any you don't need: kind ("start", "revision" or "answer"), lead_id, token, version, company, website, brand_kit_name (may be missing), angle, contact_name, contact_role, reference_url, prompt, callback_url. Follow-ups also have note and message (revision), or answer and question (answer).

3. On kind "start": run the prospect-teaser flow for the website, with my ref-teaser skill and my motion-craft skill. Use the brand kit named brand_kit_name if it exists; otherwise build the brand kit from the website first. The reference video is reference_url. The angle is angle. The video is for contact_name (contact_role) at company. prompt holds the same brief as one text. 16:9.

4. On kind "revision": apply the note to the video you made for the same lead_id (in the same conversation if you can), then re-render. On kind "answer": it is my answer to your question for that lead_id, so continue.

5. When the video is done, POST JSON to the callback_url from the request (it is $CALLBACK), with the header X-Webhook-Secret: $POOLDAY_WEBHOOK_SECRET and this body: {"lead_id": <as received>, "token": "<as received>", "version": <as received>, "status": "completed", "video_url": "<shareable link to the final video>", "conversation_url": "<link to this conversation>"}. Echo lead_id, token and version exactly as you received them.

6. If you need a decision from me before building, POST to the same callback_url with "status": "needs_input" and "question": "<your question>", then wait for an "answer" request. If the run fails, POST "status": "failed" and "error": "<why>".

7. If your webhook feature uses a different header name or generates its own secret, tell me the header name and value, and send that same header on the callback.
TXT
)

if [ -z "${POOLDAY_WEBHOOK_URL:-}" ]; then
  printf "%s" "$MSG" | pbcopy
  say "STEP A: The message for Poolday is now in your clipboard."
  echo "  → In Poolday, open the 'API access & API keys' conversation (or a new one, Align mode), paste (Cmd+V) and send."
  echo "  → Poolday will reply with a webhook URL."
  printf "\nPaste the webhook URL Poolday gives you here, then press Enter: "
  read -r HOOK
  setvar POOLDAY_WEBHOOK_URL "$HOOK"
else
  say "Webhook URL already saved. The callback address changed with this tunnel, so tell Poolday:"
  echo "  \"My callback URL is now $CALLBACK\""
  printf "%s" "My callback URL is now $CALLBACK" | pbcopy
  echo "  (copied to your clipboard)"
fi
set -a; . "$ENV"; set +a

# 5. Dashboard
[ -f work/leads.db ] || { say "Preparing the lead list (first time)…"; python3 -m prospect_loop run >/dev/null; }
say "Starting the dashboard: http://localhost:8765"
python3 -m prospect_loop serve >/tmp/poolday-dashboard.log 2>&1 &
SERVER_PID=$!
trap 'kill $SERVER_PID $TUNNEL_PID 2>/dev/null; echo; echo "Stopped."' EXIT
sleep 2; open "http://localhost:8765"

# 6. Test lead
printf "\nSend one test lead (Wispr Flow) to Poolday now? Start your screen recording first. [y/N] "
read -r GO
if [ "$GO" = "y" ] || [ "$GO" = "Y" ]; then
  python3 -m prospect_loop webhook-test --domain wisprflow.ai --brand-kit "Wispr Flow"
  echo "Sent. Watch the dashboard: the video lands in Review when Poolday calls back."
fi
say "Keep this window open while Poolday works. Press Ctrl+C to stop everything."
wait $SERVER_PID
