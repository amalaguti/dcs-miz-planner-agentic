## ADDED Requirements

### Requirement: Optional dynamics expand pack on Mission Spec
The Mission Spec SHALL allow an optional `dynamics` object with `mode` one of
`fixed`, `live`, `choose`, `hybrid`, a non-empty `pools` list (except `fixed` may
omit pools), optional `roll` / `menu` / `exclusive` fields as designed. Pool entries
MUST reference existing enemy and/or target indices only (no invented unit placement).
When `dynamics` is set, zones and triggers MUST be empty before expand (same conflict
rule family as narrative). The system MUST expand `dynamics` into typed native trigger
actions (`set_flag_random`, radio items, `activate_group`, messages as applicable)
before validation/compile completes, without LLM Lua.

#### Scenario: Live mode expands dice and activates late enemies
- **WHEN** a Spec has `dynamics.mode: live`, late-activated enemies, empty triggers, and
  pools with `roll_value` / `enemy_indices`
- **THEN** expand MUST emit `set_flag_random` and activate the matching enemy groups
  via existing Spec trigger vocabulary

#### Scenario: Choose mode expands F10 menu
- **WHEN** a Spec has `dynamics.mode: choose` with pool `menu_label`s and late enemies
- **THEN** expand MUST emit radio menu items that activate the corresponding pools

#### Scenario: Dynamics conflicts with hand triggers
- **WHEN** `dynamics` is set and `triggers` is non-empty
- **THEN** validation MUST fail with a clear conflict error

#### Scenario: Narrative and dynamics not both expanding
- **WHEN** both `narrative.enabled` and `dynamics` would expand into an empty trigger
  graph
- **THEN** validation MUST reject the combination (XOR expand authority)
