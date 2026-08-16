## ADDED Requirements

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

### Requirement: Human acceptance on Caucasus
A compiled Batumi cold free-flight `.miz` MUST be openable in the DCS Mission
Editor and flyable as Instant Action with Caucasus and Su-25T installed. This
is human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Caucasus smoke in DCS
- **WHEN** a user opens the compiled Caucasus cold freeflight `.miz` in DCS ME
  or Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Batumi around 09:00 in clear weather
