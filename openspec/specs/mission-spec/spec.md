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
The Mission Spec MAY include optional top-level keys `enemies`, `objectives`, `triggers`,
`targets`, `package`, and `zones`. For free-flight missions combat keys MUST be absent or
empty per existing free-flight rules. For intercept missions, `enemies` and `objectives`
MUST be non-empty per intercept rules. For CAP missions, `objectives` MUST be non-empty per
CAP rules and `enemies` MAY be empty or non-empty; CAP Specs MUST also include the nested
`cap` block. For ground-attack missions, `targets` and `objectives` MUST be non-empty per
ground-attack rules, `enemies` MUST be empty, and the nested `strike` block MUST be present.
For escort missions, `package` and `objectives` MUST be non-empty per escort rules,
`enemies` MAY be empty or non-empty, the nested `escort` block MUST be present, and
`targets` / `strike` / `player.payload` MUST be absent or unsupported. `triggers` and
`zones` MAY be non-empty when they conform to the typed mission-triggers model. Free-form
or Lua-bearing trigger payloads MUST be rejected. The system MUST NOT silently drop
unsupported non-empty values.

#### Scenario: Free flight with absent extensions compiles
- **WHEN** a free-flight Mission Spec omits `enemies`, `objectives`, `triggers`,
  `targets`, `package`, and `zones`
- **THEN** the Spec SHALL be structurally valid and the compiler MUST proceed as for free
  flight

#### Scenario: Typed triggers allowed on free flight
- **WHEN** a free-flight Spec includes a well-typed `time_more` → `message` trigger and
  empty combat extensions
- **THEN** structural load and shared validation MUST succeed

#### Scenario: Free flight refuses non-empty enemies
- **WHEN** a free-flight Mission Spec sets `enemies` to a non-empty value
- **THEN** the system MUST refuse load or validation with a clear error that free_flight
  requires empty combat extensions

#### Scenario: Escort requires package and escort block
- **WHEN** an escort Mission Spec omits `package` or the nested `escort` block
- **THEN** loading or validation MUST fail with a clear error

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
(structured field agreed in design). Unknown objective types MUST be rejected. Typed
`triggers`/`zones` MAY be present per the mission-triggers model.

#### Scenario: intercept_enemy objective accepted
- **WHEN** an intercept Spec includes the supported intercept objective shape and empty
  `triggers`
- **THEN** validation MUST accept the Spec (subject to other intercept rules)

#### Scenario: Well-typed triggers allowed on intercept
- **WHEN** an intercept Spec sets a well-typed non-empty `triggers` list
- **THEN** structural load and shared validation MUST succeed (native ME emit via the compiler)

### Requirement: Checked-in intercept example Spec
The repository SHALL include a checked-in example Mission Spec for the Manston dawn-style
intercept (early start time, Channel, Spitfire player, Bf-109K-4 enemies) usable as validate
and compile input.

#### Scenario: Example present
- **WHEN** a developer clones the repository
- **THEN** an intercept example Spec MUST be present and loadable under schema_version `"1"`

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
Typed `triggers`/`zones` MAY be present per the mission-triggers model. Objective type
`patrol` MUST be rejected on non-CAP mission types unless a later change explicitly allows it.

#### Scenario: Pure patrol CAP accepted
- **WHEN** a CAP Spec has `objectives` containing `patrol` and empty `enemies`
- **THEN** validation MUST accept the Spec (subject to other CAP and registry rules)

#### Scenario: CAP with light opposition accepted
- **WHEN** a CAP Spec includes a non-empty `enemies` list with known Channel aircraft ids and
  a `patrol` objective
- **THEN** the Spec MUST load as structurally valid for CAP compilation

#### Scenario: Well-typed triggers allowed on CAP
- **WHEN** a CAP Spec sets a well-typed non-empty `triggers` list
- **THEN** structural load and shared validation MUST succeed (native ME emit via the compiler)

### Requirement: Checked-in CAP example Spec
The repository SHALL include a checked-in example Mission Spec for a Manston Channel CAP
(player Spitfire, airfield-relative station, engagement rules) usable as validate and
compile input under schema_version `"1"`.

