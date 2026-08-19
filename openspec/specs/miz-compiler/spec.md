# Miz Compiler

## Purpose

The compiler turns a validated Mission Spec into a DCS `.miz` package deterministically.
No LLM emits mission Lua. PyDCS is the current backend and stays an implementation detail
behind a narrow interface.

## Requirements

### Requirement: Compile Mission Spec to .miz
The system SHALL provide a deterministic compiler that transforms a free-flight Mission Spec into a DCS `.miz` package without using an LLM to emit mission Lua.

#### Scenario: Successful compile of Manston example
- **WHEN** a user compiles the checked-in Manston cold free-flight Mission Spec
- **THEN** the system MUST write a `.miz` file that is a valid zip containing at least `mission`, `options`, `theatre`, and `warehouses` members

### Requirement: Spec theatre binds to PyDCS terrain
The compiler MUST construct the PyDCS mission terrain from an explicit binding of Spec
theatre id → terrain factory (not a silent Channel hardcode that ignores `spec.theatre`).
When the Spec theatre has no binding, compile MUST fail with a clear unbound-theatre
error and MUST NOT emit a `.miz` that uses a different terrain silently.

#### Scenario: Channel Spec uses Channel terrain
- **WHEN** a Mission Spec with theatre `TheChannel` is compiled
- **THEN** the compiler MUST construct a PyDCS Channel terrain for the mission

#### Scenario: Unbound theatre fails compile
- **WHEN** compile is asked to use a theatre id with no terrain binding
- **THEN** compile MUST fail without writing a successful mismatched-terrain `.miz`

### Requirement: Cold parking start at Manston
The compiler SHALL place the player Spitfire as a cold start from parking at Manston on The Channel.

#### Scenario: Cold parking placement
- **WHEN** the Mission Spec requests cold parking at Manston for `SpitfireLFMkIX` with skill Player
- **THEN** the compiled mission MUST use Channel theatre `TheChannel`, player type `SpitfireLFMkIX`, skill `Player`, and a parking cold-start (TakeOffParking / From Parking Area) at Manston

### Requirement: Time and weather from Mission Spec
The compiler SHALL apply Mission Spec start time and weather preset to the `.miz`.

#### Scenario: 09:00 sunny
- **WHEN** the Mission Spec sets start time to 09:00 and weather preset to `sunny_clear`
- **THEN** the compiled mission MUST use `start_time` 32400 and a clear/sunny weather configuration consistent with the preset

### Requirement: Radio frequency within the aircraft's band
The compiler SHALL assign each flight group a radio frequency the aircraft can tune, rather than relying on backend defaults.

#### Scenario: Spitfire on the Channel
- **WHEN** the Mission Spec places a Spitfire LF Mk IX
- **THEN** the compiled mission MUST set the group frequency inside Allied VHF (~100-156 MHz) — 124 MHz, matching the stock DCS Channel missions — and MUST NOT leave the PyDCS default of 251 MHz, which DCS rejects on launch

### Requirement: Compiler behind a narrow interface
The compiler implementation SHALL be reachable through a `CompilerInterface` (or equivalent) so the Mission Spec remains the public contract and PyDCS remains an interchangeable backend.

#### Scenario: Spec in, path out
- **WHEN** application code requests compilation of a Mission Spec
- **THEN** it MUST call the compiler interface with the Mission Spec and receive an output `.miz` path (or equivalent result) without depending on PyDCS types in the public Mission Spec model

### Requirement: CLI or entrypoint for compile
The system SHALL provide a documented command-line entrypoint to compile a Mission Spec file to a `.miz`.

#### Scenario: Compile from command line
- **WHEN** a developer runs the documented compile command against the Manston example Mission Spec
- **THEN** a `.miz` MUST be produced under the configured output directory (default `out/`)

### Requirement: Human acceptance in DCS
A compiled Manston cold free-flight `.miz` MUST be openable in the DCS Mission Editor and flyable as Instant Action / single mission with the player cold at Manston.

#### Scenario: Load in DCS
- **WHEN** a user opens the compiled `.miz` in DCS Mission Editor or Instant Action (with The Channel and Spitfire LF Mk IX installed)
- **THEN** the mission MUST load without editor errors and present the player as cold-started at Manston around 09:00 in clear weather

### Requirement: Free-flight compile ignores absent extension points
When compiling a free-flight Mission Spec, the compiler SHALL treat absent or empty `enemies`, `objectives`, and `triggers` as no-ops and MUST produce the same free-flight placement behaviour as before schema extension points were reserved.

#### Scenario: Manston example without extensions
- **WHEN** the checked-in Manston free-flight Mission Spec (with `schema_version` `"1"` and no extension payloads) is compiled
- **THEN** the system MUST write a `.miz` that places the player cold at Manston on The Channel with the Spec’s time and weather, and the `.miz` MUST remain openable in the DCS Mission Editor / Instant Action

### Requirement: Non-empty extension points not compiled yet
For free-flight Specs, the compiler (or loader, before compile) MUST NOT silently drop
non-empty `enemies` or `objectives`. Until a later change implements those capabilities for
free flight, non-empty combat values MUST cause a clear failure. Intercept Specs MAY compile
non-empty `enemies` / `objectives` per intercept requirements. Non-empty typed `triggers` /
`zones` MUST compile to native ME trigger tables (no silent drop).

#### Scenario: Free-flight non-empty enemies refused
- **WHEN** a free-flight Mission Spec includes a non-empty `enemies` collection
- **THEN** compilation MUST NOT produce a combat `.miz`, and the user MUST receive an error
  that free_flight requires empty combat extensions

### Requirement: Compiler resolves facts via Channel registry
The free-flight compiler SHALL resolve theatre support, player airfield →
`airdromeId` (for the Spec theatre), known aircraft checks, and group radio
frequency through the packaged registry API rather than private ad-hoc
constants inaccessible to other components.

#### Scenario: Manston compile still uses registry Manston=5
- **WHEN** the checked-in Manston free-flight Mission Spec is compiled
- **THEN** the compiler MUST obtain Manston’s `airdromeId` from the packaged
  registry for theatre `TheChannel` and the resulting `.miz` MUST still place
  the player cold at Manston (`airdromeId` 5) with Spitfire group frequency
  124.0 MHz and remain openable in DCS Mission Editor / Instant Action

### Requirement: Player airdrome resolved for Spec theatre
The compiler SHALL resolve the player airfield → `airdromeId` using the Spec
theatre’s packaged airfield map. It MUST NOT apply another theatre’s airdrome
id (for example Channel `Manston=5` on Normandy terrain).

#### Scenario: NeedsOarPoint compile uses Normandy map
- **WHEN** the checked-in Needs Oar Point cold free-flight Mission Spec is
  compiled
- **THEN** the compiler MUST obtain `NeedsOarPoint`’s `airdromeId` from the
  Normandy theatre package and the resulting `.miz` MUST place the player cold
  at airdromeId 28

#### Scenario: Wrong-theatre airfield does not compile
- **WHEN** a Mission Spec requests theatre `Normandy` and airfield `Manston`
- **THEN** compilation MUST NOT write a `.miz` (shared validation failure or
  equivalent registry error)

### Requirement: Compile uses shared validation engine
Before creating a `.miz`, the free-flight compiler SHALL run the shared Mission Spec validation
engine. If validation fails, compilation MUST NOT write a `.miz` and MUST surface the validation
errors (or an equivalent clear aggregate error) without inventing a second, divergent rule set for
registry/airfield/theatre checks.

#### Scenario: Invalid Spec does not produce a .miz
- **WHEN** a Mission Spec fails shared validation (for example unknown airfield)
- **THEN** the compiler MUST NOT write an output `.miz` file and MUST report the validation failure

#### Scenario: Valid Manston Spec still compiles
- **WHEN** the checked-in Manston free-flight Mission Spec passes shared validation
- **THEN** the compiler MUST still produce a `.miz` that places the player cold at Manston with
  Spitfire group frequency 124.0 MHz and remains openable in DCS Mission Editor / Instant Action

### Requirement: Manston compile covered by golden fixtures
The free-flight Manston acceptance compile path SHALL be covered by the repository’s
golden-fixture regression suite. Structural contracts previously asserted only in ad-hoc
compile tests (Channel theatre, Manston cold Spitfire placement, start time, VHF frequency,
required zip members) MUST remain enforced through that suite.

#### Scenario: Manston structural contracts still enforced
- **WHEN** the test suite runs after a compiler change that breaks Manston free-flight
  structure (for example wrong frequency or missing `theatre` member)
- **THEN** the golden-fixture (or equivalent Manston structural) tests MUST fail before the
  change is considered acceptable

### Requirement: Compile intercept Mission Spec to .miz
The compiler SHALL transform a validated intercept Mission Spec into a DCS `.miz` that places
the player flight and at least one enemy `Bf-109K-4` flight on The Channel, using registry
facts for aircraft ids and radio frequencies. It MUST NOT invent DCS identifiers. Free-flight
compile behaviour MUST remain unchanged for free-flight Specs. WWII Axis enemies MUST use
PyDCS country `ThirdReich` on red (not modern `Germany` on blue).

#### Scenario: Manston intercept example compiles
- **WHEN** the checked-in Manston intercept example Spec is compiled with Channel available
  in inventory
