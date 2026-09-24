#!/usr/bin/env bash
# End-to-end demo in mock mode: every step of the loop, from a fresh database.
# Usage (from loop/):  make demo      or      bash scripts/demo.sh
set -euo pipefail
cd "$(dirname "$0")/.."
export LLM_MODE="${LLM_MODE:-mock}" LOOP_TODAY="${LOOP_TODAY:-2026-09-24}"
PY="${PYTHON:-python3}"
run() { echo; echo "\$ prospect_loop $*"; $PY -m prospect_loop "$@"; }
id_of() { $PY - "$1" <<'PY'
import sys; from prospect_loop import store
print(next(l["id"] for l in store.all_leads(store.connect()) if l["domain"] == sys.argv[1]))
PY
}

run reset
echo; echo "== 1-3. Find + enrich + qualify + generate Poolday prompts"
run run
FLAM=$(id_of flamapp.ai); WISPR=$(id_of wisprflow.ai)
echo; echo "== Poolday prompt for Flam (human pastes this into Poolday)"
$PY -c "from prospect_loop import store; l=store.get(store.connect(), $FLAM); print(l['poolday_prompts']['command']); print('---- fallback ----'); print(l['poolday_prompts']['fallback'])"
echo; echo "== 4. Human pastes back the video link, then the gate"
run video "$FLAM" "https://poolday.ai/share/demo-flam-v1"
run regenerate "$FLAM" --note "hard cut at 0:04 on the kick, hold the logo 2 frames longer"
run video "$FLAM" "https://poolday.ai/share/demo-flam-v2"
echo; echo "== 5. Approve -> email draft"
run approve "$FLAM"
run video "$WISPR" "https://poolday.ai/share/demo-wispr-v1"
run reject "$WISPR" --note "UI rebuild looks off-brand; redo with brand kit"
echo; echo "== 6. Export drafts (.eml + CSV) for the hiring manager to send"
run export
run list --status exported
echo; echo "Demo OK. Open the dashboard with: make serve"
