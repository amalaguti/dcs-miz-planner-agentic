## Why

CAP narrative (`#23`) proved opt-in packs → native ME triggers. Intercept Specs still
ship quiet: scramble and kill with no ops callouts or win/lose. Extending the same
pattern to intercept is the natural next immersion slice without Lua.

## What Changes

- Add intercept narrative pack under existing `narrative.enabled` (dispatch by
  `mission_type`).
- Intercept beats: scramble/push message; bandits-down → message + win (v1; zone callout
  optional if we can share intercept corridor geometry without new Spec fields).
- Example `examples/manston_dawn_intercept_narrative.yaml`; agent schema/prompt notes;
  tests + ME acceptance.
- Refactor narrative module to support multiple packs (CAP unchanged).

## Non-goals

- Escort / ground-attack / free-flight packs (follow-on).
- `#22` Lua snippets; new trigger condition/action types.
- Changing intercept enemy placement geometry in the compiler (narrative may *reuse*
  known Manston corridor constants only if documented; prefer Spec-relative zones if added).
- Default-on narrative; auto-inject when triggers already present.

## Capabilities

### New Capabilities

- (none — extends existing `mission-narrative`)

### Modified Capabilities

- `mission-narrative`: Intercept pack when `mission_type: intercept` and
  `narrative.enabled`; CAP pack remains.
- `mission-spec`: Narrative enabled for intercept (not CAP-only).
- `agent-tools`: Schema notes mention intercept narrative.
- `golden-fixtures`: Intercept narrative example compile coverage.

## Impact

- `narrative.py` multi-pack dispatch; example YAML; agent notes; tests; BACKLOG/README.
- Acceptance: ME Triggers shows intercept narrative rules on compiled example.
