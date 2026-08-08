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

### Requirement: Weather preset SoT parity
The test suite SHALL assert that Mission Spec weather preset ids are aligned across the
`WeatherPreset` enum, Channel `weather_presets.yaml` (registry), `planning_options`
weather family ids, and the presets explicitly handled by the compiler weather apply
path. The sets MUST be equal (no enum-only, YAML-only, planning-only, or
compiler-orphan ids). Ordinary pytest MUST run this check hermetically without a DCS
install.

#### Scenario: Weather id sets match
- **WHEN** the weather SoT parity test runs
- **THEN** enum, registry YAML, planning weather options, and compiler-handled preset
  ids MUST be the same non-empty set

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
enemy (or target) groups, and MUST include a hermetic structural golden fixture for that
Spec’s compile path (required zip members, theatre, normalized `mission`, dictionary, and
`meta.json` contracts). Tests MUST compile with an injected Channel inventory and match
that golden. Ordinary pytest MUST NOT rewrite the fixture; refresh MUST be explicit.
Contracts MUST include radio-item, activate-group, and late-activation markers consistent
with the Spec.

#### Scenario: Radio late-activation compile matches golden
- **WHEN** the radio / late-activation example is compiled under the golden harness
- **THEN** the test MUST pass if and only if output matches the checked-in structural
  golden (including radio-item, activate-group, and late-activation contracts)


### Requirement: Sound and numeric-flag example is covered
The repository MUST include a checked-in Spec that uses a `sound` action with a curated
`asset_id` and at least one numeric or timed flag rule (`flag_equals` / `flag_more` /
`flag_less` / `time_since_flag` and/or `inc_flag` / `set_flag_value`), and MUST include a
hermetic structural golden fixture for that Spec’s compile path. Tests MUST compile with
injected Channel inventory and match that golden. Ordinary pytest MUST NOT rewrite the
fixture; refresh MUST be explicit. Contracts MUST include sound-to-all and numeric/timed
flag markers consistent with the Spec.

#### Scenario: Sound and flag compile matches golden
- **WHEN** the sound / numeric-flag example is compiled under the golden harness
- **THEN** the test MUST pass if and only if output matches the checked-in structural
  golden (including sound-to-all and numeric/timed flag contracts)


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
referencing a Spec zone, with at least one observable companion action (e.g. `message`),
and MUST include a hermetic structural golden fixture for that Spec’s compile path. Tests
MUST compile with injected Channel inventory and match that golden. Ordinary pytest MUST
NOT rewrite the fixture; refresh MUST be explicit. Contracts MUST include mark-to-all
and/or smoke-marker markers consistent with the Spec.

#### Scenario: Mark/smoke compile matches golden
- **WHEN** the mark/smoke example is compiled under the golden harness
- **THEN** the test MUST pass if and only if output matches the checked-in structural
  golden (including mark-to-all and/or smoke-marker contracts)


### Requirement: Altitude and speed gate example is covered
The repository MUST include a checked-in Spec that uses at least one of
`unit_altitude_higher`, `unit_altitude_lower`, `unit_speed_higher`, or
`unit_speed_lower`, with at least one observable companion action (e.g. `message`), and
MUST include a hermetic structural golden fixture for that Spec’s compile path. Tests MUST
compile with injected Channel inventory and match that golden. Ordinary pytest MUST NOT
rewrite the fixture; refresh MUST be explicit. Contracts MUST include the corresponding
unit-altitude and/or unit-speed predicates for the player unit.

#### Scenario: Gate compile matches golden
- **WHEN** the altitude/speed gate example is compiled under the golden harness
- **THEN** the test MUST pass if and only if output matches the checked-in structural
  golden (including unit-altitude and/or unit-speed contracts)


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

### Requirement: Weather invent tests pin seeds
Hermetic weather invent / compile tests that assert exact weather emit MUST set
an explicit `weather_opts.seed`. SoT parity for pattern ids MUST remain green
when invent metadata (gallery families) is added.

#### Scenario: Invent determinism test
- **WHEN** the weather invent test suite runs
- **THEN** at least one test MUST prove same seed → same snapshot and different
  seeds → differing within-family result for a gallery pattern

