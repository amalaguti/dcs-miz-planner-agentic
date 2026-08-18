## ADDED Requirements

### Requirement: Compile escort at Mount Pleasant
The compiler SHALL compile a Falklands escort Mission Spec that cold-starts
the player Su-25T at Mount Pleasant and escorts a UK Su-25T package to the
packaged South Atlantic station (150° / 40 km / 4000 m) with optional
Argentina Su-25T bounce. Channel escort goldens (Manston 120/55) MUST stay
bit-identical.

#### Scenario: Mount Pleasant escort contracts
- **WHEN** `examples/mount_pleasant_south_atlantic_escort.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Falklands`, player type `Su-25T`,
  `airdromeId` 2, start_time 32400, player radio 251.0 MHz, Escort tasking,
  country `UK` on the package, and country `Argentina` when enemies are
  present
