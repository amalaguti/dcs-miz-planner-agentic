## MODIFIED Requirements

### Requirement: Nevada invent is free_flight only
Invent/chat SHALL allow all six mission types when the bound theatre is
`Nevada` (home `Nellis`; CAP/intercept/escort station 350° / 40 km north over
desert north-range land; GA/recon AOI 303° / 85 km inland past Creech —
not Manston 125/76, not Cherbourg 180/63, not escort 120/55, not CAP 350/40
for land observe). Repair MUST NOT copy Channel, Normandy, Caucasus, or Syria
`channel_place` geometry onto Nevada.

#### Scenario: Nevada recon invent allowed
- **WHEN** invent is asked for recon on Nevada
- **THEN** the planner MUST be allowed to emit `theatre: Nevada` with
  `airfield: Nellis` and AOI geometry from the Nevada inland place/schema
  (MUST NOT be required to emit TheChannel, Manston 125/76, CAP 350/40,
  Aleppo 121/200, or Kutaisi 43/110)