- **THEN** the system MUST write a `.miz` containing required zip members and mission content
  for player `SpitfireLFMkIX` and enemy `Bf-109K-4`, with in-band group frequencies from the
  Channel registry

#### Scenario: Free-flight Manston still compiles
- **WHEN** the checked-in Manston cold free-flight Spec is compiled
- **THEN** the compiler MUST still produce the accepted free-flight `.miz` behaviour

### Requirement: Human acceptance for intercept in DCS
A compiled intercept example `.miz` MUST be openable in the DCS Mission Editor and flyable
as Instant Action / single mission with The Channel, Spitfire LF Mk IX, and Bf-109K-4
available.

#### Scenario: Load intercept in DCS
- **WHEN** a user opens the compiled intercept `.miz` in DCS Mission Editor or Instant Action
- **THEN** the mission MUST load without editor errors and present the player and enemy
  flights as specified (Axis/red for Bf-109s)

### Requirement: Compile CAP Mission Spec to .miz
The compiler SHALL transform a validated CAP Mission Spec into a DCS `.miz` that places the
player flight cold at the Spec airfield on The Channel, sets the flight main task to CAP,
adds a patrol-station waypoint with an Orbit task (and OptROE from Spec engagement) at the
airfield-relative station, and — when `enemies` is non-empty — places those enemy flights.
It MUST NOT invent DCS identifiers. Free-flight and intercept compile behaviour MUST remain
unchanged for those Spec types. WWII Axis enemies MUST continue to use PyDCS country
`ThirdReich` on red.

#### Scenario: Manston CAP example compiles
- **WHEN** the checked-in Manston CAP example Spec is compiled with Channel available in
  inventory
- **THEN** the system MUST write a `.miz` containing required zip members, player
  `SpitfireLFMkIX` at Manston cold parking, CAP tasking with Orbit at the resolved station,
  and in-band Spitfire group frequency from the Channel registry

#### Scenario: Free-flight and intercept still compile
- **WHEN** the checked-in Manston free-flight or intercept Spec is compiled
- **THEN** the compiler MUST still produce the previously accepted behaviour for that type

### Requirement: Human acceptance for CAP in DCS
A compiled CAP example `.miz` MUST be openable in the DCS Mission Editor and flyable as
Instant Action / single mission with The Channel and Spitfire LF Mk IX available (and Bf-109
when the example includes enemies).

#### Scenario: Load CAP in DCS
- **WHEN** a user opens the compiled CAP `.miz` in DCS Mission Editor or Instant Action
- **THEN** the mission MUST load without editor errors and present the player CAP route /
  station (and any specified enemy flights)

### Requirement: Compile ground-attack Mission Spec to .miz
The compiler SHALL transform a validated ground-attack Mission Spec into a DCS `.miz` that
places the player flight cold at the Spec airfield on The Channel, applies the named
registry payload (verified bomb and — when selected — slipper-tank CLSIDs on Spitfire
pylons), sets the flight main task to GroundAttack, does not restrict fuel-tank jettison
(player may jettison in cockpit), adds ingress/target waypoints at the airfield-relative
strike point, and places
the declared **enemy** ground target unit group(s) on the opposing coalition only. It MUST
NOT invent DCS identifiers, MUST NOT place targets on the player's coalition, and MUST NOT
re-enable PyDCS install payload-directory scanning. Free-flight, intercept, and CAP compile
behaviour MUST remain unchanged for those Spec types. WWII Axis ground units MUST use PyDCS
country `ThirdReich` on red when the Spec says so.

#### Scenario: Manston ground-attack example compiles
- **WHEN** the checked-in Manston ground-attack example Spec is compiled with Channel
  available in inventory
- **THEN** the system MUST write a `.miz` containing required zip members, player
  `SpitfireLFMkIX` at Manston cold parking with bomb and slipper-tank loadout CLSIDs from
  the Channel-crossing payload preset, GroundAttack tasking toward the resolved strike
  point, placed ground targets, and in-band Spitfire group frequency from the Channel
  registry

#### Scenario: Prior mission types still compile
- **WHEN** the checked-in Manston free-flight, intercept, or CAP Spec is compiled
- **THEN** the compiler MUST still produce the previously accepted behaviour for that type

### Requirement: Human acceptance for ground-attack in DCS
A compiled ground-attack example `.miz` MUST be openable in the DCS Mission Editor and
flyable as Instant Action / single mission with The Channel and Spitfire LF Mk IX available.

#### Scenario: Load ground-attack in DCS
- **WHEN** a user opens the compiled ground-attack `.miz` in DCS Mission Editor or Instant
  Action
- **THEN** the mission MUST load without editor errors and present the player strike route,
  bomb loadout, and ground targets

### Requirement: Compile escort Mission Spec to .miz
The compiler SHALL transform a validated escort Mission Spec into a DCS `.miz` that places
the player flight cold at the Spec airfield on The Channel, places the friendly `package`
flight(s) inflight on a route toward the airfield-relative destination, sets the player
flight main task to Escort, attaches an Escort task action referencing the package group
id, applies Spec engagement as group ROE, and — when `enemies` is non-empty — places
opposing aircraft near the escort route / destination neighbourhood. It MUST NOT invent DCS
identifiers. Free-flight, intercept, CAP, and ground-attack compile behaviour MUST remain
unchanged for those Spec types.

#### Scenario: Manston escort example compiles
- **WHEN** the checked-in Manston escort example Spec is compiled with Channel available in
  inventory
- **THEN** the system MUST write a `.miz` containing required zip members, player
  `SpitfireLFMkIX` at Manston cold parking with Escort tasking and Escort task action linked
  to the package, placed friendly package aircraft, optional bounce enemies when declared,
  and in-band Spitfire group frequency from the Channel registry

#### Scenario: Prior mission types still compile
- **WHEN** the checked-in Manston free-flight, intercept, CAP, or ground-attack Spec is
  compiled
- **THEN** the compiler MUST still produce the previously accepted behaviour for that type

### Requirement: Human acceptance for escort in DCS
A compiled escort example `.miz` MUST be openable in the DCS Mission Editor and flyable as
Instant Action / single mission with The Channel and Spitfire LF Mk IX available (package
aircraft module as declared by the example).

#### Scenario: Load escort in DCS
- **WHEN** a user opens the compiled escort `.miz` in DCS Mission Editor or Instant Action
- **THEN** the mission MUST load without editor errors and present the player escort route,
  friendly package, and any declared bounce

### Requirement: Compile populates briefing l10n
On successful compile of any supported Mission Spec (free flight, intercept, CAP,
ground-attack, escort), the compiler SHALL write Sortie, Description, and player-coalition
Task text into the `.miz` localisation dictionary per the `mission-briefing` capability.
Compile MUST accept an optional squadron voice parameter for briefing register; when
omitted, briefing text MUST use default voice `raf`. Placement, weather, radio, and
mission-type tasking behaviour MUST otherwise remain unchanged.

#### Scenario: Manston free flight includes briefing text
- **WHEN** the checked-in Manston cold free-flight Spec is compiled
- **THEN** the `.miz` MUST include non-empty Sortie and Description dictionary entries and
  a non-empty player-coalition Task, and MUST still place the player cold at Manston with
  prior acceptance behaviour

#### Scenario: Optional voice reaches briefing
- **WHEN** compile is invoked with voice `usaaf` for a valid Channel Spec
- **THEN** the written briefing Task or Description MUST use USAAF commander register
  wording from the shared brief builder

### Requirement: Compile applies dawn and marginal weather
The compiler SHALL map Spec weather `dawn_clear` and `marginal_vfr` to distinct PyDCS
weather configurations (visibility and/or cloud density differing from `sunny_clear`).
Precipitation fields MUST use PyDCS perception enums (not raw integers). Unsupported
weather values MUST fail before writing a `.miz`.

#### Scenario: Dawn clear compile differs from sunny
- **WHEN** the dawn example Spec is compiled
- **THEN** the `.miz` weather configuration MUST differ from the sunny-clear free-flight
  example in visibility and/or cloud settings as designed

#### Scenario: Marginal VFR compile reduces visibility
- **WHEN** the marginal VFR example Spec is compiled
- **THEN** the `.miz` MUST reflect reduced visibility versus `sunny_clear` (marginal VFR
  band) and MUST still place the player per the Spec

#### Scenario: Sunny clear still compiles
- **WHEN** the Manston cold free-flight Spec (`sunny_clear`) is compiled
- **THEN** prior clear-weather behaviour MUST remain

### Requirement: Compiler emits gallery weather recipes
When compiling a Spec weather pattern whose recipe includes `cloud_preset`, the
compiler MUST set PyDCS `Weather.clouds_preset` via `CloudPreset.by_name`, clamp
cloud base to that preset’s allowed range, and apply recipe fog/visibility/temp/
QNH/turbulence/ground wind. Patterns without `cloud_preset` MAY keep the legacy
density/thickness path. Unsupported recipe preset ids MUST fail clearly before
writing a `.miz`.

#### Scenario: Rain overcast compiles with RainyPreset
- **WHEN** a Spec with a rain-overcast pattern is compiled
- **THEN** the mission weather table MUST include the corresponding rainy gallery
  preset string (e.g. `RainyPreset1`)

