## ADDED Requirements

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

### Requirement: Human acceptance on Nevada
A compiled Nellis cold free-flight `.miz` MUST be openable in the DCS Mission
Editor and flyable as Instant Action with Nevada and Su-25T installed. This
is human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Nevada smoke in DCS
- **WHEN** a user opens the compiled Nevada cold freeflight `.miz` in DCS ME
  or Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Nellis around 09:00 in clear weather
