# Mission Validation

## Purpose

Shared structural, DCS-exists, and free-flight semantic checks for Mission Specs.
Used by the CLI (`dcs-miz validate`) and the compiler so both surfaces share one rule set.

## Requirements

### Requirement: Shared Mission Spec validation API
The system SHALL expose a Python validation API that accepts a loaded
free-flight `MissionSpec` and returns a structured result indicating success
or one or more errors. Each error MUST include a stable machine-oriented code,
a human-readable message, and a field path when applicable. Independent checks
SHOULD be reported together rather than stopping at the first failure when
practical.

#### Scenario: Valid Manston free-flight passes
- **WHEN** the checked-in Manston cold free-flight Mission Spec is loaded and
  validated against the packaged registry and a local inventory that reports
  `TheChannel` as available and planner-supported
- **THEN** the validation result MUST indicate success with no errors

#### Scenario: Unknown airfield is reported clearly
- **WHEN** a Mission Spec names an airfield absent from the packaged registry
  for the Spec theatre
- **THEN** validation MUST fail with an error that identifies the airfield
  field and lists known airfields for that theatre (or equivalent clear
  diagnostics)

#### Scenario: Multiple independent errors collected
- **WHEN** a Mission Spec uses both an unknown aircraft id and an unknown
  weather preset
- **THEN** the validation result MUST include errors for both problems in one
  response

### Requirement: Player airfield belongs to Spec theatre
Validation SHALL reject a Mission Spec whose player airfield is not registered
for the Spec theatre, even if the same Spec key exists on another packaged
theatre. Diagnostics MUST identify the airfield field and list known airfields
for that theatre (or equivalent clear diagnostics).

#### Scenario: Channel airfield on Normandy fails
- **WHEN** a Mission Spec sets theatre `Normandy` and airfield `Manston`
- **THEN** validation MUST fail with an error that identifies the airfield
  field and lists known Normandy airfields (or equivalent clear diagnostics)

#### Scenario: Normandy airfield on Channel fails
- **WHEN** a Mission Spec sets theatre `TheChannel` and airfield
  `NeedsOarPoint`
- **THEN** validation MUST fail with an error that identifies the airfield
  field and lists known TheChannel airfields (or equivalent clear diagnostics)

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

### Requirement: Weather SoT parity includes expanded patterns
Weather SoT parity checks MUST require enum, YAML preset keys, planning_options
weather ids, and compiler-supported presets to stay aligned when patterns are
added.

#### Scenario: Parity green after expand
- **WHEN** `collect_weather_sot` / weather parity tests run after this change
- **THEN** all surfaces MUST list the same expanded weather id set

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

### Requirement: Validation accepts weather_opts
Shared validation MUST accept Specs with valid `weather_opts.seed` (non-negative
integer or project-defined int range) and MUST continue to reject unknown
weather pattern ids. Invent/resolution failures (e.g. empty gallery family
config) MUST surface as clear validation or compile errors.

#### Scenario: Valid seed validates
- **WHEN** a Channel Spec uses a known weather pattern and `weather_opts.seed`
  within the allowed range
- **THEN** validation MUST succeed for weather_opts

### Requirement: Fog dynamics validation
Shared validation MUST accept well-formed `fog_dynamics` and MUST reject invalid
timings (e.g. negative duration) with clear errors. Validation MUST NOT require
empty triggers solely because fog_dynamics is set.

#### Scenario: Negative duration rejected
- **WHEN** `fog_dynamics.duration_s` is negative
- **THEN** load or validation MUST fail

### Requirement: Player flight validation
Shared validation SHALL enforce `player.flight` rules when the object is present: `size`
in 2–4; `role` in `lead`|`wingman`; `ai_skill` in the AI allowlist (not `Player` /
`Client`); `player.skill` MUST be `Player` when flight is present; `role: wingman`
requires `size` ≥ 2. Validation MUST NOT invent aircraft ids or allow free-form skill
strings outside the allowlist.

#### Scenario: Client skill rejected with flight
- **WHEN** a Spec sets `player.flight` and `player.skill` to `Client`
- **THEN** validation MUST fail with a clear error that the human slot MUST be `Player`

#### Scenario: AI skill Player rejected
- **WHEN** a Spec sets `player.flight.ai_skill` to `Player`
- **THEN** validation MUST fail with a clear error that mates MUST use an AI skill

### Requirement: Join-up validation
Shared validation SHALL accept `player.flight.join_up` as optional boolean. When
`join_up` is true and `role` is not `wingman`, validation MAY warn or ignore without
failing. Invalid types MUST fail structural load.

