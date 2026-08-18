## ADDED Requirements

### Requirement: Compile ground_attack at Mount Pleasant
The compiler SHALL compile a Falklands ground_attack Mission Spec that
cold-starts the player Su-25T at Mount Pleasant with payload
`su25t_2x_fab250` and places Argentina Ural-375 (and companions) at 269° /
21 km / 2000 m. It MUST bind PyDCS `Falklands` terrain. It MUST NOT write
Channel 125/76, Syria 121/200, Caucasus 43/110, Nevada 303/85, or CAP 150/40
station 38677.30416062245 / 67168.748047 as the required destination.

#### Scenario: Mount Pleasant ground_attack contracts
- **WHEN** `examples/mount_pleasant_east_falkland_ground_attack.yaml` is
  compiled
- **THEN** the `.miz` MUST contain theatre `Falklands`, player type `Su-25T`,
  `airdromeId` 2, start_time 32400, player radio 251.0 MHz, Ground Attack
  tasking, FAB-250, country `UK` on the player, and country `Argentina` on
  the trucks (MUST NOT contain Channel 30989.935547 or CAP station
  38677.30416062245)
