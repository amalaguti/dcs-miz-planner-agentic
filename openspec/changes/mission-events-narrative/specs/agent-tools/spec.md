## ADDED Requirements

### Requirement: Spec schema notes include narrative
When `get_mission_spec_schema` (or equivalent prompt fragment) describes combat mission
types, it MUST mention optional opt-in `narrative.enabled` for CAP (expands to typed
zones/triggers), MUST NOT encourage Lua, and MUST note that narrative conflicts with
hand-authored non-empty zones/triggers.

#### Scenario: Schema notes mention narrative
- **WHEN** an agent requests the Spec schema for `cap`
- **THEN** the notes MUST reference optional narrative without inventing unsupported
  trigger types
