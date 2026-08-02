## ADDED Requirements

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