#### Scenario: Example present
- **WHEN** a developer clones the repository
- **THEN** a CAP example Spec MUST be present and loadable under schema_version `"1"`

### Requirement: Ground-attack mission type
The Mission Spec SHALL support `mission_type` value `ground_attack` in addition to
`free_flight`, `intercept`, and `cap`. A ground-attack Spec MUST include a nested `strike`
object (airfield-relative target area and altitude), a non-empty `targets` list of ground
units, a named `player.payload` preset, and a non-empty `objectives` list including
`attack_ground`. Air `enemies` MUST be empty. Free-flight, intercept, and CAP rules MUST
remain unchanged. The `strike` block MUST be forbidden on non–ground_attack types.

#### Scenario: Manston ground-attack Spec accepted
- **WHEN** a Mission Spec sets `mission_type` to `ground_attack`, player `SpitfireLFMkIX` at
  Manston with a known payload preset, a valid `strike` block, non-empty `targets`, and an
  `attack_ground` objective
- **THEN** the Spec MUST load as structurally valid for ground-attack compilation

#### Scenario: Strike block forbidden on free flight
- **WHEN** a Mission Spec sets `mission_type` to `free_flight` and includes a `strike` object
- **THEN** loading or validation MUST fail with a clear error

### Requirement: Strike target area is airfield-relative
The `strike` block SHALL express the target area as `bearing_deg` (0–360) and a positive
`distance_km` relative to the player departure airfield, plus a positive `altitude_m` for
ingress. The Spec MUST NOT require raw Channel map x/y or invented WGS84 coordinates.

#### Scenario: Bearing and distance required
- **WHEN** a ground-attack Spec omits `bearing_deg` or `distance_km`, or sets a non-positive
  distance or altitude
- **THEN** loading MUST fail with a structural validation error identifying the `strike` fields

### Requirement: Ground targets collection
A ground-attack Mission Spec MUST declare a non-empty `targets` list. Each target entry MUST
include an exact DCS land-vehicle or ship type id and a positive count. Unknown unit ids MUST
be rejected by validation against the Channel strike-target registry (land + sea). Air
`enemies` MUST remain empty for ground_attack. Land vehicles are for enemy-held territory;
over-water placements MUST use sea-domain ship ids.

#### Scenario: Soft truck targets accepted
- **WHEN** a ground-attack Spec lists known Channel ground unit ids with valid counts and
  empty `enemies`
- **THEN** the Spec MUST load as structurally valid for compilation

#### Scenario: Unknown ground unit rejected
- **WHEN** a ground-attack Spec names a ground unit absent from the Channel registry
- **THEN** validation MUST fail identifying the unknown unit

#### Scenario: Non-empty air enemies refused for ground attack
- **WHEN** a ground-attack Spec sets a non-empty `enemies` list
- **THEN** loading or validation MUST fail stating air enemies are not supported for
  ground_attack in this schema version

### Requirement: Enemy-only strike targets
Every ground-attack `targets` entry MUST belong to the coalition opposing `player.coalition`
(no same-side / friendly targets) **unless** `strike.practice` is true (bombing-practice /
training narrative). When `practice` is false or omitted, validation MUST reject any target
whose coalition matches the player. When `practice` is true, same-coalition targets MUST be
accepted (e.g. UK-side range targets for a blue player). The compiler MUST place target
groups on the coalition declared in each target entry.

#### Scenario: Blue player with red targets accepted
- **WHEN** a ground-attack Spec has `player.coalition` `blue` and all `targets` use coalition
  `red`
- **THEN** the Spec MUST load as structurally valid (subject to other ground-attack rules)

#### Scenario: Friendly / same-coalition target rejected in combat
- **WHEN** a ground-attack Spec has `strike.practice` false or omitted and includes a target
  whose coalition equals `player.coalition`
- **THEN** loading or validation MUST fail with a clear error that strike targets must be
  enemy (opposing coalition) only unless practice is set

