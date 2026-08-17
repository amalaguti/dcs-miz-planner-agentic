## ADDED Requirements

### Requirement: Compile escort at Batumi
The compiler SHALL compile a Caucasus escort Mission Spec that cold-starts
the player Su-25T at Batumi and flies a Georgia Su-25T package to the
packaged Black Sea station (270° / 40 km / 4000 m) with optional Russia
Su-25T bounce. It MUST bind PyDCS `Caucasus` terrain. It MUST NOT write
Channel Manston escort 120/55 as the required destination.

#### Scenario: Batumi escort contracts
- **WHEN** `examples/batumi_black_sea_escort.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Caucasus`, player type `Su-25T`,
  `airdromeId` 22, cold parking, start_time 32400, player radio 251.0 MHz,
  Escort tasking, country `Georgia` on the package, and country `Russia` when
  enemies are present

### Requirement: Human acceptance for Caucasus escort in DCS
A compiled Batumi escort `.miz` MUST be openable in the DCS Mission Editor
and flyable as Instant Action with Caucasus and Su-25T installed. This is
human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Caucasus escort in DCS
- **WHEN** a user opens the compiled Caucasus escort `.miz` in DCS ME or
  Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Batumi with a package west over the Black Sea
