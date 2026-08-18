## ADDED Requirements

### Requirement: Compile recon at Mount Pleasant
The compiler SHALL compile a Falklands recon Mission Spec that cold-starts
the player Su-25T at Mount Pleasant and places an observe AOI at the packaged
East Falkland inland station (269° / 21 km / 2000 m) with Ural-375 contacts
country Argentina. It MUST bind PyDCS `Falklands` terrain. It MUST NOT write
Channel Manston french-coast 125/76, Syria Aleppo 121/200, Caucasus Kutaisi
43/110, Nevada Creech 303/85, or the Falklands CAP 150/40 station
38677.30416062245 / 67168.748047 as the required AOI.

#### Scenario: Mount Pleasant East Falkland recon contracts
- **WHEN** `examples/mount_pleasant_east_falkland_recon.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Falklands`, player type `Su-25T`,
  `airdromeId` 2, cold parking, start_time 32400, player radio 251.0 MHz,
  Reconnaissance tasking, `recon_aoi`, country `UK` on the player, and
  country `Argentina` on land contacts (MUST NOT contain Channel 30989.935547
  or CAP station 38677.30416062245)

### Requirement: Human acceptance for Falklands recon in DCS
A compiled Mount Pleasant East Falkland recon `.miz` MUST be openable in the
DCS Mission Editor and flyable as Instant Action with South Atlantic and
Su-25T installed. This is human do-soon after merge, not a hermetic merge
gate.

#### Scenario: Load Falklands recon in DCS
- **WHEN** a user opens the compiled Falklands recon `.miz` in DCS ME or
  Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Mount Pleasant with an observe AOI inland short of Goose
  Green
