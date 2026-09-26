#!/usr/bin/env bash
# One-click setup on a Mac: tunnel + settings + dashboard + the Poolday message, filled in.
# Run it with:  bash ~/poolday-trial/loop/start-mac.command
set -uo pipefail
cd "$(dirname "$0")"
ENV="$HOME/secrets/poolday-webhook.env"
LOG="/tmp/poolday-tunnel.log"
say() { printf "\n\033[1m%s\033[0m\n" "$*"; }

# 1. Tools (Homebrew is often installed but not on the PATH: find it)
for b in /opt/homebrew/bin/brew /usr/local/bin/brew; do
  if ! command -v brew >/dev/null 2>&1 && [ -x "$b" ]; then
    eval "$("$b" shellenv)"
    grep -q "brew shellenv" "$HOME/.zprofile" 2>/dev/null || echo "eval \"\$($b shellenv)\"" >> "$HOME/.zprofile"
  fi
done
if ! command -v brew >/dev/null 2>&1; then
  say "Homebrew is missing. Install it first: open https://brew.sh, copy the line on the page into Terminal, then run this again."
  exit 1
fi
command -v cloudflared >/dev/null 2>&1 || { say "Installing cloudflared (one time)…"; brew install cloudflared; }
command -v python3 >/dev/null 2>&1 || { say "Installing Python (one time)…"; brew install python; }
command -v ffmpeg >/dev/null 2>&1 || { say "Installing ffmpeg (one time, for the email video previews: a few minutes)…"; brew install ffmpeg; }

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

# 4. Connect the Poolday automation (Automations tab → webhook input).
# The callback address travels inside each lead, so a new tunnel needs no Poolday change.
if [ -z "${POOLDAY_WEBHOOK_URL:-}" ]; then
  printf "%s" "$POOLDAY_WEBHOOK_SECRET" | pbcopy
  say "STEP A: your callback secret is now in your clipboard."
  echo "  → In the Poolday automation prompt, select <SECRET> and paste (Cmd+V) over it. Save the automation."
  echo "  → Copy the automation's webhook URL."
  printf "\nPaste the automation's webhook URL here, then press Enter: "
  read -r HOOK
  setvar POOLDAY_WEBHOOK_URL "$HOOK"
else
  echo "Poolday automation URL already saved."
fi
set -a; . "$ENV"; set +a

# 5. Dashboard
[ -f work/leads.db ] || { say "Preparing the lead list (first time)…"; python3 -m prospect_loop run >/dev/null; }
say "Starting the dashboard: http://localhost:8765"
# Free the port if another program (e.g. an old "python3 -m http.server 8765") holds it
OLD=$(lsof -ti tcp:8765 2>/dev/null || true)
[ -n "$OLD" ] && { echo "Port 8765 was busy (process $OLD): closing it."; kill $OLD 2>/dev/null; sleep 1; }
python3 -m prospect_loop serve >/tmp/poolday-dashboard.log 2>&1 &
SERVER_PID=$!
trap 'kill $SERVER_PID $TUNNEL_PID 2>/dev/null; echo; echo "Stopped."' EXIT
for _ in $(seq 1 20); do curl -s http://localhost:8765/api/meta >/dev/null 2>&1 && break; sleep 0.5; done
if ! curl -s http://localhost:8765/api/meta >/dev/null 2>&1; then
  say "The dashboard didn't start. Details:"; tail -20 /tmp/poolday-dashboard.log; exit 1
fi
if curl -s "$URL/api/poolday/callback" | grep -q '"ok"'; then echo "Tunnel → dashboard: OK"; else echo "Warning: the tunnel doesn't reach the dashboard yet (it can take ~30s)."; fi
open "http://localhost:8765"

# 6. Test lead
printf "\nSend one test lead (Wispr Flow) to Poolday now? Start your screen recording first. [y/N] "
read -r GO
if [ "$GO" = "y" ] || [ "$GO" = "Y" ]; then
  python3 -m prospect_loop webhook-test --domain wisprflow.ai --brand-kit "Wispr Flow"
  echo "Sent. Watch the dashboard: the video lands in Review when Poolday calls back."
fi
say "Keep this window open while Poolday works. Press Ctrl+C to stop everything."
wait $SERVER_PID
