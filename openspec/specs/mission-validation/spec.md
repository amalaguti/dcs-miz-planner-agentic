# Mission Validation

## Purpose

Shared structural, DCS-exists, and free-flight semantic checks for Mission Specs.
Used by the CLI (`dcs-miz validate`) and the compiler so both surfaces share one rule set.

## Requirements

### Requirement: Shared Mission Spec validation API
The system SHALL expose a Python validation API that accepts a loaded free-flight `MissionSpec`
and returns a structured result indicating success or one or more errors. Each error MUST include
a stable machine-oriented code, a human-readable message, and a field path when applicable.
Independent checks SHOULD be reported together rather than stopping at the first failure when
practical.

#### Scenario: Valid Manston free-flight passes
- **WHEN** the checked-in Manston cold free-flight Mission Spec is loaded and validated against
  the Channel registry and a local inventory that reports `TheChannel` as available and
  planner-supported
- **THEN** the validation result MUST indicate success with no errors

#### Scenario: Unknown airfield is reported clearly
- **WHEN** a Mission Spec names an airfield absent from the Channel registry
- **THEN** validation MUST fail with an error that identifies the airfield field and lists known
  airfields (or equivalent clear diagnostics)

#### Scenario: Multiple independent errors collected
- **WHEN** a Mission Spec uses both an unknown aircraft id and an unknown weather preset
- **THEN** the validation result MUST include errors for both problems in one response

### Requirement: DCS-exists checks use registry and install inventory
Validation SHALL verify that theatre, aircraft, weather preset, and airfield identifiers exist in
the packaged Channel registry, and that the Spec theatre is both planner-supported and currently
`available` in the user-local install inventory (cached SQLite unless the caller supplies a test
inventory). Validation MUST NOT invent DCS identifiers and MUST NOT execute DCS Lua.

#### Scenario: Theatre not in registry
- **WHEN** a Mission Spec sets theatre to an id absent from the packaged registry
- **THEN** validation MUST fail with a clear unsupported-theatre error

#### Scenario: Theatre supported but not locally available
- **WHEN** the registry supports `TheChannel` but the install inventory does not report it as
  `available`
- **THEN** validation MUST fail and MUST NOT treat the Spec as compilable for that installation

#### Scenario: Empty or missing install inventory
- **WHEN** no usable install inventory is available (no DCS roots / empty cache that cannot be
  populated in the validate call context)
- **THEN** validation MUST fail theatre-availability checks with a diagnostic that points the user
  at refreshing or selecting a DCS install root

### Requirement: Free-flight semantic rules
For schema_version `"1"` free-flight Specs, validation SHALL enforce that reserved extension
points remain empty and that only planner-supported free-flight combinations are accepted (exact
checks limited to what the packaged registry and supported start/weather enums already define).

#### Scenario: Non-empty enemies refused
- **WHEN** a Mission Spec includes a non-empty `enemies` list
- **THEN** validation MUST fail with an error that combat extensions are not supported yet

### Requirement: Validate CLI
The system SHALL provide a `dcs-miz validate` command that loads a Mission Spec YAML and runs the
shared validation engine without compiling a `.miz`. It MUST support human-readable output and a
JSON mode for machine consumers, and MUST use a non-zero exit code on load or validation failure.

#### Scenario: Validate Manston example succeeds
- **WHEN** a user runs `dcs-miz validate` on the checked-in Manston free-flight Spec with a usable
  Channel-available inventory
- **THEN** the command MUST exit successfully and report that the Spec is valid

#### Scenario: Validate unknown aircraft fails
- **WHEN** a user validates a Spec whose player aircraft is not in the Channel registry
- **THEN** the command MUST exit non-zero and print a clear aircraft-related error

### Requirement: Validate intercept Specs
The shared validation engine SHALL accept intercept Mission Specs that satisfy intercept
schema rules and registry/install checks, including non-empty `enemies` with known aircraft
ids. It MUST still reject free-flight Specs with non-empty extension points and MUST reject
non-empty `triggers` for all schema_version `"1"` types covered by this change.

#### Scenario: Valid intercept example passes validate
- **WHEN** the checked-in intercept example is validated with Channel available inventory
- **THEN** `validate_mission_spec` / `dcs-miz validate` MUST succeed

#### Scenario: Unknown enemy aircraft fails
- **WHEN** an intercept Spec names an enemy aircraft absent from the Channel registry
- **THEN** validation MUST fail with an unknown-aircraft (or equivalent) error identifying
  the enemies path

### Requirement: Validate CAP Specs
The shared validation engine SHALL accept CAP Mission Specs that satisfy CAP schema rules
and registry/install checks, including a valid `cap` block, `patrol` objective, and — when
present — known enemy aircraft ids. It MUST still reject free-flight Specs with non-empty
extension points, MUST reject CAP Specs missing required `cap` fields or using unknown
engagement/pattern values, and MUST reject non-empty `triggers` for all schema_version `"1"`
types covered by this change.

#### Scenario: Valid CAP example passes validate
- **WHEN** the checked-in CAP example is validated with Channel available inventory
- **THEN** `validate_mission_spec` / `dcs-miz validate` MUST succeed

#### Scenario: Unknown CAP enemy aircraft fails
- **WHEN** a CAP Spec names an enemy aircraft absent from the Channel registry
- **THEN** validation MUST fail with an unknown-aircraft (or equivalent) error identifying
  the enemies path

#### Scenario: Invalid engagement fails
- **WHEN** a CAP Spec sets an engagement value outside the closed set
- **THEN** validation or Spec load MUST fail before compile
