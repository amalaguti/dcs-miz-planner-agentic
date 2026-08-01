## ADDED Requirements

### Requirement: CAP mission type
The Mission Spec SHALL support `mission_type` value `cap` in addition to `free_flight` and
`intercept`. A CAP Spec MUST include a nested `cap` object describing the patrol station
(airfield-relative bearing and distance), altitude, orbit pattern, and engagement rules.
Free-flight Specs MUST continue to require empty combat extensions; intercept Specs MUST
continue to require non-empty `enemies` and intercept objectives.

#### Scenario: CAP Spec with Manston patrol accepted
- **WHEN** a Mission Spec sets `mission_type` to `cap`, player `SpitfireLFMkIX` at Manston,
  a valid `cap` block (bearing, distance, altitude, pattern, engagement), and a `patrol`
  objective
- **THEN** the Spec MUST load as structurally valid for CAP compilation

#### Scenario: CAP block forbidden on free flight
- **WHEN** a Mission Spec sets `mission_type` to `free_flight` and includes a non-empty `cap`
  object
- **THEN** loading or validation MUST fail with a clear error

### Requirement: CAP patrol station is airfield-relative
The CAP `cap` block SHALL express the patrol station as a bearing in degrees and a positive
distance in kilometres relative to the player departure airfield. The Spec MUST NOT require
raw Channel map x/y or invented WGS84 coordinates from authors or agents.

#### Scenario: Bearing and distance required
- **WHEN** a CAP Spec omits `bearing_deg` or `distance_km`, or sets a non-positive distance
- **THEN** loading MUST fail with a structural validation error identifying the `cap` fields

### Requirement: CAP engagement rules
The CAP `cap` block SHALL include an `engagement` field with a closed set of values that map
to DCS group ROE (`weapons_free`, `open_fire`, `return_fire`, `weapons_hold`). Unknown
engagement values MUST be rejected.

#### Scenario: weapons_free accepted
- **WHEN** a CAP Spec sets `cap.engagement` to `weapons_free`
- **THEN** the Spec MUST be structurally valid (subject to other CAP rules)

#### Scenario: Unknown engagement rejected
- **WHEN** a CAP Spec sets `cap.engagement` to an undeclared value
- **THEN** loading MUST fail with a validation error

### Requirement: CAP orbit pattern and optional duration
The CAP `cap` block SHALL include `pattern` of `circle` or `race_track` and MAY include
optional `duration_min` (≥ 1). Unsupported pattern values MUST be rejected.

#### Scenario: Circle pattern accepted
- **WHEN** a CAP Spec sets `pattern` to `circle` with a positive `altitude_m`
- **THEN** the Spec MUST be structurally valid (subject to other CAP rules)

### Requirement: CAP objectives and optional enemies
A CAP Mission Spec MUST declare a non-empty `objectives` list including objective type
`patrol`. CAP Specs MAY include empty or non-empty `enemies` (empty = pure patrol).
Non-empty `triggers` MUST still be rejected. Objective type `patrol` MUST be rejected on
non-CAP mission types unless a later change explicitly allows it.

#### Scenario: Pure patrol CAP accepted
- **WHEN** a CAP Spec has `objectives` containing `patrol` and empty `enemies`
- **THEN** validation MUST accept the Spec (subject to other CAP and registry rules)

#### Scenario: CAP with light opposition accepted
- **WHEN** a CAP Spec includes a non-empty `enemies` list with known Channel aircraft ids and
  a `patrol` objective
- **THEN** the Spec MUST load as structurally valid for CAP compilation

#### Scenario: Non-empty triggers still refused for CAP
- **WHEN** a CAP Spec sets a non-empty `triggers` list
- **THEN** validation MUST fail stating triggers are not supported yet

### Requirement: Checked-in CAP example Spec
The repository SHALL include a checked-in example Mission Spec for a Manston Channel CAP
(player Spitfire, airfield-relative station, engagement rules) usable as validate and
compile input under schema_version `"1"`.

#### Scenario: Example present
- **WHEN** a developer clones the repository
- **THEN** a CAP example Spec MUST be present and loadable under schema_version `"1"`

## MODIFIED Requirements

### Requirement: Reserved extension points for future combat and triggers
The Mission Spec MAY include optional top-level keys `enemies`, `objectives`, and `triggers`.
For free-flight missions those keys MUST be absent or empty. For intercept missions, `enemies`
and `objectives` MUST be non-empty per intercept rules. For CAP missions, `objectives` MUST
be non-empty per CAP rules and `enemies` MAY be empty or non-empty; CAP Specs MUST also
include the nested `cap` block. `triggers` MUST remain empty until a later change implements
the trigger model. The system MUST NOT silently drop unsupported non-empty values.

#### Scenario: Free flight with absent extensions compiles
- **WHEN** a free-flight Mission Spec omits `enemies`, `objectives`, and `triggers`
- **THEN** the Spec SHALL be structurally valid and the compiler MUST proceed as for free flight

#### Scenario: Free flight refuses non-empty enemies
- **WHEN** a free-flight Mission Spec sets `enemies` to a non-empty value
- **THEN** the system MUST refuse load or validation with a clear error that free_flight
  requires empty combat extensions
