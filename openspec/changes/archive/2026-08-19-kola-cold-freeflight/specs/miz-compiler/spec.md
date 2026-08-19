## ADDED Requirements

### Requirement: Kola Spec binds to Kola terrain
The compiler MUST construct PyDCS Kola terrain when compiling a Mission Spec
with theatre `Kola`.

#### Scenario: Kola Spec uses Kola terrain
- **WHEN** a Mission Spec with theatre `Kola` is compiled
- **THEN** the compiler MUST construct a PyDCS Kola terrain for the mission

### Requirement: Cold parking freeflight at Bodo
The compiler SHALL place the player Su-25T as a cold start from parking at
Bodo on Kola when the Spec requests that combination. Group radio MUST be
251.0 MHz.

#### Scenario: Cold parking at Bodo
- **WHEN** the Mission Spec requests cold parking at `Bodo` for `Su-25T`
  with skill Player, country Norway, and theatre `Kola`
- **THEN** the compiled mission MUST use Kola theatre, player type
  `Su-25T`, skill `Player`, frequency 251.0, and parking cold-start at Bodo
  (airdromeId 7)

### Requirement: Human acceptance on Kola
A compiled Bodo cold free-flight `.miz` MUST be openable in the DCS Mission
Editor and flyable as Instant Action with Kola and Su-25T installed. This is
human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Kola smoke in DCS
- **WHEN** a user opens the compiled Kola cold freeflight `.miz` in DCS ME
  or Instant Action
- **THEN** the mission MUST load without editor errors and present the
  player cold-started at Bodo around 09:00 in clear weather
