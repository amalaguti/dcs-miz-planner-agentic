## ADDED Requirements

### Requirement: Compile freeflight at Groom Lake
The compiler SHALL compile a Nevada free-flight Mission Spec that cold-starts
the player Su-25T at Groom Lake with country `USA` on blue. It MUST bind
PyDCS `Nevada` terrain. It MUST write `airdromeId` 2 on the Nevada theatre
(not Falklands Mount Pleasant, not Channel Merville Calonne).

#### Scenario: Groom Lake freeflight contracts
- **WHEN** `examples/groom_lake_cold_freeflight.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Nevada`, player type `Su-25T`,
  `airdromeId` 2, cold parking, start_time 32400, player radio 251.0 MHz,
  and country `USA`
