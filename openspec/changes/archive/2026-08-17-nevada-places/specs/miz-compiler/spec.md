## ADDED Requirements

### Requirement: Compile CAP at Nellis
The compiler SHALL compile a Nevada CAP Mission Spec that cold-starts the
player Su-25T at Nellis and patrols the packaged north-range station
(350° / 40 km / 4000 m) with optional Russia Su-25T opposition. It MUST bind
PyDCS `Nevada` terrain. It MUST NOT require Incirlik 180/40, Batumi 270/40, or
Cherbourg 180/63 as the station.

#### Scenario: Nellis CAP contracts
- **WHEN** `examples/nellis_north_range_cap.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Nevada`, player type `Su-25T`,
  `airdromeId` 4, cold parking, start_time 32400, player radio 251.0 MHz,
  CAP tasking, and country `Russia` when enemies are present