### Requirement: Golden fixture for player flight
The repository SHALL include a golden / structural fixture covering a multi-unit player
flight (at least size 2 with `role: lead`) that asserts group size and Player skill on the
lead unit after compile.

#### Scenario: Lead pair golden
- **WHEN** the golden suite compiles the checked-in player-flight example Spec
- **THEN** asserts MUST confirm the player group has the Spec size and the lead unit
  skill is `Player`

### Requirement: Structural asserts for wingman Follow
Tests SHALL assert that a wingman+join_up compile emits Follow (or equivalent ME
follow task wiring) tied to the AI lead and that free-flight lead has an outbound
waypoint.

#### Scenario: Wingman join-up golden smoke
- **WHEN** the suite compiles the wingman join-up example
- **THEN** asserts MUST find Follow/groupId linkage and lead outbound content

### Requirement: Structural asserts for Failures table
Tests SHALL assert that a Spec with a curated failure compiles to mission content
containing the failure id and an enabled Failures panel table row (not
`a_set_failure`).

#### Scenario: Failure example golden smoke
- **WHEN** the suite compiles the checked-in failures example
- **THEN** asserts MUST find the failure id and enabled Failures table wiring

### Requirement: Structural asserts for section orders
Tests SHALL assert that a Spec with curated `player.flight.orders` compiles to
mission content containing radio-item / section-order wiring and does not invent
Lua for this feature.

#### Scenario: Orders example golden smoke
- **WHEN** the suite compiles the checked-in section-orders example
- **THEN** asserts MUST find radio / order flag wiring for a selected order id

### Requirement: Showers example or METAR contract coverage
The test suite SHALL cover `showers_scattered` and synthetic METAR hermetically:
either a checked-in example Spec compiled under the harness with weather-table
and briefing-substring contracts, or focused unit/contract tests that assert
(1) invent/compile gallery id ∈ showers family and (2) brief METAR contains the
fixed station id and simulated marker. Ordinary pytest MUST NOT require network
meteo.

#### Scenario: Showers or METAR contract passes offline
- **WHEN** the showers / METAR contract tests run in CI
- **THEN** they MUST pass without live METAR APIs and MUST fail if the gallery
  family or METAR markers regress

### Requirement: Structural asserts for discipline
Tests SHALL assert that a Spec with `player.flight.discipline` armed compiles to
mission content containing moving-zone / outside-zone (or equivalent) wiring and
does not invent Lua for this feature.

#### Scenario: Discipline example golden smoke
- **WHEN** the suite compiles the checked-in discipline example
- **THEN** asserts MUST find outside-moving-zone (or documented equivalent) wiring
  and a soft-warn message path

### Requirement: Recon golden fixture
The test suite SHALL include a structural golden (or compile asserts) for a checked-in
recon example that verifies Reconnaissance task presence, AOI zone, absence of bomb
CLSIDs, and find-beat messaging/trigger text. Contact unit types MUST be asserted when the
example includes `targets`.

#### Scenario: Recon golden green
- **WHEN** the recon golden / compile test runs in CI
- **THEN** it MUST pass against the checked-in example Spec

### Requirement: Surfaced U-boat recon example
The repository SHALL include a checked-in Channel `mission_type: recon` Spec that places
one or more opposing-coalition `Uboat_VIIC` contacts near a mid-Channel water AOI
(airfield-relative geometry that validates as sea domain), with no `player.payload`, and
a `recon_area` objective. The compiled `.miz` MUST include Reconnaissance tasking, the
recon AOI find beat, and ship-group contact(s) of type `Uboat_VIIC` without Bombing
tasking.

#### Scenario: U-boat recon Spec validates and compiles
- **WHEN** the checked-in U-boat recon example is validated and compiled
- **THEN** validation MUST succeed and the `.miz` MUST contain `Uboat_VIIC` and
  Reconnaissance / AOI find wiring without bomb CLSIDs

### Requirement: Surfaced U-boat hunt (GA) example
The repository SHALL include a checked-in Channel `mission_type: ground_attack` Spec that
targets one or more opposing-coalition `Uboat_VIIC` units on mid-Channel (or other
validated sea) geometry with a named Spitfire bomb payload and `attack_ground` objective.
The compiled `.miz` MUST include GroundAttack / bomb loadout and `Uboat_VIIC` ship group(s).

