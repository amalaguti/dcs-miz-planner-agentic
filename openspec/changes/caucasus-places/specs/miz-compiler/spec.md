## ADDED Requirements

### Requirement: Compile CAP at Batumi
The compiler SHALL compile a Caucasus CAP Mission Spec that cold-starts the
player Su-25T at Batumi and orbits the packaged CAP station
(270° / 40 km / 4000 m) with optional Russia Su-25T opposition. It MUST bind
PyDCS `Caucasus` terrain. Group radio MUST be 251.0 MHz. It MUST NOT write
Channel Hawkinge/Dover or Normandy Cherbourg intercept coordinates.

#### Scenario: Batumi CAP contracts
- **WHEN** `examples/batumi_black_sea_cap.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Caucasus`, player type `Su-25T`,
  `airdromeId` 22, cold parking, start_time 32400, CAP Orbit Circle, player
  radio 251.0 MHz, and country `Russia` when enemies are present

### Requirement: Human acceptance for Caucasus CAP in DCS
A compiled Batumi CAP `.miz` MUST be openable in the DCS Mission Editor and
flyable as Instant Action with Caucasus and Su-25T installed. This is human
do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Caucasus CAP in DCS
- **WHEN** a user opens the compiled Caucasus CAP `.miz` in DCS ME or Instant
  Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Batumi with a CAP station west over the Black Sea
