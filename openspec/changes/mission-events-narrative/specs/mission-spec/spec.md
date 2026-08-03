## ADDED Requirements

### Requirement: Optional narrative on Mission Spec
The Mission Spec MAY include a `narrative` object with `enabled` (boolean, default
false). When omitted, behaviour MUST match Specs with no narrative. Enabling narrative
MUST NOT introduce Lua or script fields on the Spec.

#### Scenario: Narrative field loads
- **WHEN** a Spec YAML includes `narrative: { enabled: true }` with an otherwise valid CAP
- **THEN** structural load MUST succeed (subject to narrative expansion/validation rules)

#### Scenario: Unknown narrative fields rejected
- **WHEN** `narrative` includes an undeclared field
- **THEN** loading MUST fail (unknown field)