#### Scenario: Practice strike allows same-coalition targets
- **WHEN** a ground-attack Spec sets `strike.practice` true and includes same-coalition
  targets (e.g. blue player, blue UK-side trucks)
- **THEN** the Spec MUST load as structurally valid (subject to other ground-attack rules)

### Requirement: Named player payload preset
A ground-attack Spec MUST set `player.payload` to a named Channel payload preset that is
valid for the player aircraft. Unknown presets or presets for a different aircraft MUST be
rejected. Free-flight, intercept, and CAP Specs MUST omit `player.payload` (or treat it as
unsupported) for this schema version. Packaged presets MUST include at least one
Channel-crossing Spitfire loadout that combines wing bombs with the verified 45 gal slipper
tank CLSID (centreline tank and centreline 500 lb bomb are mutually exclusive on the same
pylon).

#### Scenario: spitfire_2x250_slipper accepted
- **WHEN** a ground-attack Spec sets `player.payload` to a registered SpitfireLFMkIX preset
  that includes wing bomb CLSIDs and the slipper-tank CLSID
- **THEN** the Spec MUST be structurally valid (subject to other ground-attack rules)

#### Scenario: spitfire bomb-only preset accepted
- **WHEN** a ground-attack Spec sets `player.payload` to a registered SpitfireLFMkIX bomb
  preset without a tank
- **THEN** the Spec MUST be structurally valid (subject to other ground-attack rules)

#### Scenario: Unknown payload rejected
- **WHEN** a ground-attack Spec sets `player.payload` to an undeclared name
- **THEN** validation MUST fail identifying the unknown payload

### Requirement: Ground-attack objective
A ground-attack Mission Spec MUST declare a non-empty `objectives` list including objective
type `attack_ground`. Typed `triggers`/`zones` MAY be present per the mission-triggers
model. Objective type `attack_ground` MUST be rejected on non–ground_attack mission types
unless a later change explicitly allows it.

#### Scenario: attack_ground objective accepted
- **WHEN** a ground-attack Spec includes `attack_ground` and empty `triggers`
- **THEN** validation MUST accept the Spec (subject to other ground-attack and registry rules)

#### Scenario: Well-typed triggers allowed on ground-attack
- **WHEN** a ground-attack Spec sets a well-typed non-empty `triggers` list
- **THEN** structural load and shared validation MUST succeed (native ME emit via the compiler)

### Requirement: Checked-in ground-attack example Spec
The repository SHALL include a checked-in example Mission Spec for a Manston Channel
ground-attack (Spitfire with bomb preset, airfield-relative strike, ground targets) usable as
validate and compile input under schema_version `"1"`.

#### Scenario: Example present
- **WHEN** a developer clones the repository
- **THEN** a ground-attack example Spec MUST be present and loadable under schema_version `"1"`

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
`escort_package`. Typed `triggers`/`zones` MAY be present per the mission-triggers model.
Objective type `escort_package` MUST be rejected on non-escort mission types unless a later
change explicitly allows it.

#### Scenario: escort_package objective accepted
- **WHEN** an escort Spec includes `escort_package` and empty `triggers`
- **THEN** validation MUST accept the Spec (subject to other escort and registry rules)

#### Scenario: Well-typed triggers allowed on escort
- **WHEN** an escort Spec sets a well-typed non-empty `triggers` list
- **THEN** structural load and shared validation MUST succeed (native ME emit via the compiler)

### Requirement: Checked-in escort example Spec
The repository SHALL include a checked-in example Mission Spec for a Manston Channel escort
(Spitfire escorting a friendly package to an airfield-relative destination, optional bounce)
usable as validate and compile input under schema_version `"1"`.

#### Scenario: Example present
- **WHEN** a developer clones the repository
- **THEN** an escort example Spec MUST be present and loadable under schema_version `"1"`

### Requirement: Dawn and marginal VFR weather presets
The Mission Spec SHALL support weather preset values `dawn_clear` and `marginal_vfr` in
addition to `sunny_clear` under schema_version `"1"`. These values MUST be registered in
the Channel weather preset registry with human-readable descriptions.

