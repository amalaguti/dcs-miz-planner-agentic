## MODIFIED Requirements

### Requirement: Caucasus invent is free_flight or CAP
Invent/chat SHALL allow all six mission types when the bound theatre is
`Caucasus` (home `Batumi`; CAP/intercept/escort station 270° / 40 km west
over the Black Sea; GA/recon AOI 43° / 110 km inland past Kutaisi — not
Manston 125/76, not Cherbourg 180/63, not escort 120/55). Repair MUST NOT
copy Channel `channel_place` geometry (french coast belts, Hawkinge/Dunkirk)
or Normandy NeedsOarPoint geometry onto Caucasus.

#### Scenario: Caucasus recon invent allowed
- **WHEN** invent is asked for recon on Caucasus
- **THEN** the planner MUST be allowed to emit `theatre: Caucasus` with
  `airfield: Batumi` and AOI geometry from the Caucasus inland
  place/schema (MUST NOT be required to emit TheChannel or Manston 125/76)
