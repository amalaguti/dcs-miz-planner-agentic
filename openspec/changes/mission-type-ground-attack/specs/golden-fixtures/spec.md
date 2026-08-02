## ADDED Requirements

### Requirement: Ground-attack structural golden
The repository SHALL include a golden-fixture regression for the checked-in Manston
ground-attack example Spec. Contracts MUST cover required `.miz` members and mission content
for player GroundAttack tasking, bomb loadout CLSIDs, and declared ground targets. Ordinary
pytest MUST NOT rewrite those fixtures; a documented refresh helper MAY update them when
intentionally changing compile output.

#### Scenario: Ground-attack compile matches golden
- **WHEN** the ground-attack example Spec is compiled under the golden harness
- **THEN** the test MUST pass if and only if output matches the ground-attack golden
  contracts (including Spitfire presence, GroundAttack-related contracts, payload CLSIDs, and
  ground unit types as designed)
