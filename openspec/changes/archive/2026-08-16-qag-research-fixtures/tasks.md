## 1. Package QAG index

- [x] 1.1 Point the index at gitignored `research/` HTML paths (ASCII/exact folder names); do not copy the duplicate Cold War anti-ship file; do not ship the HTML
- [x] 1.2 Add `qag_index.yaml` with id, html (relative to `research/`), era, qag_types, spec_mission_types, theatres, keywords, enabled/skip_reason

## 2. Loader + research wiring

- [x] 2.1 Implement HTML extract + match/score loader (stdlib parser; disclaimer in snippets; cap notes; skip missing files)
- [x] 2.2 Merge QAG notes into `fixture_notes` / `gather_research_notes` when the dump exists; sources `fixture:qag:<id>`
- [x] 2.3 Update invent/chat prompts: QAG labels ≠ Spec ids; no SEAD/anti-ship Spec types from research

## 3. Tests and docs

- [x] 3.1 Pytest: stub `research/` for GA/`focus=mission_design`/`fixture:qag:`; anti-ship does not double; missing dump has no QAG notes; canned intercept notes still work
- [x] 3.2 README, ARCHITECTURE, THEATRE_TARGET_PROMOTE, agent-tooling lesson + skill, BACKLOG row
- [x] 3.3 ruff + `uv run pytest -q`
