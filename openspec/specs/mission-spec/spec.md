# Mission Spec

## Purpose

The Mission Spec is the public contract between the planning layer (eventually an AI agent)
and the compiler. It is a declarative, backend-agnostic description of a mission that
contains no DCS Lua and no compiler types.

## Requirements

### Requirement: Schema version on Mission Spec
The Mission Spec SHALL include a `schema_version` field. For this change the required value MUST be `"1"`.

#### Scenario: Version 1 accepted
- **WHEN** a Mission Spec sets `schema_version` to `"1"` with an otherwise valid free-flight body
- **THEN** the Mission Spec SHALL be accepted as structurally valid

#### Scenario: Missing or unsupported version rejected
- **WHEN** a Mission Spec omits `schema_version` or sets it to a value other than `"1"`
- **THEN** loading the Mission Spec MUST fail with a clear structural validation error before compilation

### Requirement: Unknown fields rejected
The Mission Spec SHALL reject undeclared fields at every model level (no silent ignore of unknown keys).

#### Scenario: Typos fail fast
- **WHEN** a Mission Spec YAML includes an undeclared top-level or nested key
- **THEN** loading MUST fail with a validation error that identifies the unexpected field

### Requirement: Reserved extension points for future combat and triggers
The Mission Spec MAY include optional top-level keys `enemies`, `objectives`, and `triggers`.
For free-flight missions those keys MUST be absent or empty. For intercept missions, `enemies`
and `objectives` MUST be non-empty per intercept rules; `triggers` MUST remain empty until a
later change implements the trigger model. The system MUST NOT silently drop unsupported
non-empty values.

#### Scenario: Free flight with absent extensions compiles
- **WHEN** a free-flight Mission Spec omits `enemies`, `objectives`, and `triggers`
- **THEN** the Spec SHALL be structurally valid and the compiler MUST proceed as for free flight

#### Scenario: Free flight refuses non-empty enemies
- **WHEN** a free-flight Mission Spec sets `enemies` to a non-empty value
- **THEN** the system MUST refuse load or validation with a clear error that free_flight
  requires empty combat extensions

### Requirement: Free-flight Mission Spec schema
The system SHALL define a Mission Spec for free-flight missions that includes `schema_version`, theatre, date, start time, weather preset, and a single player aircraft placement.

#### Scenario: Manston cold free-flight example is representable
- **WHEN** an author provides a free-flight Mission Spec with `schema_version` `"1"` for Channel with player `SpitfireLFMkIX`, airfield `Manston`, start type cold parking, start time 09:00, and weather preset `sunny_clear`
- **THEN** the Mission Spec SHALL be accepted as structurally valid for compilation

### Requirement: Exact DCS identifiers in the Mission Spec
The Mission Spec SHALL use verified DCS identifiers for theatre and aircraft type and SHALL NOT invent alternate spellings.

#### Scenario: Theatre and aircraft ids
- **WHEN** a free-flight Mission Spec targets The Channel and Spitfire LF Mk IX
- **THEN** theatre MUST be `TheChannel` and player aircraft type MUST be `SpitfireLFMkIX`

### Requirement: Airfield referenced by name in the Mission Spec
The Mission Spec SHALL allow the player departure airfield to be specified by display name (e.g. `Manston`), with mapping to DCS `airdromeId` performed by the compiler layer.

#### Scenario: Manston by name
- **WHEN** the Mission Spec sets player airfield to `Manston`
- **THEN** the compiled mission MUST place the player at Manston (`airdromeId` 5)

### Requirement: Checked-in example Mission Spec
The repository SHALL include a checked-in example Mission Spec that encodes the Manston cold free-flight acceptance mission and includes `schema_version` `"1"`.

#### Scenario: Example file present
- **WHEN** a developer clones the repository
- **THEN** an example Mission Spec for Manston cold free flight MUST be present, include `schema_version` `"1"`, and be usable as compile input

### Requirement: Intercept mission type
The Mission Spec SHALL support `mission_type` value `intercept` in addition to `free_flight`.
An intercept Spec MUST include a non-empty `enemies` collection using verified DCS aircraft
ids and a positive count. Free-flight Specs MUST continue to require empty `enemies`,
`objectives`, and `triggers`.

#### Scenario: Intercept with Bf-109K-4 enemies accepted
- **WHEN** a Mission Spec sets `mission_type` to `intercept`, player `SpitfireLFMkIX` at
  Manston, and `enemies` containing at least one entry with aircraft `Bf-109K-4` and count ≥ 1
- **THEN** the Spec MUST load as structurally valid for intercept compilation

#### Scenario: Free flight still refuses enemies
- **WHEN** a Mission Spec sets `mission_type` to `free_flight` with a non-empty `enemies` list
- **THEN** loading or validation MUST fail with a clear not-supported / empty-extensions error

### Requirement: Minimal intercept objective
An intercept Mission Spec MUST declare a minimal objective indicating enemy interception
(structured field agreed in design). Unknown objective types MUST be rejected. Non-empty
`triggers` MUST still be rejected in this change.

#### Scenario: intercept_enemy objective accepted
- **WHEN** an intercept Spec includes the supported intercept objective shape and empty
  `triggers`
- **THEN** validation MUST accept the Spec (subject to other intercept rules)

#### Scenario: Non-empty triggers still refused
- **WHEN** an intercept Spec sets a non-empty `triggers` list
- **THEN** validation MUST fail stating triggers are not supported yet

### Requirement: Checked-in intercept example Spec
The repository SHALL include a checked-in example Mission Spec for the Manston dawn-style
intercept (early start time, Channel, Spitfire player, Bf-109K-4 enemies) usable as validate
and compile input.

#### Scenario: Example present
- **WHEN** a developer clones the repository
- **THEN** an intercept example Spec MUST be present and loadable under schema_version `"1"`
