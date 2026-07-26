## ADDED Requirements

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
