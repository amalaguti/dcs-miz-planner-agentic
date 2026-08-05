## ADDED Requirements

### Requirement: Late activation activate-group graph
Validation MUST enforce a bidirectional graph between Spec `late_activation` and
trigger actions: every enemy or target with `late_activation: true` MUST be referenced by
at least one `activate_group` action (matching `enemy_index` or `target_index`); every
`activate_group` and `deactivate_group` MUST reference a group whose Spec
`late_activation` is true. Out-of-range index checks remain. Validation MUST fail with a
stable error code when either direction is violated.

#### Scenario: Late enemy without activate fails
- **WHEN** an enemy has `late_activation: true` and no trigger action activates that
  `enemy_index`
- **THEN** validation MUST fail with a clear late-activation / activate-graph error

#### Scenario: Activate on non-late group fails
- **WHEN** an `activate_group` references an enemy or target with `late_activation` false
  or omitted
- **THEN** validation MUST fail stating the group is not late-activated

#### Scenario: Radio late-activation example passes
- **WHEN** the checked-in Manston dawn intercept radio Spec is validated
- **THEN** validation MUST succeed for the late-activation / activate-graph rules

### Requirement: Message delay_s unsupported until implemented
Validation MUST reject any message action with `delay_s` greater than zero. Authors MUST
express timing via trigger `when` conditions (e.g. `time_more`) until delayed message emit
is implemented. `delay_s` of zero or omitted MUST remain accepted.

#### Scenario: Non-zero delay_s fails
- **WHEN** a trigger action is `type: message` with `delay_s: 5`
- **THEN** validation MUST fail stating delayed messages are unsupported

#### Scenario: Zero delay_s accepted
- **WHEN** a message action omits `delay_s` or sets `delay_s: 0`
- **THEN** validation MUST NOT fail solely for delay

### Requirement: Country and skill allowlists
Validation MUST reject unknown `country` and `skill` values on player, enemies, targets,
and escort package entries using the same allowlists the Channel compiler accepts
(curated countries including at least `UK` and `ThirdReich`; skill names matching known
PyDCS skill identifiers). Errors MUST include a stable code and a hint when a common
mistake is detected (e.g. `Germany` on red → use `ThirdReich`).

#### Scenario: Unknown country fails at validate
- **WHEN** a Spec sets `player.country` or an enemy `country` to an unsupported id
- **THEN** validation MUST fail before compile with a country-related error

#### Scenario: Unknown skill fails at validate
- **WHEN** a Spec sets a unit `skill` to a name not in the skill allowlist
- **THEN** validation MUST fail with a skill-related error

### Requirement: Intercept and CAP enemies must oppose player
For intercept and CAP Mission Specs, validation MUST require every enemy flight’s
`coalition` to be the opposing coalition of `player.coalition` (same opposing rule as
escort enemies). Free-flight remains without enemies.

#### Scenario: Blue bandit on intercept fails
- **WHEN** an intercept Spec places an enemy with the same coalition as the player
- **THEN** validation MUST fail stating enemies must be opposing coalition

#### Scenario: Red enemy on blue intercept passes coalition rule
- **WHEN** an intercept Spec places red enemies against a blue player (subject to other
  checks)
- **THEN** validation MUST NOT fail solely for enemy coalition

## MODIFIED Requirements

### Requirement: Validate typed triggers and zones
Validation of typed `zones` and `triggers` MUST continue to enforce existing
mission-triggers structural rules (zone refs, flag ids, index bounds, action/condition
vocabularies) and MUST additionally enforce the late-activation activate-group graph and
unsupported `message.delay_s` rules defined in this change.

#### Scenario: Valid trigger graph still passes
- **WHEN** a Spec uses supported conditions/actions with consistent zone and index refs
  and satisfies late-act / delay rules
- **THEN** validation MUST succeed for those trigger checks
