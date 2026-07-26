## ADDED Requirements

### Requirement: Compile intercept Mission Spec to .miz
The compiler SHALL transform a validated intercept Mission Spec into a DCS `.miz` that places
the player flight and at least one enemy `Bf-109K-4` flight on The Channel, using registry
facts for aircraft ids and radio frequencies. It MUST NOT invent DCS identifiers. Free-flight
compile behaviour MUST remain unchanged for free-flight Specs.

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
  flights as specified