#### Scenario: Dawn clear Spec is valid
- **WHEN** a Mission Spec sets `weather: dawn_clear` with an otherwise valid free-flight
  Channel payload
- **THEN** structural load and shared validation MUST accept the Spec

#### Scenario: Marginal VFR Spec is valid
- **WHEN** a Mission Spec sets `weather: marginal_vfr` with an otherwise valid free-flight
  Channel payload
- **THEN** structural load and shared validation MUST accept the Spec

### Requirement: Expanded Channel weather pattern ids
The Mission Spec `weather` field SHALL accept additional named Channel weather
pattern ids beyond `sunny_clear`, `dawn_clear`, and `marginal_vfr`, including at
least campaign-seeded patterns for light scattered, high scattered, broken,
overcast, rain overcast, and scattered summer (exact enum snake_case ids as
packaged). Unknown weather ids MUST still fail validation.

#### Scenario: New pattern Spec loads
- **WHEN** a Spec sets `weather` to a packaged expanded pattern id
- **THEN** loading and validation MUST succeed when the rest of the Spec is valid

#### Scenario: Unknown weather still rejected
- **WHEN** a Spec sets `weather` to an id not in the WeatherPreset enum
- **THEN** loading or validation MUST fail with a clear weather error

### Requirement: Dawn and marginal example Specs
The repository SHALL include checked-in example Mission Specs demonstrating dawn
(`dawn_clear` with a dawn-appropriate `start_time`) and marginal VFR (`marginal_vfr`)
Channel free-flight (or equivalent minimal) sorties usable as validate/compile input.

#### Scenario: Dawn example present
- **WHEN** a developer lists Channel weather examples
- **THEN** a dawn example Spec MUST be present and compile under Channel inventory

#### Scenario: Marginal VFR example present
- **WHEN** a developer lists Channel weather examples
- **THEN** a marginal VFR example Spec MUST be present and compile under Channel inventory

### Requirement: Optional narrative on Mission Spec
The Mission Spec MAY include a `narrative` object with `enabled` (boolean, default
false). When omitted, behaviour MUST match Specs with no narrative. Enabling narrative
MUST NOT introduce Lua or script fields on the Spec.

#### Scenario: Narrative field loads
- **WHEN** a Spec YAML includes `narrative: { enabled: true }` with an otherwise valid CAP
- **THEN** structural load MUST succeed (subject to narrative expansion/validation rules)

#### Scenario: Unknown narrative fields rejected
- **WHEN** `narrative` includes an undeclared field
- **THEN** loading MUST fail (unknown field)

### Requirement: Late activation on combat groups
`EnemyFlight` and `GroundTarget` entries MAY set `late_activation` (boolean, default
false). When true, the compiler MUST place the group as late-activated (dormant until an
`activate_group` action references it). When false or omitted, groups MUST remain
immediately active as today.

#### Scenario: Late enemy defaults off
- **WHEN** an enemy flight omits `late_activation`
- **THEN** loading MUST treat it as false and compile MUST not mark the group late-activated

#### Scenario: Late enemy accepted
- **WHEN** an enemy flight sets `late_activation: true`
- **THEN** structural load MUST succeed when the rest of the Spec is valid

### Requirement: Sound actions reference curated assets only
When a Mission Spec includes a trigger `sound` action, it MUST identify audio by a
curated `asset_id` from the product sound-asset registry. The Spec MUST NOT carry raw
audio paths or binary sound data.

#### Scenario: asset_id field only
- **WHEN** a Spec declares `type: sound` with `asset_id` and no path fields
- **THEN** loading MUST succeed when the rest of the Spec is valid

### Requirement: Triggers may use group life less thresholds
When a Mission Spec includes a trigger condition `group_life_less`, it MUST identify the
affected group by Spec `enemy_index` or `target_index` and a remaining-life `percent`
threshold. The Spec MUST NOT carry raw DCS group ids for this condition.

#### Scenario: Index and percent fields
- **WHEN** a Spec declares `type: group_life_less` with exactly one index field and
  `percent` in 1–100