#### Scenario: join_up on lead does not fail
- **WHEN** a Spec sets `role: lead` and `join_up: true`
- **THEN** validation MUST succeed (join-up is a no-op for lead structure)

### Requirement: Aircraft failure validation
Shared validation SHALL reject unknown failure ids for the player aircraft, out-of-
range probability / times, and MUST NOT invent DCS failure strings. When `failures`
is non-empty and the player aircraft has no failure catalog, validation MUST fail
clearly.

#### Scenario: Unknown id rejected
- **WHEN** a Spec sets `failures[].id` to a string not in the Channel catalog for
  `player.aircraft`
- **THEN** validation MUST fail with a clear unknown-failure error

#### Scenario: Probability out of range rejected
- **WHEN** `failures[].probability` is outside 0–100
- **THEN** load or validation MUST fail

### Requirement: Section order validation
Shared validation SHALL reject unknown order ids and SHALL reject `orders` when
`player.flight` is absent. Validation MUST NOT invent order identifiers.

#### Scenario: Unknown order id rejected
- **WHEN** a Spec sets `player.flight.orders` to include an unknown id
- **THEN** validation MUST fail with a clear unknown-order error

#### Scenario: Orders without flight rejected
- **WHEN** a Spec sets section orders without `player.flight`
- **THEN** validation MUST fail (Pydantic/extra forbid or explicit path error)

### Requirement: Validate showers scattered weather
The shared validation engine SHALL accept Channel Specs with
`weather: showers_scattered` when the id is packaged in the registry, and MUST
continue to reject unknown weather ids.

#### Scenario: Showers validates
- **WHEN** a Spec uses `weather: showers_scattered` on Channel with known player
  assets
- **THEN** validation MUST succeed for weather

### Requirement: Weather SoT parity includes showers scattered
Weather SoT parity checks MUST include `showers_scattered` across enum, YAML
preset keys, planning_options weather ids, and compiler-supported presets.

#### Scenario: Parity includes showers
- **WHEN** `collect_weather_sot` / weather parity tests run after this change
- **THEN** all surfaces MUST list `showers_scattered` in the same weather id set

### Requirement: Discipline validation
Shared validation SHALL reject `player.flight.discipline` when flight is absent,
`role` is not `wingman`, or `join_up` is false. Validation SHALL reject unknown
`hard` action ids and out-of-range radius/timing. Validation MUST NOT invent
discipline identifiers.

#### Scenario: Discipline on lead rejected
- **WHEN** a Spec sets `discipline` with `role: lead`
- **THEN** validation MUST fail with a clear role/join_up error

#### Scenario: Unknown hard action rejected
- **WHEN** `discipline.hard` is not a curated id
- **THEN** validation MUST fail with a clear unknown-hard-action error

### Requirement: Validate recon Specs
Validation SHALL accept a well-formed recon Spec and MUST reject: missing/invalid `recon`
geometry, `player.payload`, `strike`/`cap`/`escort` blocks, non-empty air `enemies`,
same-coalition contacts, unknown contact unit ids, missing `recon_area`, and
`attack_ground` (or other unsupported) objectives on recon. Errors MUST name the field path.

#### Scenario: Valid recon passes
- **WHEN** a complete Manston recon Spec is validated
- **THEN** validation MUST succeed with no errors

#### Scenario: Payload on recon fails clearly
- **WHEN** a recon Spec sets `player.payload`
- **THEN** validation MUST fail identifying `player.payload`

### Requirement: Validate target motion and domain
Validation MUST reject invalid motion combinations (patrol without radius, path
without enough points, mixed patrol+path fields, out-of-range radius). Path
waypoints and patrol centers MUST be checked against the unit’s land|sea domain
using the same Channel domain rules as strike/recon placement. Domain mismatches
MUST fail validation.

#### Scenario: Sea path on land rejected
- **WHEN** a sea-domain unit has a path point classified as land
- **THEN** validation MUST fail with a domain mismatch error

#### Scenario: Land truck path on land accepted
- **WHEN** a land soft-vehicle target has a short inland path
- **THEN** validation MUST succeed

### Requirement: Path domain mismatch remains validated
Validate SHALL continue to reject land path waypoints whose map samples are not
land (and sea path samples not sea) with motion_domain_mismatch (or an equally
specific path-point domain code). Host invent clamp MUST NOT weaken this check
for CLI validate.

