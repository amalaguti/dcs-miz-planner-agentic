## Context

`MissionSpec.triggers` is `list[dict]` and any non-empty value fails model validation.
R5 shows Channel IA needs native ME triggers (zones, flags, time, unit-dead, messages).
M6 splits Spec (`#20`) from compile (`#21`) so the contract is solid before PyDCS emit.

## Goals / Non-Goals

**Goals:**

- Discriminated, backend-agnostic trigger + zone models (Pydantic, `extra=forbid`).
- Small v1 vocabulary aligned with stock Channel patterns.
- Shared validation of refs (zones, enemy indices).
- Compile hard-fails if behaviour is declared but `#21` is not implemented yet.

**Non-Goals:**

- PyDCS `Triggers` / `action` / `condition` emit.
- Lua, Mist, radio menus, cockpit args.
- Map absolute x/y as the primary authoring mode (prefer airfield-relative like CAP).

## Decisions

1. **Zones are first-class Spec list `zones[]`, referenced by name**
   - Each zone: `name`, `bearing_deg`, `distance_km`, `radius_m` relative to player
     departure airfield (same convention as `cap`/`strike`/`escort`).
   - Alternatives: absolute ME x/z (harder for agent); inline-only zones (duplication).

2. **Trigger rule shape**
   - `TriggerRule`: optional `name`, `once: bool` (default true), `when: list[Condition]`
     (AND), `then: list[Action]` (ordered, non-empty).
   - Empty `when` forbidden; empty `then` forbidden.

3. **Discriminated unions via `type` field**
   - Conditions: `time_more` (`seconds` ≥ 0), `flag_is` (`flag` str, `value` bool),
     `unit_dead` (`enemy_index` 0-based into `enemies`), `coalition_in_zone`
     (`zone`, `coalition`).
   - Actions: `message` (`text`, optional `delay_s`, `duration_s`), `set_flag`
     (`flag`, `value`), `mission_end` (`result`: `win` | `lose`).
   - No free-form `script` / `lua` fields.

4. **Keep schema_version `"1"`**
   - Expand the reserved `triggers` slot; change `list[dict]` to typed models.
   - Alternatives: bump to `"2"` (heavier migration; not needed if loader stays strict).

5. **Compile policy for this change**
   - If `zones` or `triggers` non-empty → `ValueError` / validation-style compile failure
     citing `trigger-compiler-native` not yet available.
   - Specs with empty zones/triggers compile unchanged (all current examples).

6. **Agent surface**
   - Update `get_mission_spec_schema` / prompts: triggers optional; note compile of
     behaviour is future `#21`; do not invent types outside the v1 enum set.

## Risks / Trade-offs

- [Authors write triggers that cannot fly yet] → Clear compile error; README/BACKLOG point
  to `#21` as next.
- [OR vs AND predicates] → v1 AND-only; OR deferred.
- [enemy_index fragile if enemies reordered] → Document 0-based; later named refs optional.
- [PyDCS naming mismatch at `#21`] → Spec stays logical; mapping table lives in compiler.

## Migration Plan

- Additive models; examples stay empty triggers.
- Optional checked-in YAML that **validates** but is marked “compile blocked until #21”
  (test-only fixture, not a flyable example).

## Open Questions

- Whether `flag` is string-only or also int (ME uses numeric flags) — prefer string ids in
  Spec, map to ints at `#21`.
- Whether `once: false` (continuous) ships in v1 (yes as bool; `#21` maps to continuous).
