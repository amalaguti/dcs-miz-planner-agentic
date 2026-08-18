## ADDED Requirements

### Requirement: Compile recon at Nellis
The compiler SHALL compile a Nevada recon Mission Spec that cold-starts the
player Su-25T at Nellis and places an observe AOI at the packaged Creech
inland station (303° / 85 km / 2000 m) with Ural-375 contacts country Russia.
It MUST bind PyDCS `Nevada` terrain. It MUST NOT write Channel Manston
french-coast 125/76, Syria Aleppo 121/200, Caucasus Kutaisi 43/110, or the
Nevada CAP 350/40 station as the required AOI.

#### Scenario: Nellis Creech recon contracts
- **WHEN** `examples/nellis_creech_recon.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Nevada`, player type `Su-25T`,
  `airdromeId` 4, cold parking, start_time 32400, player radio 251.0 MHz,
  Reconnaissance tasking, `recon_aoi`, country `USA` on the player, and
  country `Russia` on land contacts

### Requirement: Human acceptance for Nevada recon in DCS
A compiled Nellis Creech recon `.miz` MUST be openable in the DCS Mission
Editor and flyable as Instant Action with Nevada and Su-25T installed. This is
human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Nevada recon in DCS
- **WHEN** a user opens the compiled Nevada recon `.miz` in DCS ME or Instant
  Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Nellis with an observe AOI inland past Creech