#### Scenario: Legacy sunny still compiles
- **WHEN** `examples/manston_cold_freeflight.yaml` (sunny_clear) is compiled
- **THEN** compile MUST succeed and prior clear-weather visibility behaviour MUST
  remain acceptable (high visibility, no fog unless recipe says otherwise)

### Requirement: Compile emits native zones and triggers
When a Mission Spec has non-empty `zones` or `triggers`, the compiler SHALL write
corresponding native DCS trigger zones and trigger rules into the `.miz` via PyDCS (or
equivalent). It MUST NOT refuse solely because triggers are present. Specs with empty
zones and triggers MUST keep prior compile behaviour.

#### Scenario: Time message sample compiles
- **WHEN** `examples/manston_freeflight_trigger_sample.yaml` is compiled
- **THEN** the `.miz` MUST contain a time-after condition and an out-text (message) action
  and MUST still place the player cold at Manston

#### Scenario: Empty triggers still compile
- **WHEN** the Manston cold free-flight Spec (empty triggers) is compiled
- **THEN** prior free-flight behaviour MUST remain

### Requirement: Spec vocabulary maps to ME predicates
The compiler SHALL map v1 Spec conditions/actions to native predicates: `time_more` to
time-after, `flag_is` to flag true/false, `flag_equals` / `flag_more` / `flag_less` to
numeric flag compare, `time_since_flag` to time-since-flag, `unit_dead` to group-dead for
the referenced enemy flight, `target_dead` to group-dead for the referenced ground/sea
target group, `group_life_less` to group-life-less for the referenced enemy or target
group at the Spec percent threshold, `coalition_in_zone` to part-of-coalition-in-zone,
`unit_altitude_higher` / `unit_altitude_lower` to unit-altitude higher/lower (AGL or MSL
per Spec `agl`) for the player unit, `unit_speed_higher` / `unit_speed_lower` to
unit-speed higher/lower for the player unit with Spec `speed_kmh` converted to m/s;
`message` to delayed out-text, `set_flag` to set/clear flag, `set_flag_value` /
`inc_flag` to set-flag-value / increase-flag, `set_flag_random` to set-flag-random
(Spec `min`/`max` → ME min_value/max_value), `mission_end` to end-mission with win/lose
for the player coalition, `sound` to sound-to-all with the resolved registry file
embedded in the `.miz` mapResource, `radio_item_add` / `radio_item_remove` to F10 radio
item add/remove (flag on for add), `activate_group` / `deactivate_group` to
activate/deactivate the referenced placed group, `mark` to mark-to-all for the referenced
zone with compiler-assigned mark id and Spec text, `smoke` to explosion/smoke-marker for
the referenced zone with curated color. Groups with Spec `late_activation: true` MUST be
written with ME late activation enabled. Unsupported types MUST fail clearly before
writing a `.miz`.

#### Scenario: Unknown mapping fails
- **WHEN** a future/unsupported condition type somehow reaches compile
- **THEN** compile MUST fail with a clear error and MUST NOT write a `.miz`

#### Scenario: target_dead maps to group dead
- **WHEN** a ground_attack Spec with a `target_dead` rule is compiled
- **THEN** the `.miz` MUST include a group-dead condition for the corresponding placed
  target group

#### Scenario: Radio and activate emit
- **WHEN** a Spec with `radio_item_add` and `activate_group` actions is compiled
- **THEN** the `.miz` MUST include corresponding radio-item and activate-group predicates

#### Scenario: Late activation on enemy group
- **WHEN** an enemy with `late_activation: true` is compiled
- **THEN** the placed group MUST be marked late-activated in the `.miz`

#### Scenario: Sound embeds and emits
- **WHEN** a Spec with a valid `sound` action is compiled
- **THEN** the `.miz` MUST include a sound-to-all action and MUST embed the resolved
  asset file in mission resources

#### Scenario: set_flag_random emits
- **WHEN** a Spec with `set_flag_random` is compiled
- **THEN** the `.miz` MUST include `a_set_flag_random` for the mapped flag id

#### Scenario: Numeric flag emit
- **WHEN** a Spec with `flag_more` and `inc_flag` (or `set_flag_value`) is compiled
- **THEN** the `.miz` MUST include corresponding numeric flag condition and action
  predicates

#### Scenario: group_life_less emit
- **WHEN** a Spec with a valid `group_life_less` condition is compiled
- **THEN** the `.miz` MUST include a group-life-less condition for the corresponding
  placed group at the Spec percent

#### Scenario: mark emit
- **WHEN** a Spec with a valid `mark` action is compiled
- **THEN** the `.miz` MUST include a mark-to-all action for the referenced zone

#### Scenario: smoke emit
- **WHEN** a Spec with a valid `smoke` action is compiled
- **THEN** the `.miz` MUST include a smoke-marker (explosion marker) action for the
  referenced zone

#### Scenario: altitude gate emit
- **WHEN** a Spec with a valid `unit_altitude_higher` (or lower) condition is compiled
- **THEN** the `.miz` MUST include the corresponding unit-altitude predicate for the
  player unit

#### Scenario: speed gate emit
- **WHEN** a Spec with a valid `unit_speed_higher` (or lower) condition is compiled
- **THEN** the `.miz` MUST include the corresponding unit-speed predicate for the player
  unit

### Requirement: Compiler expands dynamics before .miz emit
The PyDCS compiler path MUST run the same dynamics expansion used by validation so the
saved `.miz` contains the expanded native trigger tables (dice and/or radio + activate),
not an unexpanded `dynamics` declaration alone.

#### Scenario: Live dynamics example compiles with Set Flag Random
- **WHEN** a packaged live-dynamics example Spec is compiled
- **THEN** the mission member MUST include Set Flag Random (or equivalent PyDCS emit)
  and activate-group actions for pool branches

### Requirement: Compiler applies invent weather snapshot
Before writing weather into the `.miz`, the compiler MUST apply the invent-
resolved weather snapshot for the Spec (gallery clamp, fog, temp, QNH, turb,
wind layers as present). Given the same Spec including `weather_opts.seed`,
compile MUST be deterministic. Unsupported gallery ids in a snapshot MUST fail
clearly before writing a `.miz`.

#### Scenario: Pinned seed compile stable
- **WHEN** a gallery-pattern Spec with `weather_opts.seed` set is compiled twice
- **THEN** the mission weather table fields covered by the snapshot MUST match
  between runs

#### Scenario: Legacy sunny with seed still compiles
- **WHEN** `sunny_clear` with an explicit seed is compiled
- **THEN** compile MUST succeed without assigning a rainy gallery preset

### Requirement: Compiler applies shared weather snapshot helper
The compiler weather apply path SHALL use a shared helper that can also apply an
invent `WeatherSnapshot` to an already-loaded PyDCS Mission (for re-weather
miz-patch), including gallery clamp and wind layers.

#### Scenario: Snapshot apply reusable
- **WHEN** a WeatherSnapshot is applied to a loaded Mission
- **THEN** cloud preset / fog / wind fields MUST match invent compile behaviour
  for the same snapshot

### Requirement: Compiler emits curated fog animation script
When `fog_dynamics` is set, the compiler MUST emit a native ONCE trigger that
fires after `start_after_s` and runs curated Lua calling
`world.weather.setFogAnimation` with params derived only from Spec fields
(prefer `DoScriptFile` + miz resource over DictKey `DoScript`). Unsupported
modes MUST fail before writing a `.miz`. The Lua text MUST come from a
human-authored template, not from the LLM.

#### Scenario: Burn-off emits setFogAnimation
- **WHEN** a Spec with `fog_dynamics.mode: burn_off` is compiled
- **THEN** the `.miz` MUST contain `setFogAnimation` (mission resource and/or
  trigger wiring) and the configured duration

### Requirement: Compiler emits multi-unit player flight
When `player.flight` is present with `role: lead` (or default), the compiler SHALL
create one player aircraft group with `group_size` equal to Spec `size`, place all
units at the Spec airfield with the Spec start type and aircraft id, set the first
unit to skill `Player`, and set all other units to Spec `ai_skill` (default
`Average`). When `role: wingman`, the compiler SHALL emit **two** groups: an AI lead
group of size `size - 1` (all `ai_skill`) named distinctly from the player group, and
a size-1 player group with skill `Player` on its first (only) unit — MUST NOT place
`Player` on a non-first unit of a mixed group (DCS single-player will not hand control).
Group radio frequency and mission-type tasking MUST apply to the player group.
When `player.flight` is omitted, the compiler MUST emit a single-unit Player group as
today. Player-bound trigger conditions MUST use the human unit id (player group unit 0).

#### Scenario: Lead four-ship compile
- **WHEN** compiling a free-flight Spec with `player.flight.size: 4` and `role: lead`
- **THEN** the `.miz` MUST contain a player group of four `SpitfireLFMkIX` units with the
  first unit skill `Player` and the other three AI-skilled, cold at the Spec airfield

#### Scenario: Wingman pair compile
- **WHEN** compiling a Spec with `player.flight.size: 2` and `role: wingman`
- **THEN** the `.miz` MUST contain a separate AI lead group (one AI-skilled unit) and a
  size-1 player group with skill `Player` on its only unit

#### Scenario: Solo unchanged
- **WHEN** compiling a Spec that omits `player.flight`
- **THEN** the compiler MUST still emit a one-unit Player group as before

