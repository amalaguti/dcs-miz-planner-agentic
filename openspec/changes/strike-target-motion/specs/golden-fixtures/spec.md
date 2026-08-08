## ADDED Requirements

### Requirement: Moving U-boat examples
Checked-in mid-Channel U-boat recon and/or hunt Specs MUST demonstrate
`motion: patrol` (or path) on `Uboat_VIIC` sea contacts/targets. Compile asserts
or goldens MUST verify ship unit presence and multi-point route wiring.

#### Scenario: U-boat patrol example green
- **WHEN** the moving U-boat example(s) are validated and compiled in CI
- **THEN** tests MUST pass and assert route/motion evidence in the `.miz`

### Requirement: Soft-vehicle path example
The repository SHALL include a checked-in land GA (or recon) Spec with soft-vehicle
`motion: path` (short inland legs). Compile asserts MUST verify vehicle id and
multi-point route.

#### Scenario: Convoy path example green
- **WHEN** the soft-vehicle path example is validated and compiled in CI
- **THEN** tests MUST pass and assert route/motion evidence in the `.miz`
