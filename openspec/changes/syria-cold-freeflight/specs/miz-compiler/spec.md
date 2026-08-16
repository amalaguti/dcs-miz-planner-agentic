## ADDED Requirements

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

### Requirement: Human acceptance on Syria
A compiled Incirlik cold free-flight `.miz` MUST be openable in the DCS Mission
Editor and flyable as Instant Action with Syria and Su-25T installed. This
is human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Syria smoke in DCS
- **WHEN** a user opens the compiled Syria cold freeflight `.miz` in DCS ME
  or Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Incirlik around 09:00 in clear weather
