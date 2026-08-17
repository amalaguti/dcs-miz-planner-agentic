## ADDED Requirements

### Requirement: Compile intercept at Nellis
The compiler SHALL compile a Nevada intercept Mission Spec that cold-starts
the player Su-25T at Nellis and places opposition on the packaged
north-range corridor (Nellis + 350° / 40 km). Channel Hawkinge/Dover
literals MUST stay bit-identical.

#### Scenario: Nellis intercept contracts
- **WHEN** `examples/nellis_dawn_intercept.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Nevada`, player type `Su-25T`,
  `airdromeId` 4, start_time 21600, player radio 251.0 MHz, country `Russia`
  when enemies are present, and enemy map position -358803.06487951166 /
  -24179.163922677217 (MUST NOT contain Channel 30989.935547)