#### Scenario: U-boat hunt Spec validates and compiles
- **WHEN** the checked-in U-boat hunt example is validated and compiled
- **THEN** validation MUST succeed and the `.miz` MUST contain `Uboat_VIIC` and bomb
  CLSID(s)

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

### Requirement: Examples cover convoy AAA and sea AI options
The repository SHALL include or update checked-in examples that demonstrate
(1) soft-vehicle convoy with transit-style AI / move_formation, (2) AAA or
flak with alert-style AI where practical, and (3) U-boat or sea craft with
roe/alarm. Compile asserts MUST verify option and/or PointAction evidence in
the `.miz`.

#### Scenario: Convoy AI example green
- **WHEN** the convoy AI example is validated and compiled in CI
- **THEN** tests MUST pass and assert AI/move evidence in the `.miz`

#### Scenario: Sea AI example green
- **WHEN** the sea AI example is validated and compiled in CI
- **THEN** tests MUST pass and assert ROE/Alarm (or documented) evidence in the `.miz`

### Requirement: Strike unit catalog covered by tests
Hermetic tests SHALL assert that catalog sync populates strike units and that
`list_strike_targets` filters work offline without a live DCS install.

#### Scenario: Catalog strike unit tests green
- **WHEN** catalog / tool tests run in CI
- **THEN** they MUST pass and fail if Uboat sea membership or tool filters regress

### Requirement: Target invent heuristics covered by tests
Hermetic tests SHALL assert that packaged planning-option invent heuristics
(preferred motion / AI preset for soft, AAA, sea under way, harbour) remain
present after catalog sync, and that invent prompts or Spec schema notes
mention the cue mapping.

#### Scenario: Heuristic meta and prompt tests green
- **WHEN** catalog / agent invent tests run in CI
- **THEN** they MUST pass and fail if preferred_* meta or cue-table guidance
  regresses

### Requirement: Channel geometry invent covered by tests
Hermetic tests SHALL assert channel_place geometry recipes after catalog sync
and that domain-mismatch repair nudges include geometry guidance.

#### Scenario: Place recipe and repair tests green
- **WHEN** catalog / agent tests run in CI
- **THEN** they MUST pass and fail if inland/mid-Channel recipes or repair
  geometry text regress

### Requirement: Path and harbour harden covered by tests
Hermetic tests SHALL assert french_coast path_point_deltas, harbour sea-only
guidance text, path-domain repair YAML snippet, and host land-path clamp
behaviour (when implemented).

#### Scenario: Path harbour harden tests green
- **WHEN** catalog / agent / validation tests run in CI
- **THEN** they MUST pass and fail if path deltas, harbour sea guidance, repair
  path example, or clamp behaviour regresses

### Requirement: Promote checklist covered by tests
Hermetic tests SHALL assert that the theatre/target promote checklist file
exists and contains theatre-slice and target-unit section headings (and the
non-goals against ME scrape / auto-promote).

#### Scenario: Checklist presence test green
- **WHEN** docs / process tests run in CI
- **THEN** they MUST fail if the checklist file or required sections are removed

### Requirement: Expanded shelf covered by examples and tests
Hermetic tests SHALL assert new registry ids, class shelf membership, AAA AI
class for new flak ids, and at least one example Spec using a new AAA unit and
one using a new sea unit compile/validate.

#### Scenario: Shelf expand tests green
- **WHEN** registry / catalog / target AI / example tests run in CI
- **THEN** they MUST pass and fail if promoted ids or class lists regress

### Requirement: Halftrack GA example compiles
Repository SHALL include a Manston ground_attack example Spec that uses a
packaged halftrack unit on path motion with convoy_transit, and that example
MUST validate and compile under Channel inventory.

#### Scenario: Halftrack example validates and compiles
- **WHEN** examples/manston_ground_attack_halftracks.yaml is validated and
  compiled with Channel inventory
- **THEN** validation MUST succeed and a .miz file MUST be produced