### Requirement: Wingman join-up Follow and shared route
When `player.flight.role` is `wingman` and `join_up` is enabled, the compiler SHALL
(1) place mission route/tasking (CAP / ground-attack / escort, and a minimal
free-flight outbound leg for free_flight) on the **AI lead** group, and (2) add a
native ME **Follow** task on the **player** group targeting that AI lead group id
(PyDCS `Follow`). The player group MUST remain size-1 with skill `Player`. When
`join_up` is false, behaviour MUST match `#15b` (tasks on player group, no Follow).
`role: lead` multi-unit groups MUST NOT require Follow for cohesion.

#### Scenario: Wingman free-flight Follow
- **WHEN** compiling a free-flight Spec with wingman + join_up
- **THEN** the `.miz` MUST contain a Follow action referencing the AI lead group and
  an outbound waypoint on the AI lead group

#### Scenario: Wingman CAP tasking on lead
- **WHEN** compiling a CAP Spec with wingman + join_up
- **THEN** CAP orbit/route tasking MUST be on the AI lead group and the player group
  MUST Follow that lead

#### Scenario: Join-up opt-out
- **WHEN** compiling wingman with `join_up: false`
- **THEN** the player group MUST NOT have a Follow-to-lead task from this feature

### Requirement: Compiler emits Failures panel table
For each Spec `failures` entry, the compiler SHALL write a mission-root Failures
panel row (`mission.failures`) with `enable` true, `id`, `prob` from `probability`,
After time from `start_after_s` floored to minutes (`hh`/`mm`), and Within minutes
`mmint` from `random_pause_s` using `max(1, ceil(seconds/60))` (Within 0 MUST NOT
be emitted — it never fires). No Lua and no `a_set_failure` triggers MUST be emitted
for this feature. When `failures` is omitted or empty, the compiler MUST NOT add
enabled failure rows from this feature.

#### Scenario: Magneto at T+120
- **WHEN** compiling a Spec with one failure id `ENG0_MAGNETO0` and
  `start_after_s: 120`
- **THEN** the `.miz` MUST contain an enabled `ENG0_MAGNETO0` Failures table entry
  with After 0 hours / 2 minutes and Within at least 1 minute

### Requirement: Compiler emits section-order F10 packs
When `player.flight.orders` is non-empty, the compiler SHALL emit F10 radio items
and flag→AI-task wiring for each curated order id, targeting AI mates (lead) or
the AI lead group (wingman). Emit MUST use native ME / PyDCS tasks — no LLM Lua.
When `orders` is omitted or empty, the compiler MUST NOT add this feature's F10
order pack.

#### Scenario: Rejoin order wired
- **WHEN** compiling a Spec with `orders` containing `rejoin`
- **THEN** the `.miz` MUST contain a radio item for section rejoin and Follow (or
  equivalent) task wiring for the AI section

### Requirement: Compiler emits showers scattered gallery weather
When compiling a Spec with `weather: showers_scattered`, the compiler MUST apply
the invent-resolved weather snapshot and set a rainy light gallery
`cloud_preset` from that pattern’s allowed family (via existing
`CloudPreset.by_name` / base clamp path).

#### Scenario: Showers compiles with light-rain gallery
- **WHEN** a Spec with `weather: showers_scattered` and a pinned
  `weather_opts.seed` is compiled
- **THEN** the mission weather table MUST include a gallery preset string from
  the showers family (e.g. `RainyPreset4` or `NEWRAINPRESET4`)

### Requirement: Compiler emits fail-to-follow discipline
When `player.flight.discipline` is armed, the compiler SHALL emit native
moving-zone + flag/message wiring that soft-warns the player after sustained
time outside the AI-lead bubble, then applies the curated hard action after
further time outside. Emit MUST NOT use LLM-authored Lua. When discipline is
omitted, the compiler MUST NOT add this feature's discipline pack. Soft warn
SHOULD set the `#15d` rejoin flag when `orders` includes `rejoin`.

#### Scenario: Soft warn wired
- **WHEN** compiling a wingman+join_up Spec with discipline armed
- **THEN** the `.miz` MUST contain moving-zone / outside-zone (or equivalent)
  conditions and a rejoin/soft-warn message path

### Requirement: Compile recon missions
The compiler SHALL compile a validated `mission_type: recon` Spec into a Channel `.miz`
with player `SpitfireLFMkIX` cold at the declared airfield, group task
`Reconnaissance`, ingress toward the airfield-relative AOI, an AOI trigger zone sized from
`recon.radius_m`, weapons-hold (or equivalent observe) ROE, and no bomb/payload CLSIDs.
When `targets` is non-empty, the compiler MUST place contact groups near the AOI without
GroundAttack/Bombing/AttackGroup tasking. The compiler MUST emit a native find beat:
player-coalition `coalition_in_zone` on the AOI → message instructing observe complete /
RTB (and MAY set a reserved flag). Free-form Lua MUST NOT be used.

#### Scenario: Manston recon compiles
- **WHEN** `examples/manston_recon.yaml` (or equivalent) is compiled
- **THEN** the `.miz` MUST include Reconnaissance tasking, an AOI zone, no bomb CLSIDs, and
  a find-zone message (or equivalent trigger comment/text)

#### Scenario: Contacts placed without attack tasking
- **WHEN** a recon Spec includes opposing-coalition truck contacts
- **THEN** the `.miz` MUST contain those unit types near the AOI and MUST NOT attach
  GroundAttack or Bombing attack tasks for the player strike path

### Requirement: Compile places U-boat ship groups on sea AOI/strike
For validated recon or ground_attack Specs that list `Uboat_VIIC` targets on sea-domain
geometry, the compiler MUST place PyDCS ship groups of that type near the AOI/strike
point (existing sea placement path). Free-form Lua MUST NOT be required.

#### Scenario: Recon U-boat contacts compile as ships
- **WHEN** a recon Spec with mid-Channel `Uboat_VIIC` contacts is compiled
- **THEN** the `.miz` MUST contain `Uboat_VIIC` ship unit(s) near the AOI

#### Scenario: GA U-boat targets compile as ships
- **WHEN** a ground_attack Spec with mid-Channel `Uboat_VIIC` targets is compiled
- **THEN** the `.miz` MUST contain `Uboat_VIIC` ship unit(s) near the strike point

### Requirement: Compiler emits native waypoints for target motion
For each non-static `targets[]` entry, the compiler MUST add native ME route
waypoints on the placed ship or vehicle group (PyDCS `add_waypoint` or equivalent).
`patrol` MUST produce a looping route around the AOI/strike placement within
`patrol_radius_m`. `path` MUST place the group along the Spec waypoints and loop.
Static/omit MUST NOT add motion waypoints. Free-form Lua MUST NOT be required.
Player GroundAttack Bombing MAY remain aimed at the fixed strike point in v1.
Cruise speeds MUST come from curated bands (seeded pick or Spec `speed_kmh`).
Moving land groups MUST receive Disperse Under Fire (ME option) by default unless
disabled via Spec.

#### Scenario: U-boat patrol compiles with ship waypoints
- **WHEN** a mid-Channel Spec with `Uboat_VIIC` and `motion: patrol` is compiled
- **THEN** the `.miz` MUST contain `Uboat_VIIC` and multiple route points for that group

#### Scenario: Truck path compiles with vehicle waypoints
- **WHEN** a land GA Spec with soft-vehicle `motion: path` is compiled
- **THEN** the `.miz` MUST contain that vehicle type and multiple route points

#### Scenario: Moving land convoy gets Disperse Under Fire
- **WHEN** a soft-vehicle path Spec is compiled without disabling disperse
- **THEN** the `.miz` MUST include Disperse Under Fire / option id 8 on the group route

#### Scenario: Static target unchanged
- **WHEN** a Spec target omits motion
- **THEN** the group MUST be placed without a multi-point motion route (same as today)

### Requirement: Compiler emits Opt* and PointAction for target AI
For each target with non-empty resolved AI / move_formation (after preset
expand), the compiler MUST attach native PyDCS option tasks on the placed
ship or vehicle group (prefer first waypoint) and MUST set land waypoint
`PointAction` when `move_formation` is set (including all motion route points).
Emit MUST use allowlisted Opt* only (e.g. `OptROE`, `OptAlarmState`,
`OptEngageAirWeapons`, `OptRestrictTargets`, `OptInterceptionRange` where
class allows). Free-form Lua MUST NOT be required. Targets that omit AI MUST
retain `#15g` motion/disperse behaviour only.

#### Scenario: Convoy Alarm and Off/On Road compile
- **WHEN** a soft-vehicle path Spec with alarm and move_formation is compiled
- **THEN** the `.miz` MUST include the corresponding option wiring and Action
  string for the vehicle route

#### Scenario: U-boat ROE and Alarm compile
- **WHEN** a sea Spec with U-boat ai roe/alarm is compiled
- **THEN** the `.miz` MUST include those options on the ship group route

#### Scenario: Static omit unchanged
- **WHEN** a Spec target omits ai and move_formation
- **THEN** compile MUST NOT add new AI option tasks beyond existing motion/disperse rules

### Requirement: Normandy Spec binds to Normandy terrain
The compiler MUST construct PyDCS Normandy terrain when compiling a Mission Spec
with theatre `Normandy`.

#### Scenario: Normandy Spec uses Normandy terrain
- **WHEN** a Mission Spec with theatre `Normandy` is compiled
- **THEN** the compiler MUST construct a PyDCS Normandy terrain for the mission

