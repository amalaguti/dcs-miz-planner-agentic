## ADDED Requirements

### Requirement: Compile escort at Incirlik
The compiler SHALL compile a Syria escort Mission Spec that cold-starts
the player Su-25T at Incirlik and flies a Turkey Su-25T package to the
packaged Iskenderun station (180° / 40 km / 4000 m) with optional Syria
Su-25T bounce. It MUST bind PyDCS `Syria` terrain. It MUST NOT write
Channel Manston escort 120/55 as the required destination.

#### Scenario: Incirlik escort contracts
- **WHEN** `examples/incirlik_iskenderun_escort.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Syria`, player type `Su-25T`,
  `airdromeId` 16, cold parking, start_time 32400, player radio 251.0 MHz,
  Escort tasking, country `Turkey` on the package, and country `Syria` when
  enemies are present

### Requirement: Human acceptance for Syria escort in DCS
A compiled Incirlik escort `.miz` MUST be openable in the DCS Mission Editor
and flyable as Instant Action with Syria and Su-25T installed. This is
human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Syria escort in DCS
- **WHEN** a user opens the compiled Syria escort `.miz` in DCS ME or
  Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Incirlik with a package south over the Gulf of Iskenderun
