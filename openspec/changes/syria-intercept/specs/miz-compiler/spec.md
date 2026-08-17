## ADDED Requirements

### Requirement: Compile intercept at Incirlik
The compiler SHALL compile a Syria intercept Mission Spec that cold-starts
the player Su-25T at Incirlik and places opposition on the packaged
Iskenderun corridor (Incirlik + 180° / 40 km). Channel Hawkinge/Dover
literals MUST stay bit-identical.

#### Scenario: Incirlik intercept contracts
- **WHEN** `examples/incirlik_dawn_intercept.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Syria`, player type `Su-25T`,
  `airdromeId` 16, start_time 21600, player radio 251.0 MHz, country `Syria`
  when enemies are present, and enemy map position 181207.773438 /
  -35240.347656 (MUST NOT contain Channel 30989.935547)
