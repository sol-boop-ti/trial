PY ?= python3
export LOOP_TODAY ?= 2026-09-24

.PHONY: demo seed serve test reset claude-tasks claude-import

demo:            ## full loop end to end in mock mode, printed to the terminal
	LLM_MODE=mock bash scripts/demo.sh

seed: reset      ## fresh DB with leads found + qualified (start of the screen recording)
	$(PY) -m prospect_loop run

serve:           ## review dashboard on http://127.0.0.1:8765
	$(PY) -m prospect_loop serve

test:
	LLM_MODE=mock $(PY) -m unittest discover -s tests -v

reset:
	$(PY) -m prospect_loop reset

claude-tasks:    ## Claude Code mode: dump pending LLM tasks to work/llm_tasks.json
	$(PY) -m prospect_loop llm-export

claude-import:   ## Claude Code mode: load the answered tasks
	$(PY) -m prospect_loop llm-import
