## ADDED Requirements

### Requirement: Spec schema notes include escort narrative
When `get_mission_spec_schema` describes `escort`, it MUST mention optional
`narrative.enabled` (expands to typed zones/triggers; conflicts with hand-authored
zones/triggers; requires escort, package, and enemies).

#### Scenario: Escort schema notes mention narrative
- **WHEN** an agent requests the Spec schema for `escort`
- **THEN** the notes MUST reference optional narrative without inventing unsupported
  trigger types
