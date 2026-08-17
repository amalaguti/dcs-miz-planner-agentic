## MODIFIED Requirements

### Requirement: Syria invent is free_flight only
Invent/chat SHALL allow all six mission types when the bound theatre is
`Syria` (home `Incirlik`; CAP/intercept/escort station 180° / 40 km south
over the Gulf of Iskenderun; GA/recon AOI 121° / 200 km inland past Aleppo —
not Manston 125/76, not Cherbourg 180/63, not escort 120/55, not CAP 180/40
for land observe). Repair MUST NOT copy Channel, Normandy, or Caucasus
`channel_place` geometry onto Syria.

#### Scenario: Syria recon invent allowed
- **WHEN** invent is asked for recon on Syria
- **THEN** the planner MUST be allowed to emit `theatre: Syria` with
  `airfield: Incirlik` and AOI geometry from the Syria inland place/schema
  (MUST NOT be required to emit TheChannel, Manston 125/76, CAP 180/40, or
  Kutaisi 43/110)