### Requirement: Cold parking freeflight at Needs Oar Point
The compiler SHALL place the player Spitfire as a cold start from parking at
Needs Oar Point on Normandy when the Spec requests that combination.

#### Scenario: Cold parking at NeedsOarPoint
- **WHEN** the Mission Spec requests cold parking at `NeedsOarPoint` for
  `SpitfireLFMkIX` with skill Player and theatre `Normandy`
- **THEN** the compiled mission MUST use Normandy theatre, player type
  `SpitfireLFMkIX`, skill `Player`, and parking cold-start at Needs Oar Point
  (airdromeId 28)

### Requirement: Human acceptance on Normandy 2.0
A compiled Needs Oar Point cold free-flight `.miz` MUST be openable in the DCS
Mission Editor and flyable as Instant Action with Normandy 2.0 and Spitfire LF
Mk IX installed.

#### Scenario: Load Normandy smoke in DCS
- **WHEN** a user opens the compiled Normandy cold freeflight `.miz` in DCS ME
  or Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Needs Oar Point around 09:00 in clear weather

### Requirement: Intercept enemy spawn is TheChannel-only
The compiler SHALL use the packaged intercept spawn recipe for Spec theatre
`TheChannel` (Hawkinge + Dover-approach offset), `Normandy` (NeedsOarPoint
+ 180° / 63 km), and `Caucasus` (Batumi + 270° / 40 km). Other theatres MUST
fail closed. Channel enemy coordinates MUST remain the existing Hawkinge
golden pair.

#### Scenario: Channel intercept still uses Hawkinge recipe
- **WHEN** a TheChannel intercept Spec is compiled
- **THEN** enemy placement MUST still use the existing Hawkinge anchor plus
  Dover-approach offset (golden `x=30989.935547`, `y=-35402.577148`)

### Requirement: Compile intercept at Needs Oar Point
The compiler SHALL compile a Normandy intercept Mission Spec that cold-starts
the player Spitfire at Needs Oar Point and places Bf-109K-4 enemies inflight
on the packaged Cherbourg-corridor recipe (NeedsOarPoint + 180° / 63 km). It
MUST bind PyDCS `Normandy` terrain. It MUST NOT write Channel Hawkinge/Dover
coordinates.

#### Scenario: Needs Oar Point intercept contracts
- **WHEN** `examples/needs_oar_point_dawn_intercept.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Normandy`, player type
  `SpitfireLFMkIX`, `airdromeId` 28, cold parking, start_time 21600, player
  radio 124.0 MHz, and enemy `Bf-109K-4` at 40.0 MHz

### Requirement: Compile intercept at Batumi
The compiler SHALL compile a Caucasus intercept Mission Spec that cold-starts
the player Su-25T at Batumi and places Russia Su-25T enemies inflight on the
packaged Black Sea recipe (Batumi + 270° / 40 km). It MUST bind PyDCS
`Caucasus` terrain. It MUST NOT write Channel Hawkinge/Dover coordinates.

#### Scenario: Batumi intercept contracts
- **WHEN** `examples/batumi_dawn_intercept.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Caucasus`, player type `Su-25T`,
  `airdromeId` 22, cold parking, start_time 21600, player radio 251.0 MHz,
  country `Russia`, and enemy coordinates `-355810.6875`, `577386.1875`

### Requirement: Human acceptance for Caucasus intercept in DCS
A compiled Batumi intercept `.miz` MUST be openable in the DCS Mission Editor
and flyable as Instant Action with Caucasus and Su-25T installed. This is
human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Caucasus intercept in DCS
- **WHEN** a user opens the compiled Caucasus intercept `.miz` in DCS ME or
  Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Batumi with bandits west over the Black Sea

### Requirement: Compile escort at Needs Oar Point
The compiler SHALL compile a Normandy escort Mission Spec that cold-starts
the player Spitfire at Needs Oar Point and flies a Mosquito package to the
packaged Cherbourg-corridor station (180° / 63 km / 4000 m) with optional
Bf-109K-4 bounce. It MUST bind PyDCS `Normandy` terrain. It MUST NOT write
Channel Manston escort 120/55 as the required destination.

#### Scenario: Needs Oar Point escort contracts
- **WHEN** `examples/needs_oar_point_escort.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Normandy`, player type
  `SpitfireLFMkIX`, `airdromeId` 28, cold parking, start_time 32400, player
  radio 124.0 MHz, package `MosquitoFBMkVI`, Escort tasking, and enemy
  `Bf-109K-4` at 40.0 MHz when enemies are present

### Requirement: Compile escort at Batumi
The compiler SHALL compile a Caucasus escort Mission Spec that cold-starts
the player Su-25T at Batumi and flies a Georgia Su-25T package to the
packaged Black Sea station (270° / 40 km / 4000 m) with optional Russia
Su-25T bounce. It MUST bind PyDCS `Caucasus` terrain. It MUST NOT write
Channel Manston escort 120/55 as the required destination.

#### Scenario: Batumi escort contracts
- **WHEN** `examples/batumi_black_sea_escort.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Caucasus`, player type `Su-25T`,
  `airdromeId` 22, cold parking, start_time 32400, player radio 251.0 MHz,
  Escort tasking, country `Georgia` on the package, and country `Russia` when
  enemies are present

### Requirement: Compile recon at Batumi
The compiler SHALL compile a Caucasus recon Mission Spec that cold-starts
the player Su-25T at Batumi and observes land contacts at the packaged
Kutaisi-inland AOI (43° / 110 km / 2000 m) with weapons hold. It MUST bind
PyDCS `Caucasus` terrain. It MUST NOT require Channel french-coast 125/76
or Black Sea CAP 270/40 as the AOI.

#### Scenario: Batumi recon contracts
- **WHEN** `examples/batumi_kutaisi_recon.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Caucasus`, player type
  `Su-25T`, `airdromeId` 22, cold parking, start_time 32400, player
  radio 251.0 MHz, Reconnaissance tasking, `Ural-375`, and recon AOI
  find-beat tokens

### Requirement: Human acceptance for Caucasus escort in DCS
A compiled Batumi escort `.miz` MUST be openable in the DCS Mission Editor
and flyable as Instant Action with Caucasus and Su-25T installed. This is
human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Caucasus escort in DCS
- **WHEN** a user opens the compiled Caucasus escort `.miz` in DCS ME or
  Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Batumi with a package west over the Black Sea

### Requirement: Compile recon at Needs Oar Point
The compiler SHALL compile a Normandy recon Mission Spec that cold-starts
the player Spitfire at Needs Oar Point and observes land contacts at the
packaged Maupertus-inland AOI (180° / 133 km / 2000 m) with weapons hold.
It MUST bind PyDCS `Normandy` terrain. It MUST NOT require Channel
french-coast 125/76 as the AOI.

#### Scenario: Needs Oar Point recon contracts
- **WHEN** `examples/needs_oar_point_recon.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Normandy`, player type
  `SpitfireLFMkIX`, `airdromeId` 28, cold parking, start_time 32400, player
  radio 124.0 MHz, Reconnaissance tasking, `Blitz_36-6700A`, and recon AOI
  find-beat tokens

### Requirement: Join-up outbound bearing stays airfield-relative
Wingman join-up outbound SHALL remain an airfield-relative heading default
(120°) on any bound theatre that compiles a player flight with join-up. It
MUST NOT be treated as Channel-only intercept spawn geometry.

#### Scenario: Normandy free_flight join-up still compiles
- **WHEN** a Normandy NeedsOarPoint free-flight Spec includes a wingman
  join-up
- **THEN** the compiler MUST still be allowed to emit Follow / outbound
  using the generic airfield-relative bearing

### Requirement: Compile CAP at Needs Oar Point
The compiler SHALL compile a Normandy CAP Mission Spec that cold-starts the
player Spitfire at Needs Oar Point and orbits the packaged CAP station
(180° / 63 km / 4000 m) with optional Bf-109K-4 opposition. It MUST bind
PyDCS `Normandy` terrain (not `Normandy2` or TheChannel). It MUST NOT write
Channel Hawkinge/Dover intercept coordinates.

#### Scenario: Needs Oar Point CAP contracts
- **WHEN** `examples/needs_oar_point_cap.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Normandy`, player type
  `SpitfireLFMkIX`, `airdromeId` 28, cold parking, start_time 32400, CAP Orbit
  Circle, player radio 124.0 MHz, and enemy `Bf-109K-4` at 40.0 MHz when
  enemies are present

### Requirement: Human acceptance for Normandy CAP in DCS
A compiled Needs Oar Point CAP `.miz` MUST be openable in the DCS Mission
Editor and flyable as Instant Action with Normandy 2.0 and Spitfire LF Mk IX
installed. This is human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Normandy CAP in DCS
- **WHEN** a user opens the compiled Normandy CAP `.miz` in DCS ME or Instant
  Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Needs Oar Point with a CAP station south toward Cherbourg

### Requirement: Compile ground-attack at Needs Oar Point
The compiler SHALL compile a Normandy ground-attack Mission Spec that
cold-starts the player Spitfire at Needs Oar Point with the named Channel
crossing payload, GroundAttack tasking toward the airfield-relative strike
point inland of Maupertus, and declared Axis land target groups. It MUST bind
PyDCS `Normandy` terrain (not `Normandy2` or TheChannel). It MUST NOT write
Channel Hawkinge/Dover intercept coordinates. WWII Axis ground units MUST use
PyDCS country `ThirdReich` on red when the Spec says so.

