## MODIFIED Requirements

### Requirement: Nevada invent is free_flight only
Invent/chat SHALL allow `free_flight` and `cap` when the bound theatre is
`Nevada` (home `Nellis`; CAP station 350° / 40 km north over desert north-range
land — not Cherbourg 180/63, not Batumi 270/40, not Incirlik 180/40, not
Creech 303/40). It SHALL refuse `intercept`, `ground_attack`, `escort`, and
`recon` on Nevada every turn.

#### Scenario: Nevada CAP invent allowed
- **WHEN** invent is asked for a CAP on Nevada
- **THEN** the planner MUST be allowed to emit `theatre: Nevada` with
  `airfield: Nellis` and CAP geometry from the Nevada place/schema
  (MUST NOT be required to emit TheChannel, Cherbourg 180/63, Batumi 270/40,
  or Incirlik 180/40)
