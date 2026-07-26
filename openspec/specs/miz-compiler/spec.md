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
The compiler (or loader, before compile) MUST NOT silently drop non-empty `enemies`, `objectives`, or `triggers`. Until a later change implements those capabilities, non-empty values MUST cause a clear failure.

#### Scenario: Non-empty enemies refused
- **WHEN** a Mission Spec includes a non-empty `enemies` collection
- **THEN** compilation MUST NOT produce a combat `.miz`, and the user MUST receive an error that combat extensions are not supported yet

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
