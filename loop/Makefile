PY ?= python3
export LOOP_TODAY ?= 2026-09-24

.PHONY: demo demo-api seed serve serve-fake fake-poolday test reset claude-tasks claude-import

demo:            ## full loop end to end in mock mode, printed to the terminal
	LLM_MODE=mock bash scripts/demo.sh

demo-api:        ## the loop driving the (fake) Poolday API from the terminal: send, question, answer, revision
	bash scripts/demo_poolday_api.sh

seed: reset      ## fresh DB with leads found + qualified (start of the screen recording)
	$(PY) -m prospect_loop run

serve:           ## review dashboard on http://127.0.0.1:8765
	$(PY) -m prospect_loop serve

serve-fake:      ## dashboard with the local fake Poolday API (runs advance every 3s, poller every 2s)
	POOLDAY_API=fake FAKE_POOLDAY_STEP_S=3 POOLDAY_POLL_S=2 $(PY) -m prospect_loop serve

fake-poolday:    ## standalone fake Poolday API on :8766 (NOT Poolday's real API)
	$(PY) -m prospect_loop fake-poolday --port 8766

test:
	LLM_MODE=mock $(PY) -m unittest discover -s tests -v

reset:
	$(PY) -m prospect_loop reset

claude-tasks:    ## Claude Code mode: dump pending LLM tasks to work/llm_tasks.json
	$(PY) -m prospect_loop llm-export

claude-import:   ## Claude Code mode: load the answered tasks
	$(PY) -m prospect_loop llm-import
