## ADDED Requirements

### Requirement: Compile freeflight at Rio Gallegos
The compiler SHALL compile a Falklands free-flight Mission Spec that
cold-starts the player Su-25T at Rio Gallegos with country `Argentina` on
red. It MUST bind PyDCS `Falklands` terrain. It MUST write `airdromeId` 5 on
the Falklands theatre (not Channel Manston).

#### Scenario: Rio Gallegos freeflight contracts
- **WHEN** `examples/rio_gallegos_cold_freeflight.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Falklands`, player type `Su-25T`,
  `airdromeId` 5, cold parking, start_time 32400, player radio 251.0 MHz,
  and country `Argentina`
