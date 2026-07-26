## ADDED Requirements

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
The Mission Spec MAY include optional top-level keys `enemies`, `objectives`, and `triggers` as reserved extension points. For free-flight missions in this change, those keys MUST be absent or empty. Non-empty values MUST NOT be compiled; the system MUST fail with a clear “not supported yet” error.

#### Scenario: Free flight with absent extensions compiles
- **WHEN** a free-flight Mission Spec omits `enemies`, `objectives`, and `triggers`
- **THEN** the Spec SHALL be structurally valid and the compiler MUST proceed as for free flight

#### Scenario: Non-empty reserved extensions rejected for now
- **WHEN** a Mission Spec sets any of `enemies`, `objectives`, or `triggers` to a non-empty value
- **THEN** the system MUST refuse compilation (or refuse load) with an error stating that capability is not supported yet

## MODIFIED Requirements

### Requirement: Free-flight Mission Spec schema
The system SHALL define a Mission Spec for free-flight missions that includes `schema_version`, theatre, date, start time, weather preset, and a single player aircraft placement.

#### Scenario: Manston cold free-flight example is representable
- **WHEN** an author provides a free-flight Mission Spec with `schema_version` `"1"` for Channel with player `SpitfireLFMkIX`, airfield `Manston`, start type cold parking, start time 09:00, and weather preset `sunny_clear`
- **THEN** the Mission Spec SHALL be accepted as structurally valid for compilation

### Requirement: Checked-in example Mission Spec
The repository SHALL include a checked-in example Mission Spec that encodes the Manston cold free-flight acceptance mission and includes `schema_version` `"1"`.

#### Scenario: Example file present
- **WHEN** a developer clones the repository
- **THEN** an example Mission Spec for Manston cold free flight MUST be present, include `schema_version` `"1"`, and be usable as compile input
