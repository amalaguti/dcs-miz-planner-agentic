## ADDED Requirements

### Requirement: Compile CAP at Mount Pleasant
The compiler SHALL compile a Falklands CAP Mission Spec that cold-starts the
player Su-25T at Mount Pleasant and patrols the packaged South Atlantic
station (150° / 40 km / 4000 m) with optional Argentina Su-25T opposition. It
MUST bind PyDCS `Falklands` terrain. It MUST NOT require Manston 135/25,
Cherbourg 180/63, Incirlik 180/40, Batumi 270/40, or Nellis 350/40 as the
station.

#### Scenario: Mount Pleasant CAP contracts
- **WHEN** `examples/mount_pleasant_south_atlantic_cap.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Falklands`, player type `Su-25T`,
  `airdromeId` 2, cold parking, start_time 32400, player radio 251.0 MHz,
  CAP tasking, and country `Argentina` when enemies are present