- **THEN** loading MUST succeed when the rest of the Spec is valid

### Requirement: Triggers may use map marks and zone smoke
When a Mission Spec includes a trigger action `mark`, it MUST identify the location by
Spec zone name and provide mark `text`. When it includes `smoke`, it MUST identify the
location by Spec zone name and a curated smoke `color`. The Spec MUST NOT carry raw map
coordinates or free-form Lua for these actions.

#### Scenario: Mark fields
- **WHEN** a Spec declares `type: mark` with `zone` and `text`
- **THEN** loading MUST succeed when the rest of the Spec is valid

#### Scenario: Smoke fields
- **WHEN** a Spec declares `type: smoke` with `zone` and a curated `color`
- **THEN** loading MUST succeed when the rest of the Spec is valid

### Requirement: Triggers may use player altitude and speed gates
When a Mission Spec includes a trigger condition `unit_altitude_higher` or
`unit_altitude_lower`, it MUST provide `altitude_m` (> 0) and MAY set `agl` (default
true). When it includes `unit_speed_higher` or `unit_speed_lower`, it MUST provide
`speed_kmh` (> 0). These conditions MUST refer to the player aircraft only. The Spec MUST
NOT carry raw DCS unit ids or free-form Lua for these conditions.

#### Scenario: Altitude gate fields
- **WHEN** a Spec declares `type: unit_altitude_higher` with `altitude_m` and optional
  `agl`
- **THEN** loading MUST succeed when the rest of the Spec is valid

#### Scenario: Speed gate fields
- **WHEN** a Spec declares `type: unit_speed_lower` with `speed_kmh`
- **THEN** loading MUST succeed when the rest of the Spec is valid

### Requirement: Optional dynamics expand pack on Mission Spec
The Mission Spec SHALL allow an optional `dynamics` object with `mode` one of
`fixed`, `live`, `choose`, `hybrid`, a non-empty `pools` list (except `fixed` may
omit pools), optional `roll` / `menu` / `exclusive` fields as designed. Pool entries
MUST reference existing enemy and/or target indices only (no invented unit placement).
When `dynamics` is set, zones and triggers MUST be empty before expand (same conflict
rule family as narrative). The system MUST expand `dynamics` into typed native trigger
actions (`set_flag_random`, radio items, `activate_group`, messages as applicable)
before validation/compile completes, without LLM Lua.

#### Scenario: Live mode expands dice and activates late enemies
- **WHEN** a Spec has `dynamics.mode: live`, late-activated enemies, empty triggers, and
  pools with `roll_value` / `enemy_indices`
- **THEN** expand MUST emit `set_flag_random` and activate the matching enemy groups
  via existing Spec trigger vocabulary

#### Scenario: Choose mode expands F10 menu
- **WHEN** a Spec has `dynamics.mode: choose` with pool `menu_label`s and late enemies
- **THEN** expand MUST emit radio menu items that activate the corresponding pools

#### Scenario: Dynamics conflicts with hand triggers
- **WHEN** `dynamics` is set and `triggers` is non-empty
- **THEN** validation MUST fail with a clear conflict error

#### Scenario: Narrative and dynamics not both expanding
- **WHEN** both `narrative.enabled` and `dynamics` would expand into an empty trigger
  graph
- **THEN** validation MUST reject the combination (XOR expand authority)

### Requirement: Optional weather_opts seed on Mission Spec
The Mission Spec MAY include optional `weather_opts` with integer `seed`.
Omitted `weather_opts` MUST remain valid. Unknown keys under `weather_opts`
MUST be rejected. The top-level `weather` field MUST remain a WeatherPreset
enum id (not a nested object).

#### Scenario: Spec with weather_opts seed loads
- **WHEN** a Spec sets `weather: broken_channel` and `weather_opts: { seed: 42 }`
- **THEN** structural load MUST succeed

#### Scenario: Spec without weather_opts still loads
- **WHEN** a Spec omits `weather_opts`
- **THEN** structural load MUST succeed as today

