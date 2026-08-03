## ADDED Requirements

### Requirement: Narrative-produced rules stay in v1 vocabulary
Zones and triggers produced by narrative expansion MUST use only supported v1 condition
types (`time_more`, `flag_is`, `unit_dead`, `coalition_in_zone`) and action types
(`message`, `set_flag`, `mission_end`). They MUST remain eligible for native ME compile
emit without Lua.

#### Scenario: Expanded CAP graph validates
- **WHEN** a CAP Spec with `narrative.enabled: true` is expanded and validated
- **THEN** validation MUST succeed for the resulting zone/trigger graph when pack
  preconditions are met
