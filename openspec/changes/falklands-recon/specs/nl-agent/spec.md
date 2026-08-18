## MODIFIED Requirements

### Requirement: Falklands invent is free_flight only
Invent/chat SHALL allow all six mission types when the bound theatre is
`Falklands` (home `MountPleasant`; CAP/intercept/escort station 150° / 40 km
SSE over the South Atlantic sea; GA/recon AOI 269° / 21 km inland short of
Goose Green — not Manston 125/76, not Cherbourg 180/63, not escort 120/55,
not CAP 150/40 for land observe, not Nevada 303/85, not Aleppo 121/200, not
Kutaisi 43/110). Repair MUST NOT copy Channel, Normandy, Caucasus, Syria, or
Nevada `channel_place` geometry onto Falklands.

#### Scenario: Falklands recon invent allowed
- **WHEN** invent is asked for recon on Falklands
- **THEN** the planner MUST be allowed to emit `theatre: Falklands` with
  `airfield: MountPleasant` and AOI geometry from the East Falkland inland
  place/schema (MUST NOT be required to emit TheChannel, Manston 125/76,
  CAP 150/40, Nevada 303/85, Aleppo 121/200, or Kutaisi 43/110)
