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

### Requirement: Soft-warn missing known aircraft modules
When a usable DCS install root from the theatre inventory is present on disk, validation
MUST soft-warn (MUST NOT fail solely for this reason) if the Mission Spec references a
known Channel aircraft whose expected module folder is missing under that install’s
aircraft locations (at least `Mods/aircraft` and `CoreMods/WWII Units`, using the
committed Spec-id → folder map including known hyphen aliases). Warnings MUST use a
stable code (e.g. `aircraft_module_missing`) and MUST NOT write or promote module ids
into registry YAML. When no inventory roots exist on disk, validation MUST skip this
check (no spurious warnings).

#### Scenario: Missing Spitfire folder warns
- **WHEN** a free-flight Spec uses `SpitfireLFMkIX` and the inventory points at a DCS root
  on disk that lacks the Spitfire aircraft folder
- **THEN** validation MUST still be ok for this reason alone and MUST include an
  `aircraft_module_missing` warning for the player aircraft

#### Scenario: Present folder does not warn
- **WHEN** the same Spec is validated against a root that contains the Spitfire folder
- **THEN** validation MUST NOT emit `aircraft_module_missing` for that aircraft

#### Scenario: No roots on disk skips check
- **WHEN** inventory lists no DCS roots that exist as directories
- **THEN** validation MUST NOT emit aircraft-module-missing warnings

### Requirement: Registry theatres must have terrain bindings
Validation MUST fail when the Spec theatre is present in the packaged registry but has no
compiler terrain binding, with a stable code (e.g. `theatre_terrain_unbound`). This prevents
aspirational theatre ids from validating green before the compiler can place them.

#### Scenario: Bound Channel theatre passes binding check
- **WHEN** a Spec uses theatre `TheChannel` and the Channel binding exists
- **THEN** validation MUST NOT fail solely for terrain binding

#### Scenario: Unbound registry theatre fails
- **WHEN** validation sees a registry theatre id that is missing from the terrain binding map
- **THEN** validation MUST fail with `theatre_terrain_unbound` (or equivalent)

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
ids and opposing coalition vs the player. It MUST still reject free-flight Specs with
non-empty combat extension points. Typed `triggers`/`zones` MUST be validated per
mission-triggers rules (not blanket-rejected).

#### Scenario: Valid intercept example passes validate
- **WHEN** the checked-in intercept example is validated with Channel available inventory
- **THEN** `validate_mission_spec` / `dcs-miz validate` MUST succeed

#### Scenario: Unknown enemy aircraft fails
- **WHEN** an intercept Spec names an enemy aircraft absent from the Channel registry
- **THEN** validation MUST fail with an unknown-aircraft (or equivalent) error identifying
  the enemies path

#### Scenario: Blue bandit on intercept fails
- **WHEN** an intercept Spec places an enemy with the same coalition as the player
- **THEN** validation MUST fail stating enemies must be opposing coalition

### Requirement: Validate CAP Specs
The shared validation engine SHALL accept CAP Mission Specs that satisfy CAP schema rules
and registry/install checks, including a valid `cap` block, `patrol` objective, and — when
present — known enemy aircraft ids with opposing coalition vs the player. It MUST still
reject free-flight Specs with non-empty combat extension points, MUST reject CAP Specs
missing required `cap` fields or using unknown engagement/pattern values, and MUST validate
typed `triggers`/`zones` per mission-triggers rules (not blanket-reject non-empty triggers).

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
zone names, out-of-range `enemy_index` / `target_index`, missing zone references (including
`mark.zone` / `smoke.zone`), empty flag names, unknown `sound.asset_id` values, invalid
`smoke.color`, invalid `group_life_less` (bad index XOR, out-of-range index, or percent
outside 1–100), non-positive `altitude_m` / `speed_kmh` on altitude/speed gate
conditions, late-activation without a matching `activate_group` (and activate/deactivate on
non-late groups), and `message.delay_s` greater than zero. Blanket refusal of any non-empty
`triggers` list MUST NOT apply once the typed model is in force.

#### Scenario: Out-of-range enemy_index fails
- **WHEN** `unit_dead.enemy_index` is 0 but `enemies` is empty
- **THEN** validation MUST fail

