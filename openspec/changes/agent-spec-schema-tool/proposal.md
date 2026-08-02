## Why

Live interactive chat showed the model inventing flat Mission Spec JSON that
Pydantic rejects (`airfield`/`aircraft` top-level, ISO `date` string, wrong
`enemies`, nested `cap.objectives`). A hand-written CAP skeleton in the system
prompt fixed the immediate gap, but that text will drift as ground-attack,
escort, and new options land. Spec shape must be derived from the real contract
(`MissionSpec` / examples), not maintained as prompt prose.

## What Changes

- Add an agent tool (e.g. `get_mission_spec_schema`) that returns a **compact**
  example Spec JSON plus field notes / anti-patterns for a given `mission_type`
  (and shared envelope fields).
- Derive those examples from Pydantic `MissionSpec` and/or checked-in
  `examples/*.yaml` — **not** a hand-edited SQLite schema SoT.
- Shrink the always-on system prompt to stable rules + a short anti-pattern
  reminder; use the derived type-specific example when locking Spec and in the
  host repair nudge after parse failure.
- Optionally cache a derived projection in catalog SQLite (same pattern as
  planning options); sync from code/examples only.
- Wire the tool into the tool bridge + `list`-style discovery used by plan/chat.

## Non-goals

- Provider structured-output / constrained decoding for Spec-emit turns (follow-on).
- Migrating the live LLM client to the Responses API.
- New mission types (ground-attack, escort) or compiler changes.
- Making SQLite the schema source of truth.
- Dumping raw full `model_json_schema()` into the prompt without a compact projection.
- In-game DCS acceptance for this change (agent/CLI/pytest only).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `agent-tools`: add `get_mission_spec_schema` (mission-type-scoped Spec shape + notes)
- `nl-agent`: system prompt / repair path use derived Spec shape instead of a
  hand-maintained full CAP skeleton
- `plan-repl`: chat host repair nudge and Spec-lock guidance use the same derived shape

## Impact

- `tools/surface.py`, `agent/tool_bridge.py`, `agent/prompts.py`, `agent/session.py`,
  `agent/planner.py`; likely a small `agent/spec_schema.py` (or similar) helper
- Tests: tool contract + prompt/repair uses derived example; existing chat/plan green
- Catalog sync only if a cache table is chosen; no change to validate/compile SoT
- Backlog `#10c`; clears the way for M4 mission types without prompt-skeleton sprawl
