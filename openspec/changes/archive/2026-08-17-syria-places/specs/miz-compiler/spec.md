## ADDED Requirements

### Requirement: Compile CAP at Incirlik
The compiler SHALL compile a Syria CAP Mission Spec that cold-starts the
player Su-25T at Incirlik and patrols the packaged Iskenderun station
(180° / 40 km / 4000 m) with optional Syria Su-25T opposition. It MUST bind
PyDCS `Syria` terrain. It MUST NOT require Batumi 270/40 or Cherbourg 180/63
as the station.

#### Scenario: Incirlik CAP contracts
- **WHEN** `examples/incirlik_iskenderun_cap.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Syria`, player type `Su-25T`,
  `airdromeId` 16, cold parking, start_time 32400, player radio 251.0 MHz,
  CAP tasking, and country `Syria` when enemies are present
