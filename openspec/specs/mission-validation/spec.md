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
ids. It MUST still reject free-flight Specs with non-empty combat extension points. Typed
`triggers`/`zones` MUST be validated per mission-triggers rules (not blanket-rejected).

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
combat extension points, MUST reject CAP Specs missing required `cap` fields or using
unknown engagement/pattern values, and MUST validate typed `triggers`/`zones` per
mission-triggers rules (not blanket-reject non-empty triggers).

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

### Requirement: Validate ground-attack Specs
The shared validation engine SHALL accept ground-attack Mission Specs that satisfy
ground-attack schema rules and registry/install checks, including a valid `strike` block,
known `player.payload` for the player aircraft, known ground unit ids in `targets`, enemy
(opposing) coalition on every target, and an `attack_ground` objective. It MUST reject
unknown payloads or ground units, MUST reject same-coalition / friendly targets, MUST reject
non-empty air `enemies` on ground_attack, MUST reject `strike` / `player.payload` /
`attack_ground` on unsupported mission types, and MUST keep free-flight / intercept / CAP
validation behaviour unchanged.

#### Scenario: Valid ground-attack example passes validate
- **WHEN** the checked-in ground-attack example is validated with Channel available inventory
- **THEN** validation MUST succeed with no errors

#### Scenario: Unknown payload fails
- **WHEN** a ground-attack Spec sets `player.payload` to a name absent from the Channel
  payload registry
- **THEN** validation MUST fail with a clear error identifying the unknown payload

#### Scenario: Unknown ground unit fails
- **WHEN** a ground-attack Spec names a target unit absent from the Channel ground-unit
  registry
- **THEN** validation MUST fail with a clear error identifying the unknown unit

#### Scenario: Friendly target coalition fails
- **WHEN** a combat ground-attack Spec (`strike.practice` false/omitted) includes a target
  coalition matching `player.coalition`
- **THEN** validation MUST fail stating targets must be enemy (opposing coalition) only
  unless practice is set

#### Scenario: Practice same-coalition target passes
- **WHEN** a ground-attack Spec sets `strike.practice` true with same-coalition targets
- **THEN** validation MUST succeed for the coalition rule (subject to other checks)

### Requirement: Validate escort Specs
The shared validation engine SHALL accept escort Mission Specs that satisfy escort schema
rules and registry checks, including a valid `escort` block, non-empty same-coalition
`package` with known aircraft ids, `escort_package` objective, and — when present — known
opposing `enemies`. It MUST reject escort Specs with opposing-coalition package entries,
unknown package/enemy aircraft, missing required `escort` fields, misuse of
`strike`/`targets`/`payload` on escort. Typed `triggers`/`zones` MUST be validated per
mission-triggers rules (not blanket-rejected).

#### Scenario: Valid escort example passes validate
- **WHEN** the checked-in escort example is validated with Channel available inventory
- **THEN** `validate_mission_spec` / `dcs-miz validate` MUST succeed

#### Scenario: Unknown package aircraft fails
- **WHEN** an escort Spec names a package aircraft absent from the Channel registry
- **THEN** validation MUST fail with an unknown-aircraft (or equivalent) error identifying
  the package path

#### Scenario: Friendly package coalition mismatch fails
- **WHEN** an escort Spec includes a package entry whose coalition differs from
  `player.coalition`
- **THEN** validation or Spec load MUST fail before compile

### Requirement: Unknown weather still rejected; new presets accepted
Shared validation SHALL accept registered weather presets `dawn_clear` and
`marginal_vfr` and MUST continue to reject unknown weather ids with a clear error listing
known presets.

#### Scenario: Unknown weather fails
- **WHEN** a Spec uses a weather value not in the Channel registry
- **THEN** validation MUST fail with an unknown-weather style error

#### Scenario: Dawn clear validates
- **WHEN** a Spec uses `weather: dawn_clear` on Channel with known player assets
- **THEN** validation MUST succeed for weather

### Requirement: Randomized Specs use shared validation
A Spec produced by seeded randomization MUST be subject to the same shared validation
engine as any other Mission Spec before compile. The system MUST NOT provide a compile
path that skips validation solely because the Spec was randomized.

#### Scenario: Invalid randomized output is refused
- **WHEN** a randomized Spec would fail structural or semantic validation
- **THEN** validate/compile MUST report the failure and MUST NOT write a `.miz`

### Requirement: Validate typed triggers and zones
The shared validation engine SHALL accept Specs whose `triggers` and `zones` conform to the
mission-triggers vocabulary and reference rules, and MUST reject unknown types, duplicate
zone names, out-of-range `enemy_index`, and missing zone references. Blanket refusal of any
non-empty `triggers` list MUST NOT apply once the typed model is in force.

#### Scenario: Out-of-range enemy_index fails
- **WHEN** `unit_dead.enemy_index` is 0 but `enemies` is empty
- **THEN** validation MUST fail

#### Scenario: Well-formed trigger passes validate
- **WHEN** a Spec with `time_more` → `message` trigger is validated
- **THEN** `validate_mission_spec` MUST succeed for trigger rules