#### Scenario: Needs Oar Point ground-attack contracts
- **WHEN** `examples/needs_oar_point_ground_attack.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Normandy`, player type
  `SpitfireLFMkIX`, `airdromeId` 28, cold parking, start_time 32400, player
  radio 124.0 MHz, GroundAttack tasking, and target types `Blitz_36-6700A`
  and `flak18`

### Requirement: Human acceptance for Normandy ground-attack in DCS
A compiled Needs Oar Point ground-attack `.miz` MUST be openable in the DCS
Mission Editor and flyable as Instant Action with Normandy 2.0 and Spitfire
LF Mk IX installed. This is human do-soon after merge, not a hermetic merge
gate.

#### Scenario: Load Normandy ground-attack in DCS
- **WHEN** a user opens the compiled Normandy ground-attack `.miz` in DCS ME
  or Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Needs Oar Point with a strike inland of Maupertus

### Requirement: Caucasus Spec binds to Caucasus terrain
The compiler MUST construct PyDCS Caucasus terrain when compiling a Mission
Spec with theatre `Caucasus`.

#### Scenario: Caucasus Spec uses Caucasus terrain
- **WHEN** a Mission Spec with theatre `Caucasus` is compiled
- **THEN** the compiler MUST construct a PyDCS Caucasus terrain for the
  mission

### Requirement: Cold parking freeflight at Batumi
The compiler SHALL place the player Su-25T as a cold start from parking at
Batumi on Caucasus when the Spec requests that combination. Group radio MUST
be 251.0 MHz.

#### Scenario: Cold parking at Batumi
- **WHEN** the Mission Spec requests cold parking at `Batumi` for `Su-25T`
  with skill Player, country Georgia, and theatre `Caucasus`
- **THEN** the compiled mission MUST use Caucasus theatre, player type
  `Su-25T`, skill `Player`, frequency 251.0, and parking cold-start at
  Batumi (airdromeId 22)

### Requirement: Cold parking Spitfire freeflight at Batumi
The compiler SHALL place the player Spitfire LF Mk IX as a cold start from
parking at Batumi on Caucasus when the Spec requests that combination.
Group radio MUST be 124.0 MHz. It MUST bind PyDCS `Caucasus` terrain.

#### Scenario: Batumi Spitfire contracts
- **WHEN** `examples/batumi_spitfire_freeflight.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Caucasus`, player type
  `SpitfireLFMkIX`, `airdromeId` 22, cold parking, start_time 32400, and
  player radio 124.0 MHz

### Requirement: Cold parking freeflight at Mozdok
The compiler SHALL place the player Su-25T as a cold start from parking at
Mozdok on Caucasus when the Spec requests that combination. Group radio MUST
be 251.0 MHz. Player country `Russia` MUST be on coalition red. It MUST bind
PyDCS `Caucasus` terrain. It MUST NOT write Normandy `airdromeId` 28 as
Needs Oar Point.

#### Scenario: Needs Mozdok contracts
- **WHEN** `examples/mozdok_cold_freeflight.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Caucasus`, player type `Su-25T`,
  `airdromeId` 28, cold parking, start_time 32400, player radio 251.0 MHz,
  and country `Russia`

### Requirement: Human acceptance on Caucasus
A compiled Batumi cold free-flight `.miz` MUST be openable in the DCS Mission
Editor and flyable as Instant Action with Caucasus and Su-25T installed. This
is human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Caucasus smoke in DCS
- **WHEN** a user opens the compiled Caucasus cold freeflight `.miz` in DCS ME
  or Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Batumi around 09:00 in clear weather

### Requirement: Compile CAP at Batumi
The compiler SHALL compile a Caucasus CAP Mission Spec that cold-starts the
player Su-25T at Batumi and orbits the packaged CAP station
(270° / 40 km / 4000 m) with optional Russia Su-25T opposition. It MUST bind
PyDCS `Caucasus` terrain. Group radio MUST be 251.0 MHz. It MUST NOT write
Channel Hawkinge/Dover or Normandy Cherbourg intercept coordinates.

#### Scenario: Batumi CAP contracts
- **WHEN** `examples/batumi_black_sea_cap.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Caucasus`, player type `Su-25T`,
  `airdromeId` 22, cold parking, start_time 32400, CAP Orbit Circle, player
  radio 251.0 MHz, and country `Russia` when enemies are present

### Requirement: Human acceptance for Caucasus CAP in DCS
A compiled Batumi CAP `.miz` MUST be openable in the DCS Mission Editor and
flyable as Instant Action with Caucasus and Su-25T installed. This is human
do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Caucasus CAP in DCS
- **WHEN** a user opens the compiled Caucasus CAP `.miz` in DCS ME or Instant
  Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Batumi with a CAP station west over the Black Sea

### Requirement: Compile ground-attack at Batumi
The compiler SHALL compile a Caucasus ground-attack Mission Spec that
cold-starts the player Su-25T at Batumi with the named FAB-250 payload,
GroundAttack tasking toward the airfield-relative strike point inland past
Kutaisi, and declared Russia land target groups. It MUST bind PyDCS
`Caucasus` terrain (not TheChannel or Normandy). It MUST NOT write Channel
Hawkinge/Dover intercept coordinates. Modern ground units MUST use PyDCS
country `Russia` on red when the Spec says so.

#### Scenario: Batumi ground-attack contracts
- **WHEN** `examples/batumi_kutaisi_ground_attack.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Caucasus`, player type `Su-25T`,
  `airdromeId` 22, cold parking, start_time 32400, player radio 251.0 MHz,
  GroundAttack tasking, target type `Ural-375`, country Russia, and FAB-250
  CLSID `{3C612111-C7AD-476E-8A8E-2485812F4E5C}`

### Requirement: Human acceptance for Caucasus ground-attack in DCS
A compiled Batumi ground-attack `.miz` MUST be openable in the DCS Mission
Editor and flyable as Instant Action with Caucasus and Su-25T installed. This
is human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Caucasus ground-attack in DCS
- **WHEN** a user opens the compiled Caucasus ground-attack `.miz` in DCS ME
  or Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Batumi with a strike inland past Kutaisi

### Requirement: Syria Spec binds to Syria terrain
The compiler MUST construct PyDCS Syria terrain when compiling a Mission
Spec with theatre `Syria`.

#### Scenario: Syria Spec uses Syria terrain
- **WHEN** a Mission Spec with theatre `Syria` is compiled
- **THEN** the compiler MUST construct a PyDCS Syria terrain for the
  mission

### Requirement: Cold parking freeflight at Incirlik
The compiler SHALL place the player Su-25T as a cold start from parking at
Incirlik on Syria when the Spec requests that combination. Group radio MUST
be 251.0 MHz.

#### Scenario: Cold parking at Incirlik
- **WHEN** the Mission Spec requests cold parking at `Incirlik` for `Su-25T`
  with skill Player, country Turkey, and theatre `Syria`
- **THEN** the compiled mission MUST use Syria theatre, player type
  `Su-25T`, skill `Player`, frequency 251.0, and parking cold-start at
  Incirlik (airdromeId 16)

### Requirement: Compile freeflight at Palmyra
The compiler SHALL compile a Syria free-flight Mission Spec that cold-starts
the player Su-25T at Palmyra with country `Syria` on red. It MUST bind
PyDCS `Syria` terrain. It MUST write `airdromeId` 28 on the Syria theatre
(not Caucasus Mozdok, not Normandy Needs Oar Point).

#### Scenario: Palmyra freeflight contracts
- **WHEN** `examples/palmyra_cold_freeflight.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Syria`, player type `Su-25T`,
  `airdromeId` 28, cold parking, start_time 32400, player radio 251.0 MHz,
  and country `Syria`

### Requirement: Compile CAP at Incirlik
The compiler SHALL compile a Syria CAP Mission Spec that cold-starts the
player Su-25T at Incirlik and patrols the packaged Iskenderun station
(180° / 40 km / 4000 m) with optional Syria Su-25T opposition. It MUST bind
PyDCS `Syria` terrain. It MUST NOT require Batumi 270/40 or Cherbourg 180/63
as the station.

#### Scenario: Incirlik CAP contracts
- **WHEN** `examples/incirlik_iskenderun_cap.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Syria`, player type `Su-25T`,
  `airdromeId` 16, cold parking, start_time 32400, player radio 251.0 MHz,
  CAP tasking, and country `Syria` when enemies are present

### Requirement: Compile intercept at Incirlik
The compiler SHALL compile a Syria intercept Mission Spec that cold-starts
the player Su-25T at Incirlik and places opposition on the packaged
Iskenderun corridor (Incirlik + 180° / 40 km). Channel Hawkinge/Dover
literals MUST stay bit-identical.

#### Scenario: Incirlik intercept contracts
- **WHEN** `examples/incirlik_dawn_intercept.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Syria`, player type `Su-25T`,
  `airdromeId` 16, start_time 21600, player radio 251.0 MHz, country `Syria`
  when enemies are present, and enemy map position 181207.773438 /
  -35240.347656 (MUST NOT contain Channel 30989.935547)

