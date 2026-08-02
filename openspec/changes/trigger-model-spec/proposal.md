## Why

Missions today only place units and set weather/time; they cannot declare in-flight
behaviour (messages, win/fail, zone events). Stock Channel Spitfire IA uses native ME
triggers for that. The Spec already reserves `triggers` but forces it empty. M6 needs a
typed, Lua-free condition→action model so the agent can plan behaviour and `#21` can
compile it later without inventing ME soup or LLM Lua.

## What Changes

- Define a **minimal Channel-first** trigger model on Mission Spec: zones + trigger rules
  with conditions and actions (no Lua strings in the Spec).
- v1 conditions: `time_more`, `flag_is`, `unit_dead` (enemy flight ref), `coalition_in_zone`.
- v1 actions: `message`, `set_flag`, `mission_end` (win/lose).
- Validate structure and references (zone names, enemy indices, flag ids); reject unknown
  types and Lua-like free text fields.
- Allow non-empty `triggers` / `zones` on schema_version `"1"` Specs that pass validation.
- Compiler **refuses** Specs with non-empty triggers/zones until `trigger-compiler-native`
  (`#21`) — clear error, no silent drop.
- Tests for load/validate of example rules; existing empty-trigger examples still compile.
- Update agent Spec-schema notes / prompts so the planner knows the shape (and that compile
  of behaviour awaits `#21`).

## Non-goals

- Emitting native `.miz` trigger tables (that is `#21`).
- Mist/MOOSE, `a_do_script`, embedded Lua snippets (`#22`).
- Full ME trigger surface, radio menus, cockpit-arg conditions (`#24`).
- Continuous/complex predicate trees beyond a small AND list of v1 conditions.
- Schema version bump (extend `"1"` carefully).

## Capabilities

### New Capabilities
- `mission-triggers`: Typed zones + condition→action rules on the Mission Spec; validation
  contract; compile deferred to `#21`.

### Modified Capabilities
- `mission-spec`: Replace “triggers must be empty” with the new trigger/zone model rules.
- `mission-validation`: Validate trigger/zone graphs; stop blanket-rejecting non-empty
  triggers when well-formed.
- `miz-compiler`: Refuse compile when triggers/zones are non-empty (until `#21`).
- `agent-tools` / Spec schema tool: Expose trigger shape notes for supported mission types
  (optional but recommended).

## Impact

- `models.py`, `validation.py`, loader/examples/tests
- Compiler guard in `pydcs_compiler.py`
- OpenSpec main specs at archive; BACKLOG `#20` → building/done; README next → `#21`
