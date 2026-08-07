## ADDED Requirements

### Requirement: Validate recon Specs
Validation SHALL accept a well-formed recon Spec and MUST reject: missing/invalid `recon`
geometry, `player.payload`, `strike`/`cap`/`escort` blocks, non-empty air `enemies`,
same-coalition contacts, unknown contact unit ids, missing `recon_area`, and
`attack_ground` (or other unsupported) objectives on recon. Errors MUST name the field path.

#### Scenario: Valid recon passes
- **WHEN** a complete Manston recon Spec is validated
- **THEN** validation MUST succeed with no errors

#### Scenario: Payload on recon fails clearly
- **WHEN** a recon Spec sets `player.payload`
- **THEN** validation MUST fail identifying `player.payload`