### Requirement: Fog dynamics Spec declares burn-off or roll-in
The Mission Spec MAY include optional `fog_dynamics` with `mode` one of
`burn_off` or `roll_in`, `start_after_s` and `duration_s` (non-negative), and
optional end fog numerics. The Spec MUST NOT carry free-form Lua. Omitted
`fog_dynamics` MUST preserve prior behaviour.

#### Scenario: Burn-off Spec loads
- **WHEN** a Spec sets `fog_dynamics.mode: burn_off` with valid timings
- **THEN** structural load MUST succeed

#### Scenario: Free-form script rejected
- **WHEN** a Spec includes an undeclared script or Lua field for fog
- **THEN** loading MUST fail (unknown field / forbid)

### Requirement: Optional player flight section
The Mission Spec SHALL allow an optional nested `player.flight` object on `player`.
When present it MUST declare `size` (integer 2–4 inclusive) and MAY declare `role`
(`lead` or `wingman`, default `lead`) and `ai_skill` (an AI skill name from the Channel
skill allowlist excluding `Player` and `Client`, default `Average`). When `player.flight`
is omitted, the Spec MUST continue to mean a solo player aircraft (effective size 1).
`role: wingman` MUST require `size` ≥ 2.

#### Scenario: Four-ship lead accepted
- **WHEN** a Mission Spec sets `player.flight.size` to `4` and `role` to `lead` (or omits
  role) with otherwise valid Channel player fields
- **THEN** structural load MUST succeed

#### Scenario: Pair wingman accepted
- **WHEN** a Mission Spec sets `player.flight.size` to `2` and `role` to `wingman`
- **THEN** structural load MUST succeed

#### Scenario: Solo by omission
- **WHEN** a Mission Spec omits `player.flight`
- **THEN** the Spec MUST remain valid as a solo player placement (unchanged from prior
  behaviour)

#### Scenario: Invalid size rejected
- **WHEN** a Mission Spec sets `player.flight.size` to `1` or `5`
- **THEN** loading or validation MUST fail with a clear error that size MUST be 2–4

### Requirement: Optional flight join-up flag
The Mission Spec SHALL allow optional `player.flight.join_up` (boolean, default
`true`). When `role` is `wingman` and `join_up` is true, the compiler MUST emit
Follow/shared-route behaviour per miz-compiler. When `join_up` is false, wingman
placement MUST remain separate groups without Follow (as `#15b`). For `role: lead`,
`join_up` MUST NOT change group structure (same-group section).

#### Scenario: Wingman join-up default
- **WHEN** a Spec sets `player.flight.role: wingman` and omits `join_up`
- **THEN** structural load MUST succeed and join-up MUST be treated as enabled

#### Scenario: Wingman join-up opt-out
- **WHEN** a Spec sets `player.flight.role: wingman` and `join_up: false`
- **THEN** structural load MUST succeed

### Requirement: Optional aircraft failures list
The Mission Spec SHALL allow an optional top-level `failures` list. When omitted or
empty, no Failures panel rows MUST be implied. When present, each entry MUST declare
`id` (string), `start_after_s` (non-negative integer seconds, floored to ME After
minutes on emit), and MAY declare `probability` (0–100, default 100) and
`random_pause_s` (non-negative integer, default 0; maps to Within minutes with
minimum 1). Failure `id` values MUST be exact curated DCS failure identifiers for
the player aircraft — not free-form prose.

#### Scenario: Scheduled magneto failure accepted
- **WHEN** a Spec sets `failures` to one entry with a catalog Spitfire id and
  `start_after_s: 120`
- **THEN** structural load MUST succeed

#### Scenario: Omit failures means none
- **WHEN** a Spec omits `failures`
- **THEN** the Spec MUST remain valid without failure behaviour

### Requirement: Optional curated section orders
The Mission Spec SHALL allow an optional `player.flight.orders` list of curated
order identifiers. When omitted or empty, the compiler MUST NOT emit the
section-order F10 pack from this feature. When present, each id MUST be from the
Channel curated order set (`rejoin`, `engage`, `orbit`, `rtb`, `break` in v1).
`orders` MUST require `player.flight` to be set.

