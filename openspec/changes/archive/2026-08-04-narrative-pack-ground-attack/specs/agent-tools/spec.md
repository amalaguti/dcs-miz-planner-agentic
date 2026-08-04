## ADDED Requirements

### Requirement: Spec schema notes include ground-attack narrative
When `get_mission_spec_schema` describes `ground_attack`, it MUST mention optional
`narrative.enabled` (expands to typed zones/triggers; conflicts with hand-authored
zones/triggers; requires strike and targets).

#### Scenario: Ground-attack schema notes mention narrative
- **WHEN** an agent requests the Spec schema for `ground_attack`
- **THEN** the notes MUST reference optional narrative without inventing unsupported
  trigger types beyond the documented v1 vocabulary (including `target_dead`)

## MODIFIED Requirements

### Requirement: Spec schema notes include narrative
When `get_mission_spec_schema` (or equivalent prompt fragment) describes combat mission
types, it MUST mention optional opt-in `narrative.enabled` for CAP, intercept, escort, and
ground_attack (expands to typed zones/triggers), MUST NOT encourage Lua, and MUST note
that narrative conflicts with hand-authored non-empty zones/triggers.

#### Scenario: Schema notes mention narrative
- **WHEN** an agent requests the Spec schema for `cap`, `intercept`, `escort`, or
  `ground_attack`
- **THEN** the notes MUST reference optional narrative without inventing unsupported
  trigger types
