# Golden Fixtures

## Purpose

Checked-in structural goldens and hermetic pytest regression for free-flight
compile output, starting with the Manston cold free-flight acceptance path.

## Requirements

### Requirement: Checked-in Manston structural golden
The repository SHALL include a checked-in golden fixture for the Manston cold free-flight
Mission Spec compile path. The fixture MUST capture structural expectations for the
produced `.miz` (required zip members and theatre/mission content contracts) without
requiring byte-identical comparison of the entire zip archive.

#### Scenario: Fixture present for Manston example
- **WHEN** a developer inspects the golden-fixture directory for Manston cold free-flight
- **THEN** the repository MUST contain the expected structural artifacts used by the
  regression tests (at minimum theatre identity and mission content contracts for Manston)

### Requirement: Compile output matches Manston golden
The test suite SHALL compile the checked-in Manston cold free-flight Mission Spec with an
injected install inventory that reports `TheChannel` as available and planner-supported,
then compare the resulting `.miz` against the Manston golden fixture. Comparison MUST fail
the test when required zip members are missing or contracted mission/theatre content
diverges from the golden.

#### Scenario: Fresh Manston compile matches golden
- **WHEN** the Manston example Spec is compiled under the golden-fixture test harness
- **THEN** the test MUST pass if and only if the output satisfies the checked-in structural
  golden (including Channel theatre, Spitfire at Manston cold parking, start_time 32400,
  and group frequency 124.0 MHz contracts)

#### Scenario: Intentional mismatch fails
- **WHEN** the compiled output omits a required zip member or changes a contracted field
  covered by the golden (for example theatre id or Spitfire frequency)
- **THEN** the golden-fixture test MUST fail

### Requirement: Explicit golden refresh
Updating golden fixtures MUST be an explicit developer action after an intentional compiler
or fixture-policy change. Ordinary test runs MUST NOT rewrite golden files.

#### Scenario: Normal pytest does not rewrite goldens
- **WHEN** a developer runs the default test suite
- **THEN** files under the golden-fixture directory MUST remain unchanged by that run

### Requirement: Injected inventory for hermetic goldens
Golden-fixture compile tests MUST NOT depend on the developer’s live SQLite install
inventory. They SHALL inject (or otherwise supply) a synthetic inventory sufficient for
`TheChannel` availability so the suite remains hermetic.

#### Scenario: Suite runs without live DCS inventory
- **WHEN** golden-fixture tests run in an environment without a usable cached inventory
- **THEN** the Manston golden compile comparison MUST still execute using the injected
  inventory

### Requirement: Intercept structural golden
The repository SHALL include a golden-fixture regression for the checked-in Manston intercept
compile path (injected Channel inventory), covering required zip members and contracted
mission content for player and enemy aircraft. Ordinary pytest MUST NOT rewrite those
fixtures; refresh MUST be explicit.

#### Scenario: Intercept compile matches golden
- **WHEN** the intercept example Spec is compiled under the golden harness
- **THEN** the test MUST pass if and only if output matches the intercept golden contracts
  (including `Bf-109K-4` and Spitfire presence)