#### Scenario: Off-domain land path point fails validate
- **WHEN** a land soft-vehicle target has a path point over Channel water
- **THEN** validate MUST fail with a motion domain mismatch referencing the
  path sample

### Requirement: Validate target AI options by domain and class
Validation MUST expand presets, then enforce allowlists by registry domain and
unit class heuristic (soft land vs AAA land vs sea per R12). Soft land MUST
reject interception_range and ARM-style keys if exposed. Sea MUST reject
`move_formation`, restrict_targets, and disperse-oriented fields that are
land-only (except existing `disperse_under_fire_s` already ignored/skipped for
sea emit). AAA land MAY accept interception_range. Errors MUST name field path
and reason (class/domain mismatch).

#### Scenario: Soft truck interception rejected
- **WHEN** a soft-vehicle land target sets `ai.interception_range` (or equivalent)
- **THEN** validation MUST fail with a class/domain allowlist error

#### Scenario: Sea move_formation rejected
- **WHEN** a sea-domain target sets `move_formation`
- **THEN** validation MUST fail

#### Scenario: Flak interception accepted
- **WHEN** an AAA land unit sets allowlisted interception range with valid ROE/alarm
- **THEN** validation MUST succeed when other rules pass

### Requirement: Normandy freeflight validates when inventory agrees
Validation SHALL accept a free-flight Mission Spec with theatre `Normandy` and
airfield `NeedsOarPoint` when the packaged registry supports Normandy, a terrain
binding exists, and the install inventory reports `Normandy` as available and
planner-supported.

#### Scenario: Valid Needs Oar Point freeflight passes
- **WHEN** the checked-in Normandy cold freeflight Mission Spec is validated
  against the registry and an inventory that reports `Normandy` available and
  planner-supported
- **THEN** the validation result MUST indicate success with no errors

#### Scenario: Bound Normandy theatre passes binding check
- **WHEN** a Spec uses theatre `Normandy` and the Normandy terrain binding exists
- **THEN** validation MUST NOT fail solely for terrain binding

### Requirement: Domain checks are theatre-keyed
Validation SHALL NOT run TheChannel UK–FR airport-chord domain classification
for a Spec whose theatre is not `TheChannel`. When Spec theatre is
`Normandy`, validation MUST run the Normandy UK–Cotentin chord instead.
When a Spec theatre is neither TheChannel nor Normandy and includes strike,
recon, or target-path geometry that requires land/sea domain checks,
validation MUST fail with a stable code `domain_unsupported_theatre` (or
equivalent). Airfield-relative map points MUST resolve `airdromeId` with the
Spec theatre.

#### Scenario: Normandy strike domain uses Normandy chord
- **WHEN** a Mission Spec sets theatre `Normandy` and includes land/sea strike
  geometry that requires domain classification
- **THEN** validation MUST classify using Normandy airport ids and MUST NOT
  classify points using Channel UK/FR airdrome ids

#### Scenario: Channel strike domain still classified
- **WHEN** a TheChannel ground-attack Spec is validated
- **THEN** validation MUST still apply the Channel land/sea domain rules

### Requirement: Intercept spawn is Channel-only
Validation SHALL reject `mission_type: intercept` when Spec theatre is not
`TheChannel` or `Normandy`, with stable code `intercept_unsupported_theatre`
(or equivalent).

#### Scenario: Caucasus intercept fails validation
- **WHEN** a Mission Spec sets theatre `Caucasus` and `mission_type: intercept`
- **THEN** validation MUST fail with `intercept_unsupported_theatre`

### Requirement: Normandy intercept Specs validate
Shared validation SHALL accept a well-formed Normandy intercept Spec
(theatre `Normandy`, airfield `NeedsOarPoint`, enemies present) when
inventory agrees. It MUST NOT fail Normandy intercept solely with
`intercept_unsupported_theatre`.

#### Scenario: Needs Oar Point intercept validates
- **WHEN** `examples/needs_oar_point_dawn_intercept.yaml` is validated against
  an inventory that includes offerable Normandy
- **THEN** validation MUST succeed

### Requirement: Normandy CAP Specs validate
Shared validation SHALL accept a well-formed Normandy CAP Spec (theatre
`Normandy`, airfield `NeedsOarPoint`, CAP geometry present) when inventory
agrees. Well-formed Normandy ground-attack Specs
MUST NOT fail solely with `domain_unsupported_theatre`.

#### Scenario: Needs Oar Point CAP validates
- **WHEN** `examples/needs_oar_point_cap.yaml` is validated against an
  inventory that includes offerable Normandy
