## ADDED Requirements

### Requirement: Compile recon at Needs Oar Point
The compiler SHALL compile a Normandy recon Mission Spec that cold-starts
the player Spitfire at Needs Oar Point and observes land contacts at the
packaged Maupertus-inland AOI (180° / 133 km / 2000 m) with weapons hold.
It MUST bind PyDCS `Normandy` terrain. It MUST NOT require Channel
french-coast 125/76 as the AOI.

#### Scenario: Needs Oar Point recon contracts
- **WHEN** `examples/needs_oar_point_recon.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Normandy`, player type
  `SpitfireLFMkIX`, `airdromeId` 28, cold parking, start_time 32400, player
  radio 124.0 MHz, Reconnaissance tasking, `Blitz_36-6700A`, and recon AOI
  find-beat tokens
