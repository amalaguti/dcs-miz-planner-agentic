## MODIFIED Requirements

### Requirement: Optional narrative on Mission Spec
The Mission Spec MAY include a `narrative` object with `enabled` (boolean, default
false). Supported types are `cap`, `intercept`, `escort`, `ground_attack`, and `recon`.

#### Scenario: Recon narrative field loads
- **WHEN** a Spec YAML includes `narrative: { enabled: true }` with an otherwise valid recon
- **THEN** structural load MUST succeed (subject to recon expand rules)

## ADDED Requirements

### Requirement: Optional scenery on Mission Spec
The Mission Spec MAY include a `scenery` list of airfield-relative static objects.
Types MUST be curated PyDCS fortification ids. Unknown types MUST fail validation.

#### Scenario: Scenery field loads
- **WHEN** a Spec YAML includes `scenery` with a known type such as `Hangar A`
- **THEN** structural load MUST succeed