- **THEN** validation MUST succeed

### Requirement: Normandy land/sea domain is classified
Validation SHALL classify land vs sea for Spec theatre `Normandy` using a
UK–Cotentin airport chord (curated Normandy airdrome ids), not the Channel
UK–FR chord. A well-formed Normandy ground-attack Spec whose strike point is
inland of Maupertus MUST pass domain checks when targets are land units.
Other non-Channel theatres MUST still fail with `domain_unsupported_theatre`.

#### Scenario: Normandy inland strike is land
- **WHEN** a Normandy Spec places strike at 180° / 133 km from NeedsOarPoint
  with land targets
- **THEN** validation MUST succeed (MUST NOT emit `domain_unsupported_theatre`)

#### Scenario: Normandy mid-Channel CAP station is sea
- **WHEN** domain is classified at 180° / 63 km from NeedsOarPoint on
  Normandy terrain
- **THEN** the result MUST be `sea`

#### Scenario: Caucasus strike still fails closed
- **WHEN** a Caucasus Spec includes strike geometry that requires domain
  classification
- **THEN** validation MUST fail with `domain_unsupported_theatre`

### Requirement: Normandy ground_attack Specs validate
Shared validation SHALL accept a well-formed Normandy ground-attack Spec
(theatre `Normandy`, airfield `NeedsOarPoint`, strike + land targets) when
inventory agrees.

#### Scenario: Needs Oar Point ground_attack validates
- **WHEN** `examples/needs_oar_point_ground_attack.yaml` is validated against
  an inventory that includes offerable Normandy
- **THEN** validation MUST succeed

### Requirement: Normandy escort Specs validate
Shared validation SHALL accept a well-formed Normandy escort Spec
(theatre `Normandy`, airfield `NeedsOarPoint`, nested escort + package)
when inventory agrees.

#### Scenario: Needs Oar Point escort validates
- **WHEN** `examples/needs_oar_point_escort.yaml` is validated against
  an inventory that includes offerable Normandy
- **THEN** validation MUST succeed

### Requirement: Normandy recon Specs validate
Shared validation SHALL accept a well-formed Normandy recon Spec
(theatre `Normandy`, airfield `NeedsOarPoint`, nested recon + land contacts)
when inventory agrees.

#### Scenario: Needs Oar Point recon validates
- **WHEN** `examples/needs_oar_point_recon.yaml` is validated against
  an inventory that includes offerable Normandy
- **THEN** validation MUST succeed

### Requirement: Known countries and aircraft are era-filtered
Shared validation SHALL resolve known countries and known aircraft using the
Spec theatre’s packaged era (`era_for_theatre`). A WWII theatre MUST reject
`Georgia` / `Turkey` / `Su-25T`. A modern theatre MUST accept
`SpitfireLFMkIX` (dual-era). It MUST still reject modern-only countries on
WWII theatres.

#### Scenario: Channel rejects Georgia
- **WHEN** a TheChannel Mission Spec sets player country `Georgia`
- **THEN** validation MUST fail with an unknown-country error

#### Scenario: Caucasus accepts Spitfire
- **WHEN** a Caucasus Mission Spec sets player aircraft `SpitfireLFMkIX`
- **THEN** validation MUST succeed when the rest of the Spec is well-formed

### Requirement: Caucasus freeflight validates when inventory agrees
Validation SHALL accept a free-flight Mission Spec with theatre `Caucasus`
and airfield `Batumi` when the packaged registry supports Caucasus, a terrain
binding exists, and the install inventory reports `Caucasus` as available and
planner-supported.

#### Scenario: Valid Batumi freeflight passes
- **WHEN** the checked-in Caucasus cold freeflight Mission Spec is validated
  against the registry and an inventory that reports `Caucasus` available and
  planner-supported
- **THEN** the validation result MUST indicate success with no errors

### Requirement: Batumi Spitfire freeflight validates
Shared validation SHALL accept `examples/batumi_spitfire_freeflight.yaml`
when inventory agrees.

#### Scenario: Batumi Spitfire validates
- **WHEN** that example is validated against offerable Caucasus inventory
- **THEN** validation MUST succeed

### Requirement: Caucasus CAP Specs validate
Shared validation SHALL accept a well-formed Caucasus CAP Spec (theatre
`Caucasus`, airfield `Batumi`, CAP geometry present, player Georgia `Su-25T`,
enemies Russia `Su-25T` red) when inventory agrees. It MUST still reject
Caucasus intercept with `intercept_unsupported_theatre` and Caucasus
strike/recon/path geometry with `domain_unsupported_theatre`.

