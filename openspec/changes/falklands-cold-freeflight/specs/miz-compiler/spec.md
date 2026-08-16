## ADDED Requirements

### Requirement: Falklands Spec binds to Falklands terrain
The compiler MUST construct PyDCS Falklands terrain when compiling a Mission
Spec with theatre `Falklands`.

#### Scenario: Falklands Spec uses Falklands terrain
- **WHEN** a Mission Spec with theatre `Falklands` is compiled
- **THEN** the compiler MUST construct a PyDCS Falklands terrain for the
  mission

### Requirement: Cold parking freeflight at Mount Pleasant
The compiler SHALL place the player Su-25T as a cold start from parking at
Mount Pleasant on Falklands when the Spec requests that combination. Group
radio MUST be 251.0 MHz.

#### Scenario: Cold parking at MountPleasant
- **WHEN** the Mission Spec requests cold parking at `MountPleasant` for
  `Su-25T` with skill Player, country UK, and theatre `Falklands`
- **THEN** the compiled mission MUST use Falklands theatre, player type
  `Su-25T`, skill `Player`, frequency 251.0, and parking cold-start at
  Mount Pleasant (airdromeId 2)

### Requirement: Human acceptance on Falklands
A compiled Mount Pleasant cold free-flight `.miz` MUST be openable in the DCS
Mission Editor and flyable as Instant Action with South Atlantic and Su-25T
installed. This is human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Falklands smoke in DCS
- **WHEN** a user opens the compiled Falklands cold freeflight `.miz` in DCS
  ME or Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Mount Pleasant around 09:00 in clear weather
