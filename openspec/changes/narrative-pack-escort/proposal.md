## Why

CAP and intercept narrative packs ship; escort Specs still compile quiet despite having
a Spec-relative destination and optional bounce. Extending the same opt-in pack pattern
to escort completes the air-combat mission-type set without Lua.

## What Changes

- Add escort narrative pack under `narrative.enabled` (dispatch by `mission_type`).
- Escort beats: push/join-package message; destination zone + on-station-style callout;
  bandits-down → win when enemies present (v1 requires enemies for the win path).
- Example `examples/manston_escort_narrative.yaml`; agent notes; tests; ME acceptance.
- CAP/intercept packs unchanged.

## Non-goals

- Ground-attack narrative; `#22` Lua; new trigger types; default-on narrative.
- Tracking package-group alive/dead (no Spec hook for package unit_dead yet).

## Capabilities

### New Capabilities

- (none — extends `mission-narrative`)

### Modified Capabilities

- `mission-narrative`: Escort pack; supported types become cap | intercept | escort.
- `agent-tools`: Schema notes for escort narrative.
- `golden-fixtures`: Escort narrative example coverage.

## Impact

- `narrative.py`; example YAML; agent prompts/schema; tests; BACKLOG/README.
- Acceptance: ME Triggers shows escort narrative rules on compiled example.