#### Scenario: Orders on wingman flight accepted
- **WHEN** a Spec sets `player.flight` with `role: wingman` and
  `orders: [rejoin, rtb]`
- **THEN** structural load MUST succeed

#### Scenario: Omit orders means none
- **WHEN** a Spec has `player.flight` but omits `orders`
- **THEN** the Spec MUST remain valid without section-order F10 emit from this feature

### Requirement: Showers scattered weather pattern id
The Mission Spec `weather` field SHALL accept `showers_scattered` as a
`WeatherPreset` value for Channel light-rain / showery gallery weather, in
addition to existing packaged patterns. Unknown weather ids MUST still fail
validation.

#### Scenario: Showers Spec loads
- **WHEN** a Spec sets `weather: showers_scattered` with an otherwise valid
  free-flight Channel Spec
- **THEN** loading and validation MUST succeed

#### Scenario: Unknown weather still rejected
- **WHEN** a Spec sets `weather` to an id not in the WeatherPreset enum
- **THEN** loading or validation MUST fail with a clear weather error

### Requirement: Optional flight discipline
The Mission Spec SHALL allow an optional `player.flight.discipline` object. When
omitted, the compiler MUST NOT emit fail-to-follow discipline behaviour. When
present (including empty object using defaults), discipline MUST be considered
armed and MUST only apply with `role: wingman` and `join_up: true`. Fields SHALL
include radius and soft/hard timing plus a curated `hard` action id
(`message_end` | `mission_end` | `section_rtb`).

#### Scenario: Discipline object on wingman join_up accepted
- **WHEN** a Spec sets `player.flight` with `role: wingman`, `join_up: true`, and
  `discipline: {}`
- **THEN** structural load MUST succeed

#### Scenario: Omit discipline means off
- **WHEN** a Spec has `player.flight` but omits `discipline`
- **THEN** the Spec MUST remain valid without fail-to-follow emit from this feature

### Requirement: Recon mission type
The Mission Spec SHALL support `mission_type` value `recon` in addition to `free_flight`,
`intercept`, `cap`, `ground_attack`, and `escort`. A recon Spec MUST include a nested
`recon` object (airfield-relative AOI and altitude), a non-empty `objectives` list including
`recon_area`, and MUST omit `player.payload`, `strike`, `cap`, and `escort`. Air `enemies`
MUST be empty. Optional `targets` MAY list enemy visual contacts. Existing mission types
MUST remain unchanged. The `recon` block MUST be forbidden on non-recon types.

#### Scenario: Manston recon Spec accepted
- **WHEN** a Mission Spec sets `mission_type` to `recon`, player `SpitfireLFMkIX` at
  Manston, a valid `recon` block, empty `enemies`, no payload, and a `recon_area` objective
- **THEN** the Spec MUST load as structurally valid for recon compilation

#### Scenario: Recon block forbidden on free flight
- **WHEN** a Mission Spec sets `mission_type` to `free_flight` and includes a `recon` object
- **THEN** loading or validation MUST fail with a clear error

#### Scenario: Payload forbidden on recon
- **WHEN** a recon Spec sets `player.payload`
- **THEN** loading or validation MUST fail stating payload is not supported for recon

### Requirement: Recon AOI is airfield-relative
The `recon` block SHALL express the AOI centre as `bearing_deg` (0–360) and a positive
`distance_km` relative to the player departure airfield, plus a positive `altitude_m` for
ingress/observe. It MUST include a positive `radius_m` for the AOI zone (or apply a
documented default). The Spec MUST NOT require raw Channel map x/y or invented WGS84
coordinates.

#### Scenario: Bearing and distance required
- **WHEN** a recon Spec omits `bearing_deg` or `distance_km`, or sets a non-positive
  distance, altitude, or radius
- **THEN** loading MUST fail with a structural validation error identifying the `recon`
  fields

### Requirement: Optional visual contacts
A recon Spec MAY declare an empty or non-empty `targets` list. When non-empty, each entry
MUST use a known Channel strike-unit id (land or sea), positive count, and opposing
coalition relative to `player.coalition`. Air `enemies` MUST remain empty. Contacts are
observe-only — Spec MUST NOT treat them as strike/destroy objectives.

