## ADDED Requirements

### Requirement: Compile escort at Nellis
The compiler SHALL compile a Nevada escort Mission Spec that cold-starts
the player Su-25T at Nellis and flies a USA Su-25T package to the
packaged north-range station (350° / 40 km / 4000 m) with optional Russia
Su-25T bounce. It MUST bind PyDCS `Nevada` terrain. It MUST NOT write
Channel Manston escort 120/55 as the required destination.

#### Scenario: Nellis escort contracts
- **WHEN** `examples/nellis_north_range_escort.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Nevada`, player type `Su-25T`,
  `airdromeId` 4, cold parking, start_time 32400, player radio 251.0 MHz,
  Escort tasking, country `USA` on the package, and country `Russia` when
  enemies are present
