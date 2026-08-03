## Why

Native zones/triggers compile (`#20`–`#21`), but combat Specs still ship as quiet
placements: no on-station callouts, bandit-down feedback, or win/lose. Players feel
placement, not a sortie. With trigger emit proven in Instant Action, the next value is
**curated narrative events** on real mission types — still typed Spec rules, no LLM Lua.

## What Changes

- Opt-in Spec narrative for **CAP first**: expand into typed `zones`/`triggers` (messages +
  `unit_dead` → success; squadron-commander tone) when the author/agent enables it.
- Ship a compileable CAP example that demonstrates the beats in ME Triggers / Instant Action.
- Teach the agent schema/prompts that narrative is opt-in and expands to existing trigger vocab
  (no new condition/action types in v1; no `#22` Lua).
- Tests: expanded Spec validates/compiles; golden or structural asserts on emitted rules.

## Non-goals

- Lua / Mist / MOOSE / `script-snippet-library` (`#22`).
- Auto-injecting narrative into every combat Spec by default (opt-in only).
- Intercept / strike / escort narrative packs (follow-on once CAP pattern lands).
- New trigger condition/action types, radio VO audio, or cockpit-arg triggers (`#24`).
- Changing briefing `l10n` generation (`#16`) beyond reusing voice tone for message text.

## Capabilities

### New Capabilities

- `mission-narrative`: Opt-in narrative expansion that materializes typed zones/triggers for
  immersion events (CAP v1) in squadron-commander voice.

### Modified Capabilities

- `mission-spec`: Optional narrative field (or equivalent) on Mission Spec; CAP example may
  carry narrative / expanded triggers.
- `mission-triggers`: Clarify that narrative-produced rules MUST remain within the existing
  v1 condition/action vocabulary and remain compileable.
- `agent-tools`: Schema notes / guidance mention opt-in narrative for combat types.
- `golden-fixtures`: CAP (or dedicated) fixture coverage for narrative-expanded triggers.

## Impact

- Spec model + validation; small narrative expander module; CAP example YAML; agent
  schema/prompts; tests; BACKLOG `#23` → building; README next pointer.
- Compiler path unchanged except consuming expanded Spec triggers (existing emit).
- Acceptance: open narrative CAP `.miz` in ME Triggers and Instant Action; hear/see on-station
  and bandit-down / win beats.
