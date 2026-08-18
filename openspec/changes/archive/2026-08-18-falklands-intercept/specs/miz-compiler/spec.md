## ADDED Requirements

### Requirement: Compile intercept at Mount Pleasant
The compiler SHALL compile a Falklands intercept Mission Spec that
cold-starts the player Su-25T at Mount Pleasant and places opposition on the
packaged South Atlantic corridor (Mount Pleasant + 150° / 40 km). Channel
Hawkinge/Dover literals MUST stay bit-identical.

#### Scenario: Mount Pleasant intercept contracts
- **WHEN** `examples/mount_pleasant_dawn_intercept.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Falklands`, player type `Su-25T`,
  `airdromeId` 2, start_time 21600, player radio 251.0 MHz, country
  `Argentina` when enemies are present, and enemy map position
  38677.30416062245 / 67168.748047 (MUST NOT contain Channel 30989.935547)