#### Scenario: Batumi CAP validates
- **WHEN** `examples/batumi_black_sea_cap.yaml` is validated against an
  inventory that includes offerable Caucasus
- **THEN** validation MUST succeed

#### Scenario: Caucasus intercept still fails closed
- **WHEN** a Mission Spec sets theatre `Caucasus` and `mission_type: intercept`
- **THEN** validation MUST fail with `intercept_unsupported_theatre`

### Requirement: Caucasus Mozdok freeflight validates
Shared validation SHALL accept a well-formed Caucasus free-flight Spec with
airfield `Mozdok` and player country `Russia` on coalition red when inventory
agrees. Channel/Normandy MUST still reject `Russia` as unknown-country.

#### Scenario: Needs Mozdok freeflight validates
- **WHEN** `examples/mozdok_cold_freeflight.yaml` is validated against an
  inventory that includes offerable Caucasus
- **THEN** validation MUST succeed

#### Scenario: Channel rejects Russia
- **WHEN** a TheChannel Mission Spec sets player country `Russia`
- **THEN** validation MUST fail with an unknown-country error

### Requirement: Channel rejects Turkey
Shared validation SHALL reject player country `Turkey` on a WWII theatre
(TheChannel / Normandy) with an unknown-country error. A Syria Spec MAY
use `Turkey`.

#### Scenario: Channel rejects Turkey
- **WHEN** a TheChannel Mission Spec sets player country `Turkey`
- **THEN** validation MUST fail with an unknown-country error

### Requirement: Syria freeflight validates when inventory agrees
Validation SHALL accept a free-flight Mission Spec with theatre `Syria`
and airfield `Incirlik` when the packaged registry supports Syria, a terrain
binding exists, and the install inventory reports `Syria` as available and
planner-supported.

#### Scenario: Valid Incirlik freeflight passes
- **WHEN** the checked-in Syria cold freeflight Mission Spec is validated
  against the registry and an inventory that reports `Syria` available and
  planner-supported
- **THEN** the validation result MUST indicate success with no errors

#### Scenario: Syria accepts Spitfire
- **WHEN** a Syria Mission Spec sets player aircraft `SpitfireLFMkIX`
- **THEN** validation MUST succeed when the rest of the Spec is well-formed

### Requirement: Channel rejects USA
Shared validation SHALL reject player country `USA` on a WWII theatre
(TheChannel / Normandy) with an unknown-country error. A Nevada Spec MAY
use `USA`.

#### Scenario: Channel rejects USA
- **WHEN** a TheChannel Mission Spec sets player country `USA`
- **THEN** validation MUST fail with an unknown-country error

### Requirement: Nevada freeflight validates when inventory agrees
Validation SHALL accept a free-flight Mission Spec with theatre `Nevada`
and airfield `Nellis` when the packaged registry supports Nevada, a terrain
binding exists, and the install inventory reports `Nevada` as available and
planner-supported.

#### Scenario: Valid Nellis freeflight passes
- **WHEN** the checked-in Nevada cold freeflight Mission Spec is validated
  against the registry and an inventory that reports `Nevada` available and
  planner-supported
- **THEN** the validation result MUST indicate success with no errors

#### Scenario: Nevada accepts Spitfire
- **WHEN** a Nevada Mission Spec sets player aircraft `SpitfireLFMkIX`
- **THEN** validation MUST succeed when the rest of the Spec is well-formed

### Requirement: Falklands freeflight validates when inventory agrees
Validation SHALL accept a free-flight Mission Spec with theatre `Falklands`
and airfield `MountPleasant` when the packaged registry supports Falklands, a
terrain binding exists, and the install inventory reports `Falklands` as
available and planner-supported.

#### Scenario: Valid Mount Pleasant freeflight passes
- **WHEN** the checked-in Falklands cold freeflight Mission Spec is validated
  against the registry and an inventory that reports `Falklands` available and
  planner-supported
- **THEN** the validation result MUST indicate success with no errors

#### Scenario: Falklands accepts Spitfire
- **WHEN** a Falklands Mission Spec sets player aircraft `SpitfireLFMkIX`
- **THEN** validation MUST succeed when the rest of the Spec is well-formed

#### Scenario: Channel still accepts UK
- **WHEN** a TheChannel Mission Spec sets player country `UK`
- **THEN** validation MUST succeed for country (WWII era still includes UK)
