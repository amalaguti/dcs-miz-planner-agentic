## Why

Live creativity eval (2026-08-05) still fails vague immersion asks: bare free_flight after
“interesting”, ground_attack without mark/smoke, Big Show without campaigns, and wasted
`randomize_mission` turns on fake paths. Prompts alone are not enough — host floor + better
schema examples.

## What Changes

- Prefer immersion Spec examples from `get_mission_spec_schema` (gates FF, marked GA, …).
- Host immersion repair nudge once when prompt cues immersion but Spec is bare.
- Stronger invent-time prompt rules for interesting FF / find-target GA / campaign names.
- Remove `randomize_mission` from the default invent tool surface (CLI/`dcs-miz randomize` remains).

## Non-goals

- Hard validate fail for every bare Spec (pilot may want bare on request)
- New ME predicates or `#22` Lua
- `#8a.2` maintenance slash

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Immersion floor nudge + invent tool surface without randomize
- `agent-tools`: Schema examples prefer immersion Specs; randomize not default invent tool

## Impact

- `agent/immersion.py` (new), `planner.py`, `session.py`, `prompts.py`, `spec_schema.py`,
  `tool_bridge.py`
- Tests for cues/nudge/schema/tool list; BACKLOG/LESSONS if needed
