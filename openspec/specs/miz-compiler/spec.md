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
`zones` MUST fail compile until native trigger emit is implemented (clear error; no silent
drop).

#### Scenario: Free-flight non-empty enemies refused
- **WHEN** a free-flight Mission Spec includes a non-empty `enemies` collection
- **THEN** compilation MUST NOT produce a combat `.miz`, and the user MUST receive an error
  that free_flight requires empty combat extensions

### Requirement: Compiler resolves facts via Channel registry
The free-flight compiler SHALL resolve theatre support, player airfield → `airdromeId`, known aircraft checks, and group radio frequency through the Channel reference registry API rather than private ad-hoc constants inaccessible to other components.

#### Scenario: Manston compile still uses registry Manston=5
- **WHEN** the checked-in Manston free-flight Mission Spec is compiled
- **THEN** the compiler MUST obtain Manston’s `airdromeId` from the Channel registry and the resulting `.miz` MUST still place the player cold at Manston (`airdromeId` 5) with Spitfire group frequency 124.0 MHz and remain openable in DCS Mission Editor / Instant Action

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

### Requirement: Compile refuses undeclared trigger emit
Until native trigger compilation is implemented, the compiler MUST refuse to write a `.miz`
when the Mission Spec has a non-empty `triggers` list or a non-empty `zones` list. The
error MUST state that trigger/zone emit is not available yet. Specs with empty `triggers`
and empty `zones` MUST continue to compile as today.

#### Scenario: Empty triggers still compile
- **WHEN** the checked-in Manston cold free-flight Spec (empty triggers/zones) is compiled
- **THEN** the compiler MUST write a `.miz` successfully

#### Scenario: Non-empty triggers blocked at compile
- **WHEN** a Spec that validates with a non-empty `triggers` list is compiled
- **THEN** the compiler MUST fail without writing a `.miz`, with a clear not-implemented
  message
