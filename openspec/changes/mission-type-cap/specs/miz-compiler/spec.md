## ADDED Requirements

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