### Requirement: Compile escort at Incirlik
The compiler SHALL compile a Syria escort Mission Spec that cold-starts
the player Su-25T at Incirlik and flies a Turkey Su-25T package to the
packaged Iskenderun station (180° / 40 km / 4000 m) with optional Syria
Su-25T bounce. It MUST bind PyDCS `Syria` terrain. It MUST NOT write
Channel Manston escort 120/55 as the required destination.

#### Scenario: Incirlik escort contracts
- **WHEN** `examples/incirlik_iskenderun_escort.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Syria`, player type `Su-25T`,
  `airdromeId` 16, cold parking, start_time 32400, player radio 251.0 MHz,
  Escort tasking, country `Turkey` on the package, and country `Syria` when
  enemies are present

### Requirement: Human acceptance for Syria escort in DCS
A compiled Incirlik escort `.miz` MUST be openable in the DCS Mission Editor
and flyable as Instant Action with Syria and Su-25T installed. This is
human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Syria escort in DCS
- **WHEN** a user opens the compiled Syria escort `.miz` in DCS ME or
  Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Incirlik with a package south over the Gulf of Iskenderun

### Requirement: Compile ground_attack at Incirlik
The compiler SHALL compile a Syria ground_attack Mission Spec that cold-starts
the player Su-25T at Incirlik with payload `su25t_2x_fab250` and places Syria
Ural-375 (and companions) at the packaged Aleppo inland station (121° / 200 km
/ 2000 m). It MUST bind PyDCS `Syria` terrain. It MUST NOT write Channel
Manston french-coast 125/76 or Caucasus Kutaisi 43/110 as the required
destination.

#### Scenario: Incirlik Aleppo ground_attack contracts
- **WHEN** `examples/incirlik_aleppo_ground_attack.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Syria`, player type `Su-25T`,
  `airdromeId` 16, cold parking, start_time 32400, player radio 251.0 MHz,
  FAB-250 stores, Ground Attack tasking, and country `Syria` on land targets

### Requirement: Human acceptance for Syria ground_attack in DCS
A compiled Incirlik Aleppo ground_attack `.miz` MUST be openable in the DCS
Mission Editor and flyable as Instant Action with Syria and Su-25T installed.
This is human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Syria ground_attack in DCS
- **WHEN** a user opens the compiled Syria GA `.miz` in DCS ME or Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Incirlik with a land strike inland past Aleppo

### Requirement: Compile recon at Incirlik
The compiler SHALL compile a Syria recon Mission Spec that cold-starts the
player Su-25T at Incirlik and places an observe AOI at the packaged Aleppo
inland station (121° / 200 km / 2000 m) with Ural-375 contacts country Syria.
It MUST bind PyDCS `Syria` terrain. It MUST NOT write Channel Manston
french-coast 125/76 or Caucasus Kutaisi 43/110 as the required AOI.

#### Scenario: Incirlik Aleppo recon contracts
- **WHEN** `examples/incirlik_aleppo_recon.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Syria`, player type `Su-25T`,
  `airdromeId` 16, cold parking, start_time 32400, player radio 251.0 MHz,
  Reconnaissance tasking, `recon_aoi`, and country `Syria` on land contacts

### Requirement: Human acceptance for Syria recon in DCS
A compiled Incirlik Aleppo recon `.miz` MUST be openable in the DCS Mission
Editor and flyable as Instant Action with Syria and Su-25T installed. This is
human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Syria recon in DCS
- **WHEN** a user opens the compiled Syria recon `.miz` in DCS ME or Instant
  Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Incirlik with an observe AOI inland past Aleppo

### Requirement: Human acceptance on Syria
A compiled Incirlik cold free-flight `.miz` MUST be openable in the DCS Mission
Editor and flyable as Instant Action with Syria and Su-25T installed. This
is human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Syria smoke in DCS
- **WHEN** a user opens the compiled Syria cold freeflight `.miz` in DCS ME
  or Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Incirlik around 09:00 in clear weather

### Requirement: Nevada Spec binds to Nevada terrain
The compiler MUST construct PyDCS Nevada terrain when compiling a Mission
Spec with theatre `Nevada`.

#### Scenario: Nevada Spec uses Nevada terrain
- **WHEN** a Mission Spec with theatre `Nevada` is compiled
- **THEN** the compiler MUST construct a PyDCS Nevada terrain for the
  mission

### Requirement: Cold parking freeflight at Nellis
The compiler SHALL place the player Su-25T as a cold start from parking at
Nellis on Nevada when the Spec requests that combination. Group radio MUST
be 251.0 MHz.

#### Scenario: Cold parking at Nellis
- **WHEN** the Mission Spec requests cold parking at `Nellis` for `Su-25T`
  with skill Player, country USA, and theatre `Nevada`
- **THEN** the compiled mission MUST use Nevada theatre, player type
  `Su-25T`, skill `Player`, frequency 251.0, and parking cold-start at
  Nellis (airdromeId 4)

### Requirement: Compile freeflight at Groom Lake
The compiler SHALL compile a Nevada free-flight Mission Spec that cold-starts
the player Su-25T at Groom Lake with country `USA` on blue. It MUST bind
PyDCS `Nevada` terrain. It MUST write `airdromeId` 2 on the Nevada theatre
(not Falklands Mount Pleasant, not Channel Merville Calonne).

#### Scenario: Groom Lake freeflight contracts
- **WHEN** `examples/groom_lake_cold_freeflight.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Nevada`, player type `Su-25T`,
  `airdromeId` 2, cold parking, start_time 32400, player radio 251.0 MHz,
  and country `USA`

### Requirement: Compile CAP at Nellis
The compiler SHALL compile a Nevada CAP Mission Spec that cold-starts the
player Su-25T at Nellis and patrols the packaged north-range station
(350° / 40 km / 4000 m) with optional Russia Su-25T opposition. It MUST bind
PyDCS `Nevada` terrain. It MUST NOT require Incirlik 180/40, Batumi 270/40, or
Cherbourg 180/63 as the station.

#### Scenario: Nellis CAP contracts
- **WHEN** `examples/nellis_north_range_cap.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Nevada`, player type `Su-25T`,
  `airdromeId` 4, cold parking, start_time 32400, player radio 251.0 MHz,
  CAP tasking, and country `Russia` when enemies are present

### Requirement: Compile intercept at Nellis
The compiler SHALL compile a Nevada intercept Mission Spec that cold-starts
the player Su-25T at Nellis and places opposition on the packaged
north-range corridor (Nellis + 350° / 40 km). Channel Hawkinge/Dover
literals MUST stay bit-identical.

#### Scenario: Nellis intercept contracts
- **WHEN** `examples/nellis_dawn_intercept.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Nevada`, player type `Su-25T`,
  `airdromeId` 4, start_time 21600, player radio 251.0 MHz, country `Russia`
  when enemies are present, and enemy map position -358803.06487951166 /
  -24179.163922677217 (MUST NOT contain Channel 30989.935547)

### Requirement: Compile escort at Nellis
The compiler SHALL compile a Nevada escort Mission Spec that cold-starts
the player Su-25T at Nellis and flies a USA Su-25T package to the
packaged north-range station (350° / 40 km / 4000 m) with optional Russia
Su-25T bounce. It MUST bind PyDCS `Nevada` terrain. It MUST NOT write
Channel Manston escort 120/55 as the required destination.

#### Scenario: Nellis escort contracts
- **WHEN** `examples/nellis_north_range_escort.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Nevada`, player type `Su-25T`,
  `airdromeId` 4, cold parking, start_time 32400, player radio 251.0 MHz,
  Escort tasking, country `USA` on the package, and country `Russia` when
  enemies are present

### Requirement: Compile ground_attack at Nellis
The compiler SHALL compile a Nevada ground_attack Mission Spec that cold-starts
the player Su-25T at Nellis with payload `su25t_2x_fab250` and places Russia
Ural-375 (and companions) at the packaged Creech inland station (303° / 85 km
/ 2000 m). It MUST bind PyDCS `Nevada` terrain. It MUST NOT write Channel
Manston french-coast 125/76, Syria Aleppo 121/200, Caucasus Kutaisi 43/110, or
the Nevada CAP 350/40 station as the required destination.

#### Scenario: Nellis Creech ground_attack contracts
- **WHEN** `examples/nellis_creech_ground_attack.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Nevada`, player type `Su-25T`,
  `airdromeId` 4, cold parking, start_time 32400, player radio 251.0 MHz,
  FAB-250 stores, Ground Attack tasking, and country `Russia` on land targets

### Requirement: Human acceptance for Nevada ground_attack in DCS
A compiled Nellis Creech ground_attack `.miz` MUST be openable in the DCS
Mission Editor and flyable as Instant Action with Nevada and Su-25T installed.
This is human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Nevada ground_attack in DCS
- **WHEN** a user opens the compiled Nevada GA `.miz` in DCS ME or Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Nellis with a land strike inland past Creech

### Requirement: Compile recon at Nellis
The compiler SHALL compile a Nevada recon Mission Spec that cold-starts the
player Su-25T at Nellis and places an observe AOI at the packaged Creech
inland station (303° / 85 km / 2000 m) with Ural-375 contacts country Russia.
It MUST bind PyDCS `Nevada` terrain. It MUST NOT write Channel Manston
french-coast 125/76, Syria Aleppo 121/200, Caucasus Kutaisi 43/110, or the
Nevada CAP 350/40 station as the required AOI.

