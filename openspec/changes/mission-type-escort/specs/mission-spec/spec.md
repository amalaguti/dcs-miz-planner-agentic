## ADDED Requirements

### Requirement: Escort mission type
The Mission Spec SHALL support `mission_type` value `escort` in addition to
`free_flight`, `intercept`, `cap`, and `ground_attack`. An escort Spec MUST include a nested
`escort` object (airfield-relative package destination, altitude, and engagement), a
non-empty `package` list of friendly flights, and a non-empty `objectives` list including
`escort_package`. Air `enemies` MAY be empty or non-empty (optional bounce). Ground
`targets`, `strike`, and `player.payload` MUST be absent or empty/unsupported for escort.
Free-flight, intercept, CAP, and ground-attack rules MUST remain unchanged. The `escort`
block MUST be forbidden on non-escort types.

#### Scenario: Manston escort Spec accepted
- **WHEN** a Mission Spec sets `mission_type` to `escort`, player `SpitfireLFMkIX` at
  Manston, a valid `escort` block, non-empty same-coalition `package`, and an
  `escort_package` objective
- **THEN** the Spec MUST load as structurally valid for escort compilation

#### Scenario: Escort block forbidden on free flight
- **WHEN** a Mission Spec sets `mission_type` to `free_flight` and includes an `escort`
  object
- **THEN** loading or validation MUST fail with a clear error

### Requirement: Escort destination is airfield-relative
The `escort` block SHALL express the package destination as `bearing_deg` (0–360) and a
positive `distance_km` relative to the player departure airfield, plus a positive
`altitude_m` for cruise, and an `engagement` value from the closed CAP engagement set. The
Spec MUST NOT require raw Channel map x/y or invented WGS84 coordinates.

#### Scenario: Bearing and distance required
- **WHEN** an escort Spec omits `bearing_deg` or `distance_km`, or sets a non-positive
  distance or altitude
- **THEN** loading MUST fail with a structural validation error identifying the `escort`
  fields

#### Scenario: Engagement required
- **WHEN** an escort Spec omits `engagement` or sets an undeclared engagement value
- **THEN** loading MUST fail with a structural validation error

### Requirement: Friendly package collection
An escort Mission Spec MUST declare a non-empty `package` list. Each package entry MUST
include an exact DCS aircraft type id and a positive count. Unknown aircraft ids MUST be
rejected by validation against the Channel registry. Every package entry's coalition MUST
equal `player.coalition` (friendly package only).

#### Scenario: Mosquito package accepted
- **WHEN** an escort Spec lists known Channel aircraft ids (e.g. `MosquitoFBMkVI`) with
  valid counts and the same coalition as the player
- **THEN** the Spec MUST load as structurally valid for compilation

#### Scenario: Unknown package aircraft rejected
- **WHEN** an escort Spec names a package aircraft absent from the Channel registry
- **THEN** validation MUST fail identifying the unknown aircraft

#### Scenario: Enemy coalition package refused
- **WHEN** an escort Spec includes a package entry whose coalition opposes
  `player.coalition`
- **THEN** loading or validation MUST fail stating the package must be friendly
  (same coalition)

### Requirement: Optional escort bounce enemies
An escort Spec MAY include empty or non-empty `enemies`. When present, enemy aircraft MUST
be known Channel registry ids and MUST belong to the coalition opposing the player.

#### Scenario: Clean escort accepted
- **WHEN** an escort Spec has `escort_package` objective and empty `enemies`
- **THEN** validation MUST accept the Spec (subject to other escort and registry rules)

#### Scenario: Escort with bounce accepted
- **WHEN** an escort Spec includes a non-empty `enemies` list with known opposing aircraft
- **THEN** the Spec MUST load as structurally valid for escort compilation

### Requirement: Escort objective
An escort Mission Spec MUST declare a non-empty `objectives` list including objective type
`escort_package`. Non-empty `triggers` MUST still be rejected. Objective type
`escort_package` MUST be rejected on non-escort mission types unless a later change
explicitly allows it.

#### Scenario: escort_package objective accepted
- **WHEN** an escort Spec includes `escort_package` and empty `triggers`
- **THEN** validation MUST accept the Spec (subject to other escort and registry rules)

#### Scenario: Non-empty triggers still refused
- **WHEN** an escort Spec sets a non-empty `triggers` list
- **THEN** validation MUST fail stating triggers are not supported yet

### Requirement: Checked-in escort example Spec
The repository SHALL include a checked-in example Mission Spec for a Manston Channel escort
(Spitfire escorting a friendly package to an airfield-relative destination, optional bounce)
usable as validate and compile input under schema_version `"1"`.

#### Scenario: Example present
- **WHEN** a developer clones the repository
- **THEN** an escort example Spec MUST be present and loadable under schema_version `"1"`

## MODIFIED Requirements

### Requirement: Reserved extension points for future combat and triggers
The Mission Spec MAY include optional top-level keys `enemies`, `objectives`, `triggers`,
`targets`, and `package`. For free-flight missions those combat keys MUST be absent or
empty. For intercept missions, `enemies` and `objectives` MUST be non-empty per intercept
rules. For CAP missions, `objectives` MUST be non-empty per CAP rules and `enemies` MAY be
empty or non-empty; CAP Specs MUST also include the nested `cap` block. For ground-attack
missions, `targets` and `objectives` MUST be non-empty per ground-attack rules, `enemies`
MUST be empty, and the nested `strike` block MUST be present. For escort missions,
`package` and `objectives` MUST be non-empty per escort rules, `enemies` MAY be empty or
non-empty, the nested `escort` block MUST be present, and `targets` / `strike` /
`player.payload` MUST be absent or unsupported. `triggers` MUST remain empty until a later
change implements the trigger model. The system MUST NOT silently drop unsupported
non-empty values.

#### Scenario: Free flight with absent extensions compiles
- **WHEN** a free-flight Mission Spec omits `enemies`, `objectives`, `triggers`,
  `targets`, and `package`
- **THEN** the Spec SHALL be structurally valid and the compiler MUST proceed as for free
  flight

#### Scenario: Free flight refuses non-empty enemies
- **WHEN** a free-flight Mission Spec sets `enemies` to a non-empty value
- **THEN** the system MUST refuse load or validation with a clear error that free_flight
  requires empty combat extensions

#### Scenario: Escort requires package and escort block
- **WHEN** an escort Mission Spec omits `package` or the nested `escort` block
- **THEN** loading or validation MUST fail with a clear error
