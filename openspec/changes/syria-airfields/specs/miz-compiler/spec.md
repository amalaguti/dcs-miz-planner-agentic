## ADDED Requirements

### Requirement: Compile freeflight at Palmyra
The compiler SHALL compile a Syria free-flight Mission Spec that cold-starts
the player Su-25T at Palmyra with country `Syria` on red. It MUST bind
PyDCS `Syria` terrain. It MUST write `airdromeId` 28 on the Syria theatre
(not Caucasus Mozdok, not Normandy Needs Oar Point).

#### Scenario: Palmyra freeflight contracts
- **WHEN** `examples/palmyra_cold_freeflight.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Syria`, player type `Su-25T`,
  `airdromeId` 28, cold parking, start_time 32400, player radio 251.0 MHz,
  and country `Syria`
