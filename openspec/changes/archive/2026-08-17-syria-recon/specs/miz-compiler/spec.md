## ADDED Requirements

### Requirement: Compile recon at Incirlik
The compiler SHALL compile a Syria recon Mission Spec that cold-starts the
player Su-25T at Incirlik and places an observe AOI at the packaged Aleppo
inland station (121° / 200 km / 2000 m) with Ural-375 contacts country Syria.
It MUST bind PyDCS `Syria` terrain. It MUST NOT write Channel Manston
french-coast 125/76 or Caucasus Kutaisi 43/110 as the required AOI.

#### Scenario: Incirlik Aleppo recon contracts
- **WHEN** `examples/incirlik_aleppo_recon.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Syria`, player type `Su-25T`,
  `airdromeId` 16, cold parking, start_time 32400, player radio 251.0 MHz,
  Reconnaissance tasking, `recon_aoi`, and country `Syria` on land contacts

### Requirement: Human acceptance for Syria recon in DCS
A compiled Incirlik Aleppo recon `.miz` MUST be openable in the DCS Mission
Editor and flyable as Instant Action with Syria and Su-25T installed. This is
human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Syria recon in DCS
- **WHEN** a user opens the compiled Syria recon `.miz` in DCS ME or Instant
  Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Incirlik with an observe AOI inland past Aleppo
