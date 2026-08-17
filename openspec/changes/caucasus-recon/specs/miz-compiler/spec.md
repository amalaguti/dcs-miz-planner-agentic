## ADDED Requirements

### Requirement: Compile recon at Batumi
The compiler SHALL compile a Caucasus recon Mission Spec that cold-starts
the player Su-25T at Batumi and observes land contacts at the packaged
Kutaisi-inland AOI (43° / 110 km / 2000 m) with weapons hold. It MUST bind
PyDCS `Caucasus` terrain. It MUST NOT require Channel french-coast 125/76
or Black Sea CAP 270/40 as the AOI.

#### Scenario: Batumi recon contracts
- **WHEN** `examples/batumi_kutaisi_recon.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Caucasus`, player type
  `Su-25T`, `airdromeId` 22, cold parking, start_time 32400, player
  radio 251.0 MHz, Reconnaissance tasking, `Ural-375`, and recon AOI
  find-beat tokens
