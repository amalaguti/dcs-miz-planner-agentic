## MODIFIED Requirements

### Requirement: Normandy invent is free_flight or CAP
Invent/chat SHALL allow all six mission types when the bound theatre is
`Normandy` (home `NeedsOarPoint`; CAP/intercept/escort station 180° / 63 km;
GA/recon AOI 180° / 133 km inland of Maupertus — not Manston 125/76, not
Hawkinge, not escort 120/55). Repair MUST NOT copy Channel `channel_place`
geometry (french coast belts, Hawkinge/Dunkirk bearings) onto Normandy.

#### Scenario: Normandy recon invent allowed
- **WHEN** invent is asked for recon on Normandy
- **THEN** the planner MUST be allowed to emit `theatre: Normandy` with
  `airfield: NeedsOarPoint` and AOI geometry from the Normandy inland
  place/schema (MUST NOT be required to emit TheChannel or Manston 125/76)
