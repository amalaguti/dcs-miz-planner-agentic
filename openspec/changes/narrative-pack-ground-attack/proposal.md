## Why

CAP, intercept, and escort narrative packs ship; ground-attack Specs still compile quiet
despite having a Spec-relative strike area and destroyable targets. Extending the same
opt-in pack pattern to ground_attack completes the combat mission-type set without Lua.

## What Changes

- Add ground-attack narrative pack under `narrative.enabled` (dispatch by `mission_type`).
- GA beats: push message; strike-area zone + ingress callout; first-target dead → win.
- Add typed condition `target_dead` (index into `targets[]`) so win works without air
  `enemies` (GA schema forbids air enemies).
- Example `examples/manston_ground_attack_narrative.yaml`; agent notes; tests; ME acceptance.
- Existing CAP / intercept / escort packs unchanged.

## Non-goals

- `#22` Lua snippets; default-on narrative; free_flight narrative.
- Per-unit (vs group) dead conditions; multi-target AND win logic in v1 (first target group only).
- Changing combat vs practice strike rules.

## Capabilities

### New Capabilities

- (none — extends `mission-narrative` and trigger vocabulary)

### Modified Capabilities

- `mission-narrative`: GA pack; supported types become cap | intercept | escort | ground_attack.
- `mission-triggers`: Add `target_dead` condition (index into `targets[]`).
- `miz-compiler`: Emit `target_dead` as GroupDead for compiled target groups; collect target group ids from GA placement.
- `agent-tools`: Schema notes for ground_attack narrative.
- `golden-fixtures`: GA narrative example coverage.

## Impact

- `narrative.py`, `models.py`, `validation.py`, `triggers_emit.py`, `pydcs_compiler.py`;
  example YAML; agent prompts/schema; tests; BACKLOG/README.
- Acceptance: ME Triggers shows GA narrative rules on compiled example.
