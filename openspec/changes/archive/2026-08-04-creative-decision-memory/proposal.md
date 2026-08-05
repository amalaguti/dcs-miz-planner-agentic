## Why

The agent can now invent immersion via `mission_behaviour` / `mission_inspiration`, but
each vague ask starts cold — generation history and feedback do not capture which creative
choices were made or whether they landed. Closing that loop lets taste improve locally
without training models or inventing Lua.

## What Changes

- On successful plan/accept, record structured creative decisions in existing
  `generation_history.detail_json` (inspiration ids, behaviour ids, optional sources).
- When recording satisfaction feedback linked to a generation, allow tags/notes that
  refer to those behaviours (no new feedback schema required if tags suffice).
- Before inventing immersion on vague asks, consult recent history + feedback and **bias**
  prompts toward behaviours that scored well (and soft-avoid ones that scored poorly) for
  the same mission type when possible.
- Optional prefs keys for explicit taste (`preferred_behaviours` / `avoid_behaviours` /
  `creativity_level`) if cheap; otherwise derive bias purely from history+feedback in v1.
- Tests for detail shape, prompt/bias helper, and host recording path.

## Non-goals

- Auto-rewriting `planning_options.yaml` or promoting Doc/research into Spec.
- ML ranking, cloud sync, or multi-user profiles.
- Parsing full Spec YAML to infer behaviours after the fact as the only path (prefer
  explicit detail at record time; optional light infer later).
- Changing Mission Spec schema or compiler.

## Capabilities

### New Capabilities

- (none — extends existing memory / agent surfaces)

### Modified Capabilities

- `user-memory`: Structured creative-decision fields in generation detail; optional taste
  prefs; readback usable for bias.
- `agent-tools`: Tools/prompts document recording creative detail and consulting history
  for bias; optional helper surface if needed.
- `nl-agent`: Planning guidance uses history/feedback (and prefs) to bias creative
  behaviour selection on vague asks.
- `golden-fixtures`: Hermetic tests for detail recording and bias helper.

## Impact

- `memory/` (detail convention; optional prefs keys), planner/chat `record_generation`
  call sites, `prompts.py` / optional small bias helper, `tool_bridge` descriptions,
  tests, BACKLOG/README briefly.
- Acceptance: not ME-facing — CLI/API tests that a recorded generation carries creative
  detail and that prompt/bias input prefers high-scoring behaviours.