#### Scenario: Area recon with empty targets
- **WHEN** a recon Spec omits targets or sets `targets: []`
- **THEN** the Spec MUST load as structurally valid (area recon)

#### Scenario: Enemy truck contacts accepted
- **WHEN** a recon Spec lists known Channel ground unit ids with opposing coalition and
  empty `enemies`
- **THEN** the Spec MUST load as structurally valid for compilation

#### Scenario: Same-coalition contact rejected
- **WHEN** a recon Spec includes a target whose coalition equals `player.coalition`
- **THEN** loading or validation MUST fail (contacts must be opposing coalition)

#### Scenario: Non-empty air enemies refused for recon
- **WHEN** a recon Spec sets a non-empty `enemies` list
- **THEN** loading or validation MUST fail stating air enemies are not supported for recon
  in this schema version

### Requirement: Recon objective
A recon Spec MUST declare a non-empty `objectives` list that includes `recon_area`.
Unsupported objective types for recon (including `attack_ground`) MUST be rejected.

#### Scenario: recon_area required
- **WHEN** a recon Spec has empty objectives or only non-`recon_area` objective types
- **THEN** loading or validation MUST fail requiring `recon_area`

#### Scenario: attack_ground rejected on recon
- **WHEN** a recon Spec includes an `attack_ground` objective
- **THEN** loading or validation MUST fail

### Requirement: Ground targets MAY declare motion
Each `targets[]` entry MAY include optional motion. Omit or `motion: static` MUST
mean a single placement (current behaviour). `motion: patrol` MUST include
`patrol_radius_m` within an allowed range. `motion: path` MUST include a list of
2–6 airfield-relative `{bearing_deg, distance_km}` waypoints (loop implied).
`patrol` and `path` MUST NOT be combined on the same target. Unknown motion values
MUST be rejected. Moving targets MAY set optional `speed_kmh` (clamped to a curated
unit speed band) and optional `disperse_under_fire_s` (land only; omit = default
disperse duration for moving land, `0` disables).

#### Scenario: Static omit accepted
- **WHEN** a GA or recon Spec lists targets without a motion field
- **THEN** the Spec MUST validate (identical to pre-motion behaviour)

#### Scenario: Patrol shape accepted
- **WHEN** a target has `motion: patrol` and a valid `patrol_radius_m`
- **THEN** validation MUST succeed when other target rules pass

#### Scenario: Path shape accepted
- **WHEN** a target has `motion: path` with 2–6 airfield-relative points
- **THEN** validation MUST succeed when other target rules pass

### Requirement: Ground targets MAY declare AI and move options
Each GA or recon `targets[]` entry MAY include optional `ai_preset` (curated name)
and/or optional `ai` object with allowlisted keys (`roe`, `alarm_state`,
`engage_air_weapons`, `restrict_targets`, `interception_range` as applicable) and
optional land `move_formation` (`off_road` | `on_road` | `rank` | `cone` | `vee` |
documented siblings). Omit means today’s defaults (`#15g` disperse rules unchanged
when motion is non-static land). Explicit fields MUST override colliding preset
keys. Unknown preset or ai keys MUST be rejected. Sea targets MUST NOT set
`move_formation` or disperse-only land fields beyond existing disperse rules
(sea still skips disperse emit).

#### Scenario: Omit ai accepted
- **WHEN** a target omits `ai_preset`, `ai`, and `move_formation`
- **THEN** the Spec MUST validate (pre-`#15h` behaviour plus existing motion rules)

#### Scenario: Convoy preset accepted
- **WHEN** a soft-vehicle land target sets a curated convoy/transit preset or
  equivalent allowlisted `ai` + `move_formation`
- **THEN** validation MUST succeed when other target rules pass

#### Scenario: Unknown ai key rejected
- **WHEN** a target sets an `ai` key outside the allowlist
- **THEN** loading or validation MUST fail naming the unknown key
