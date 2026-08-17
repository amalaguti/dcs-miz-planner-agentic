## MODIFIED Requirements

### Requirement: Syria invent is free_flight only
Invent/chat SHALL allow `free_flight` and `cap` when the bound theatre is
`Syria` (home `Incirlik`; CAP station 180° / 40 km south over the Gulf of
Iskenderun — not Cherbourg 180/63, not Batumi 270/40). It SHALL refuse
`intercept`, `ground_attack`, `escort`, and `recon` on Syria every turn.

#### Scenario: Syria CAP invent allowed
- **WHEN** invent is asked for a CAP on Syria
- **THEN** the planner MUST be allowed to emit `theatre: Syria` with
  `airfield: Incirlik` and CAP geometry from the Syria place/schema
  (MUST NOT be required to emit TheChannel, Cherbourg 180/63, or Batumi 270/40)
