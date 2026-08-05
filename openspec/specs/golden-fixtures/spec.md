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

### Requirement: CAP structural golden
The repository SHALL include a golden-fixture regression for the checked-in Manston CAP
compile path (injected Channel inventory), covering required zip members and contracted
mission content for player CAP tasking (Orbit / engagement) and any example enemies.
Ordinary pytest MUST NOT rewrite those fixtures; refresh MUST be explicit.

#### Scenario: CAP compile matches golden
- **WHEN** the CAP example Spec is compiled under the golden harness
- **THEN** the test MUST pass if and only if output matches the CAP golden contracts
  (including Spitfire presence, CAP/Orbit-related contracts, and engagement/ROE as designed)

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

### Requirement: Escort golden fixture
The test suite SHALL include a hermetic golden fixture for the Manston escort example that
asserts required `.miz` zip members and structural mission contracts for Escort tasking,
friendly package aircraft presence, and player placement/frequency — without requiring a
live DCS install at test time.

#### Scenario: Escort golden regresses structure
- **WHEN** the Manston escort example is compiled in tests and compared to its golden
  fixture
- **THEN** required members and escort structural contracts MUST match (allowing documented
  volatile fields such as onboard numbers)

### Requirement: Briefing dictionary in golden coverage
Golden-fixture (or equivalent contract) coverage for Manston example compiles SHALL
include the mission localisation dictionary member `l10n/DEFAULT/dictionary` (or assert
equivalent non-empty Sortie / Description / player Task content). Empty briefing
dictionary strings MUST fail the suite after this capability ships.

#### Scenario: Dictionary member asserted
- **WHEN** a Manston example Spec is compiled under the golden harness
- **THEN** the comparison or contracts MUST require `l10n/DEFAULT/dictionary` (or
  equivalent briefing content asserts) with non-empty Sortie and player Task text

### Requirement: Non-sunny weather covered by regression
The test suite SHALL regress compile output for at least one non-`sunny_clear` weather
example (dawn and/or marginal VFR) via golden fixtures or equivalent structural contracts
so weather mappings cannot silently regress.

#### Scenario: Dawn or marginal golden/contract
- **WHEN** the dawn or marginal VFR example is compiled under the test harness
- **THEN** the suite MUST assert required members and weather-related contracts (or full
  golden match) for that example

### Requirement: Trigger sample structural coverage
The test suite SHALL assert that compiling the checked-in trigger sample produces a `.miz`
whose mission member includes expected native trigger predicates for the sample rule
(time-after and out-text). Full golden refresh of all combat fixtures is NOT required solely
for empty-trigger missions.

#### Scenario: Sample trig predicates present
- **WHEN** the free-flight trigger sample is compiled in tests
- **THEN** assertions MUST find time-after and out-text (or equivalent) markers in the
  mission member

### Requirement: Narrative CAP example is covered
The repository MUST include a checked-in CAP Spec that enables narrative (or documents
expansion) and tests MUST assert that after expansion the Spec validates and compiles
with non-empty native-trigger structure (zone and/or message / mission_end rules).

#### Scenario: Narrative CAP compile structure
- **WHEN** the narrative CAP example is expanded and compiled in tests
- **THEN** the resulting `.miz` mission tables MUST include trigger rules consistent with
  the expanded Spec (e.g. message and/or mission end actions)

### Requirement: Narrative intercept example is covered
The repository MUST include a checked-in intercept Spec with `narrative.enabled` and
tests MUST assert expansion validates and compiles with native trigger structure
(scramble message and/or mission_end).

#### Scenario: Narrative intercept compile structure
- **WHEN** the narrative intercept example is expanded and compiled in tests
- **THEN** the resulting `.miz` MUST include trigger rules consistent with the pack

### Requirement: Narrative escort example is covered
The repository MUST include a checked-in escort Spec with `narrative.enabled` and tests
MUST assert expansion validates and compiles with native trigger structure (messages
and/or mission_end).

#### Scenario: Narrative escort compile structure
- **WHEN** the narrative escort example is expanded and compiled in tests
- **THEN** the resulting `.miz` MUST include trigger rules consistent with the pack

### Requirement: Narrative ground-attack example is covered
The repository MUST include a checked-in ground_attack Spec with `narrative.enabled` and
tests MUST assert expansion validates and compiles with native trigger structure
(messages and/or mission_end, and target_dead / group-dead).

