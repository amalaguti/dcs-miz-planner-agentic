## MODIFIED Requirements

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
