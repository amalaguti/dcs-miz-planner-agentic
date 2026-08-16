## ADDED Requirements

### Requirement: Compile escort at Needs Oar Point
The compiler SHALL compile a Normandy escort Mission Spec that cold-starts
the player Spitfire at Needs Oar Point and flies a Mosquito package to the
packaged Cherbourg-corridor station (180° / 63 km / 4000 m) with optional
Bf-109K-4 bounce. It MUST bind PyDCS `Normandy` terrain. It MUST NOT write
Channel Manston escort 120/55 as the required destination.

#### Scenario: Needs Oar Point escort contracts
- **WHEN** `examples/needs_oar_point_escort.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Normandy`, player type
  `SpitfireLFMkIX`, `airdromeId` 28, cold parking, start_time 32400, player
  radio 124.0 MHz, package `MosquitoFBMkVI`, Escort tasking, and enemy
  `Bf-109K-4` at 40.0 MHz when enemies are present