#### Scenario: Well-formed trigger passes validate
- **WHEN** a Spec with `time_more` → `message` trigger is validated
- **THEN** `validate_mission_spec` MUST succeed for trigger rules

#### Scenario: Unknown sound asset rejected
- **WHEN** a Spec uses `sound` with an unregistered `asset_id`
- **THEN** `validate_mission_spec` MUST fail with a clear error

#### Scenario: Invalid group_life_less rejected
- **WHEN** a Spec uses `group_life_less` with both indices set or percent outside 1–100
- **THEN** `validate_mission_spec` (or Spec load) MUST fail with a clear error

#### Scenario: Missing mark zone rejected
- **WHEN** a Spec uses `mark` with a zone name absent from `zones`
- **THEN** `validate_mission_spec` MUST fail with a clear error

#### Scenario: Invalid smoke color rejected
- **WHEN** a Spec uses `smoke` with a color outside the curated set
- **THEN** `validate_mission_spec` (or Spec load) MUST fail with a clear error

#### Scenario: Valid trigger graph still passes
- **WHEN** a Spec uses supported conditions/actions with consistent zone and index refs
  and satisfies late-act / delay rules
- **THEN** validation MUST succeed for those trigger checks

#### Scenario: Non-positive altitude gate rejected
- **WHEN** a Spec uses `unit_altitude_higher` with `altitude_m` ≤ 0
- **THEN** `validate_mission_spec` (or Spec load) MUST fail with a clear error

#### Scenario: Non-positive speed gate rejected
- **WHEN** a Spec uses `unit_speed_higher` with `speed_kmh` ≤ 0
- **THEN** `validate_mission_spec` (or Spec load) MUST fail with a clear error

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

### Requirement: Ground-attack strike domain matches target units
For ground-attack Mission Specs, validation MUST resolve the strike map point from the
player airfield and `strike` bearing/distance using the same Channel terrain math as
compile, classify that point as land or sea, and require every `targets[]` unit’s
registry domain (`land` or `sea`) to match. Mismatches MUST fail with a clear
strike-domain error (e.g. land vehicles over water, or ships over land).

#### Scenario: Shipped Manston ground-attack example passes
- **WHEN** the checked-in Manston ground-attack Spec is validated
- **THEN** strike-domain checks MUST succeed

#### Scenario: Land unit over water fails
- **WHEN** a ground-attack Spec places a land-domain target at a mid-Channel strike point
- **THEN** validation MUST fail with a strike-domain mismatch error

### Requirement: Soft-warn non-integer altitude/speed gate thresholds
Validation MUST soft-warn (MUST NOT fail solely for this reason) when a trigger uses
`unit_altitude_higher`, `unit_altitude_lower`, `unit_speed_higher`, or `unit_speed_lower`
with a non-integer `altitude_m` or `speed_kmh`, because the compiler emits integer metres
or truncated speed values. Warnings MUST use a stable code (e.g.
`gate_threshold_truncated`).

#### Scenario: Fractional altitude soft-warns
- **WHEN** a Spec uses `unit_altitude_higher` with `altitude_m: 300.7`
- **THEN** validation MUST still be ok for this reason alone and MUST include a
  truncation soft-warn

#### Scenario: Integer altitude does not warn
- **WHEN** a Spec uses `unit_altitude_higher` with `altitude_m: 300`
- **THEN** validation MUST NOT emit `gate_threshold_truncated` for that condition

### Requirement: Dynamics expand validation
Validation MUST expand `dynamics` (when present) before or as part of graph checks, and
MUST verify pool indices, late_activation on referenced groups, roll range, and mode
field consistency. Invalid dynamics MUST produce structured errors (not silent omit).

#### Scenario: Missing late_activation on pooled enemy
- **WHEN** a pool references an enemy without late_activation and mode requires dormant
  pools
- **THEN** validation MUST fail or the expander MUST set late_activation true before
  emit — product MUST pick one behaviour and document it; v1 lean fail-closed if unset

#### Scenario: Bad enemy index
- **WHEN** `enemy_indices` contains an out-of-range index
- **THEN** validation MUST fail with path pointing at the pool
