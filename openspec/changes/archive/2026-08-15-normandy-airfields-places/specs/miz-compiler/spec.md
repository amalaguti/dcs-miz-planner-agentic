## ADDED Requirements

### Requirement: Compile CAP at Needs Oar Point
The compiler SHALL compile a Normandy CAP Mission Spec that cold-starts the
player Spitfire at Needs Oar Point and orbits the packaged CAP station
(180° / 63 km / 4000 m) with optional Bf-109K-4 opposition. It MUST bind
PyDCS `Normandy` terrain (not `Normandy2` or TheChannel). It MUST NOT write
Channel Hawkinge/Dover intercept coordinates.

#### Scenario: Needs Oar Point CAP contracts
- **WHEN** `examples/needs_oar_point_cap.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Normandy`, player type
  `SpitfireLFMkIX`, `airdromeId` 28, cold parking, start_time 32400, CAP Orbit
  Circle, player radio 124.0 MHz, and enemy `Bf-109K-4` at 40.0 MHz when
  enemies are present

### Requirement: Human acceptance for Normandy CAP in DCS
A compiled Needs Oar Point CAP `.miz` MUST be openable in the DCS Mission
Editor and flyable as Instant Action with Normandy 2.0 and Spitfire LF Mk IX
installed. This is human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Normandy CAP in DCS
- **WHEN** a user opens the compiled Normandy CAP `.miz` in DCS ME or Instant
  Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Needs Oar Point with a CAP station south toward Cherbourg