#### Scenario: Nellis Creech recon contracts
- **WHEN** `examples/nellis_creech_recon.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Nevada`, player type `Su-25T`,
  `airdromeId` 4, cold parking, start_time 32400, player radio 251.0 MHz,
  Reconnaissance tasking, `recon_aoi`, country `USA` on the player, and
  country `Russia` on land contacts

### Requirement: Human acceptance for Nevada recon in DCS
A compiled Nellis Creech recon `.miz` MUST be openable in the DCS Mission
Editor and flyable as Instant Action with Nevada and Su-25T installed. This is
human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Nevada recon in DCS
- **WHEN** a user opens the compiled Nevada recon `.miz` in DCS ME or Instant
  Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Nellis with an observe AOI inland past Creech

### Requirement: Human acceptance on Nevada
A compiled Nellis cold free-flight `.miz` MUST be openable in the DCS Mission
Editor and flyable as Instant Action with Nevada and Su-25T installed. This
is human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Nevada smoke in DCS
- **WHEN** a user opens the compiled Nevada cold freeflight `.miz` in DCS ME
  or Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Nellis around 09:00 in clear weather

### Requirement: Falklands Spec binds to Falklands terrain
The compiler MUST construct PyDCS Falklands terrain when compiling a Mission
Spec with theatre `Falklands`.

#### Scenario: Falklands Spec uses Falklands terrain
- **WHEN** a Mission Spec with theatre `Falklands` is compiled
- **THEN** the compiler MUST construct a PyDCS Falklands terrain for the
  mission

### Requirement: Cold parking freeflight at Mount Pleasant
The compiler SHALL place the player Su-25T as a cold start from parking at
Mount Pleasant on Falklands when the Spec requests that combination. Group
radio MUST be 251.0 MHz.

#### Scenario: Cold parking at MountPleasant
- **WHEN** the Mission Spec requests cold parking at `MountPleasant` for
  `Su-25T` with skill Player, country UK, and theatre `Falklands`
- **THEN** the compiled mission MUST use Falklands theatre, player type
  `Su-25T`, skill `Player`, frequency 251.0, and parking cold-start at
  Mount Pleasant (airdromeId 2)

### Requirement: Compile freeflight at Rio Gallegos
The compiler SHALL compile a Falklands free-flight Mission Spec that
cold-starts the player Su-25T at Rio Gallegos with country `Argentina` on
red. It MUST bind PyDCS `Falklands` terrain. It MUST write `airdromeId` 5 on
the Falklands theatre (not Channel Manston).

#### Scenario: Rio Gallegos freeflight contracts
- **WHEN** `examples/rio_gallegos_cold_freeflight.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Falklands`, player type `Su-25T`,
  `airdromeId` 5, cold parking, start_time 32400, player radio 251.0 MHz,
  and country `Argentina`

### Requirement: Compile CAP at Mount Pleasant
The compiler SHALL compile a Falklands CAP Mission Spec that cold-starts the
player Su-25T at Mount Pleasant and patrols the packaged South Atlantic
station (150° / 40 km / 4000 m) with optional Argentina Su-25T opposition. It
MUST bind PyDCS `Falklands` terrain. It MUST NOT require Manston 135/25,
Cherbourg 180/63, Incirlik 180/40, Batumi 270/40, or Nellis 350/40 as the
station.

#### Scenario: Mount Pleasant CAP contracts
- **WHEN** `examples/mount_pleasant_south_atlantic_cap.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Falklands`, player type `Su-25T`,
  `airdromeId` 2, cold parking, start_time 32400, player radio 251.0 MHz,
  CAP tasking, and country `Argentina` when enemies are present

### Requirement: Compile intercept at Mount Pleasant
The compiler SHALL compile a Falklands intercept Mission Spec that
cold-starts the player Su-25T at Mount Pleasant and places opposition on the
packaged South Atlantic corridor (Mount Pleasant + 150° / 40 km). Channel
Hawkinge/Dover literals MUST stay bit-identical.

#### Scenario: Mount Pleasant intercept contracts
- **WHEN** `examples/mount_pleasant_dawn_intercept.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Falklands`, player type `Su-25T`,
  `airdromeId` 2, start_time 21600, player radio 251.0 MHz, country
  `Argentina` when enemies are present, and enemy map position
  38677.30416162246 / 67168.748047 (MUST NOT contain Channel 30989.935547)

### Requirement: Compile escort at Mount Pleasant
The compiler SHALL compile a Falklands escort Mission Spec that cold-starts
the player Su-25T at Mount Pleasant and escorts a UK Su-25T package to the
packaged South Atlantic station (150° / 40 km / 4000 m) with optional
Argentina Su-25T bounce. Channel escort goldens (Manston 120/55) MUST stay
bit-identical.

#### Scenario: Mount Pleasant escort contracts
- **WHEN** `examples/mount_pleasant_south_atlantic_escort.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Falklands`, player type `Su-25T`,
  `airdromeId` 2, start_time 32400, player radio 251.0 MHz, Escort tasking,
  country `UK` on the package, and country `Argentina` when enemies are
  present

### Requirement: Compile ground_attack at Mount Pleasant
The compiler SHALL compile a Falklands ground_attack Mission Spec that
cold-starts the player Su-25T at Mount Pleasant with payload
`su25t_2x_fab250` and places Argentina Ural-375 (and companions) at 269° /
21 km / 2000 m. It MUST bind PyDCS `Falklands` terrain. It MUST NOT write
Channel 125/76, Syria 121/200, Caucasus 43/110, Nevada 303/85, or CAP 150/40
station 38677.30416162246 / 67168.748047 as the required destination.

#### Scenario: Mount Pleasant ground_attack contracts
- **WHEN** `examples/mount_pleasant_east_falkland_ground_attack.yaml` is
  compiled
- **THEN** the `.miz` MUST contain theatre `Falklands`, player type `Su-25T`,
  `airdromeId` 2, start_time 32400, player radio 251.0 MHz, Ground Attack
  tasking, FAB-250, country `UK` on the player, and country `Argentina` on
  the trucks (MUST NOT contain Channel 30989.935547 or CAP station
  38677.30416162246)

### Requirement: Compile recon at Mount Pleasant
The compiler SHALL compile a Falklands recon Mission Spec that cold-starts
the player Su-25T at Mount Pleasant and places an observe AOI at the packaged
East Falkland inland station (269° / 21 km / 2000 m) with Ural-375 contacts
country Argentina. It MUST bind PyDCS `Falklands` terrain. It MUST NOT write
Channel Manston french-coast 125/76, Syria Aleppo 121/200, Caucasus Kutaisi
43/110, Nevada Creech 303/85, or the Falklands CAP 150/40 station
38677.30416162246 / 67168.748047 as the required AOI.

#### Scenario: Mount Pleasant East Falkland recon contracts
- **WHEN** `examples/mount_pleasant_east_falkland_recon.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Falklands`, player type `Su-25T`,
  `airdromeId` 2, cold parking, start_time 32400, player radio 251.0 MHz,
  Reconnaissance tasking, `recon_aoi`, country `UK` on the player, and
  country `Argentina` on land contacts (MUST NOT contain Channel 30989.935547
  or CAP station 38677.30416162246)

### Requirement: Human acceptance for Falklands recon in DCS
A compiled Mount Pleasant East Falkland recon `.miz` MUST be openable in the
DCS Mission Editor and flyable as Instant Action with South Atlantic and
Su-25T installed. This is human do-soon after merge, not a hermetic merge
gate.

#### Scenario: Load Falklands recon in DCS
- **WHEN** a user opens the compiled Falklands recon `.miz` in DCS ME or
  Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Mount Pleasant with an observe AOI inland short of Goose
  Green

### Requirement: Human acceptance on Falklands
A compiled Mount Pleasant cold free-flight `.miz` MUST be openable in the DCS
Mission Editor and flyable as Instant Action with South Atlantic and Su-25T
installed. This is human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Falklands smoke in DCS
- **WHEN** a user opens the compiled Falklands cold freeflight `.miz` in DCS
  ME or Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Mount Pleasant around 09:00 in clear weather

### Requirement: Git-pinned PyDCS does not bind new theatres
Pinning pydcs to a git revision that contains additional terrain classes (including `Kola` and Cold War Germany) MUST NOT add Spec theatre bindings. Compile and validation MUST still fail closed for unbound theatre ids. The compiler MUST NOT construct `Kola()` (or other unbound terrains) from a Spec.

#### Scenario: Kola Spec still fails compile
- **WHEN** compile is asked to use theatre id `Kola` after pydcs is git-pinned
- **THEN** compile MUST fail with an unbound-theatre error and MUST NOT write a Kola `.miz`

### Requirement: Payload-directory scan stays disabled until proven
The compiler MUST keep the install payload-directory scan disabled (`_disable_payload_scan` or equivalent) after the git pin, unless a recorded compile with a real DCS World install present succeeds with scanning enabled. Ground-attack loadouts MUST continue to use registry CLSIDs. Free-flight, intercept, and CAP compile MUST remain independent of install payload lua.

#### Scenario: Default compile still disables payload scan
- **WHEN** a Mission Spec is compiled with a DCS install detectable by PyDCS
- **THEN** the compiler MUST NOT rely on scanning the install `UnitPayloads` directory unless LESSONS records that scan-on was proven green for that pin
