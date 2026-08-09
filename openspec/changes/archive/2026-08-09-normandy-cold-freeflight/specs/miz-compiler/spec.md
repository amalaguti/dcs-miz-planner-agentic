## ADDED Requirements

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
