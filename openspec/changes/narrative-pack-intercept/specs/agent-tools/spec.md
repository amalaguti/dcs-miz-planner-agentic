## ADDED Requirements

### Requirement: Spec schema notes include intercept narrative
When `get_mission_spec_schema` describes `intercept`, it MUST mention optional
`narrative.enabled` (expands to typed triggers; conflicts with hand-authored
zones/triggers; requires enemies).

#### Scenario: Intercept schema notes mention narrative
- **WHEN** an agent requests the Spec schema for `intercept`
- **THEN** the notes MUST reference optional narrative without inventing unsupported
  trigger types
