#!/usr/bin/env bash
# The loop driving Poolday through an API, end to end, against the local FAKE Poolday API.
# Same code path as the real API: only the mapping differs (see POOLDAY_API.md).
# Usage (from loop/):  make demo-api
set -euo pipefail
cd "$(dirname "$0")/.."
export LLM_MODE="${LLM_MODE:-mock}" LOOP_TODAY="${LOOP_TODAY:-2026-09-24}"
export POOLDAY_API=fake FAKE_POOLDAY_STEP_S="${FAKE_POOLDAY_STEP_S:-1}"
PORT="${FAKE_POOLDAY_PORT:-8766}"
export POOLDAY_FAKE_URL="http://127.0.0.1:$PORT"
PY="${PYTHON:-python3}"
run() { echo; echo "\$ prospect_loop $*"; $PY -m prospect_loop "$@"; }
id_of() { $PY - "$1" <<'PY'
import sys; from prospect_loop import store
print(next(l["id"] for l in store.all_leads(store.connect()) if l["domain"] == sys.argv[1]))
PY
}

$PY -m prospect_loop fake-poolday --port "$PORT" & FAKE_PID=$!
trap 'kill $FAKE_PID 2>/dev/null' EXIT
sleep 1

run reset
run run
FLAM=$(id_of flamapp.ai)
run poolday-status
echo; echo "== Send the generated prompt to Poolday through the API"
run send "$FLAM"
run poll --watch --interval 1
echo; echo "== Poolday's agent asked a question (Align mode): the human answers"
run answer "$FLAM" "Go ahead with the 20s 16:9 cut."
run poll --watch --interval 1
echo; echo "== The video is in the human gate. Regenerate with a note -> same conversation"
run regenerate "$FLAM" --note "hard cut at 0:04 on the kick, hold the logo 2 frames longer"
run poll --watch --interval 1
echo; echo "== Human approves v2 -> email draft (nothing is sent)"
run approve "$FLAM"
run api-log "$FLAM"
echo; echo "Demo OK. Dashboard with the fake API: make serve-fake"
