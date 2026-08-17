## MODIFIED Requirements

### Requirement: Nevada invent is free_flight only
Invent/chat SHALL allow `free_flight`, `cap`, and `intercept` when the bound
theatre is `Nevada` (home `Nellis`; intercept spawn on the desert north-range
corridor 350° / 40 km — not Hawkinge, not Incirlik 180/40, not Batumi 270/40,
not Cherbourg 180/63). It SHALL refuse `ground_attack`, `escort`, and `recon`
on Nevada every turn.

#### Scenario: Nevada intercept invent allowed
- **WHEN** invent is asked for an intercept on Nevada
- **THEN** the planner MUST be allowed to emit `theatre: Nevada` with
  `airfield: Nellis` (MUST NOT be required to emit TheChannel, Hawkinge,
  Incirlik, Cherbourg, or Batumi spawn)