#### Scenario: Narrative ground-attack compile structure
- **WHEN** the narrative ground_attack example is expanded and compiled in tests
- **THEN** the resulting `.miz` MUST include trigger rules consistent with the pack

### Requirement: Radio late-activation example is covered
The repository MUST include a checked-in Spec that uses F10 radio items and late-activated
enemy (or target) groups, and tests MUST assert validation and compile emit radio-item and
activate-group structure (and late activation on the group where applicable).

#### Scenario: Radio late-activation compile structure
- **WHEN** the radio / late-activation example is compiled in tests
- **THEN** the resulting `.miz` MUST include radio-item and activate-group markers
  consistent with the Spec

### Requirement: Sound and numeric-flag example is covered
The repository MUST include a checked-in Spec that uses a `sound` action with a curated
`asset_id` and at least one numeric or timed flag rule (`flag_equals` / `flag_more` /
`flag_less` / `time_since_flag` and/or `inc_flag` / `set_flag_value`). Tests MUST assert
validation and compile emit sound-to-all (with embedded resource) and numeric flag
structure.

#### Scenario: Sound and flag compile structure
- **WHEN** the sound / numeric-flag example is compiled in tests
- **THEN** the resulting `.miz` MUST include sound-to-all and numeric flag markers
  consistent with the Spec

### Requirement: Group life less example is covered
The repository MUST include a checked-in Spec that uses a `group_life_less` condition
(enemy or target index + percent) with at least one observable action (e.g. `message`).
Tests MUST assert validation and compile emit group-life-less structure for the referenced
placed group.

#### Scenario: Group life less compile structure
- **WHEN** the group-life-less example is compiled in tests
- **THEN** the resulting `.miz` MUST include group-life-less markers consistent with the
  Spec

### Requirement: Mark and smoke example is covered
The repository MUST include a checked-in Spec that uses `mark` and/or `smoke` actions
referencing a Spec zone, with at least one observable companion action (e.g. `message`).
Tests MUST assert validation and compile emit mark-to-all and/or smoke-marker structure
for the referenced zone.

#### Scenario: Mark/smoke compile structure
- **WHEN** the mark/smoke example is compiled in tests
- **THEN** the resulting `.miz` MUST include mark-to-all and/or smoke-marker predicates
  consistent with the Spec

### Requirement: Altitude and speed gate example is covered
The repository MUST include a checked-in Spec that uses at least one of
`unit_altitude_higher`, `unit_altitude_lower`, `unit_speed_higher`, or
`unit_speed_lower`, with at least one observable companion action (e.g. `message`).
Tests MUST assert validation and compile emit of the corresponding unit-altitude and/or
unit-speed predicates for the player unit.

#### Scenario: Gate compile structure
- **WHEN** the altitude/speed gate example is compiled in tests
- **THEN** the resulting `.miz` MUST include unit-altitude and/or unit-speed predicates
  consistent with the Spec

### Requirement: Mission behaviour and inspiration options are covered
Tests MUST assert that after catalog sync (or registry load), packaged
`mission_behaviour` planning options include the v1 altitude/speed gate card, packaged
`mission_inspiration` includes at least one pattern card, and `list_mission_options`
exposes both families. Prompt or schema-note tests MAY assert that agent guidance mentions
`mission_behaviour` and inspiration/research/local-campaign creativity aids. Tests MUST
cover the local campaign index against a hermetic fixture tree.

#### Scenario: Behaviour options present in tool output
- **WHEN** tests call `list_mission_options` after sync
- **THEN** the result MUST include a `mission_behaviour` option for altitude/speed gates

#### Scenario: Inspiration options present in tool output
- **WHEN** tests call `list_mission_options` after sync
- **THEN** the result MUST include at least one `mission_inspiration` option

#### Scenario: Local campaign index fixture
- **WHEN** tests call the installed-campaigns tool against a fixture campaigns tree
- **THEN** the result MUST list the fixture campaign, at least one mission filename, and
  Doc filename(s) when the fixture includes a `Doc/` folder

### Requirement: Creative decision memory is hermetically tested
Tests MUST cover recording generation detail with a `creative` object and the bias
helper’s prefer/avoid behaviour on fixture history/feedback without a live LLM or DCS
install.

#### Scenario: Detail round-trip in tests
- **WHEN** tests record a generation with creative behaviours in detail
- **THEN** listed history MUST include those behaviours

#### Scenario: Bias helper unit test
- **WHEN** tests feed a high-scored generation with known behaviours into the bias helper
- **THEN** prefer MUST be non-empty for those behaviours
