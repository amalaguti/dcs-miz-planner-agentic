## MODIFIED Requirements

### Requirement: Syria invent is free_flight only
Invent/chat SHALL allow `free_flight`, `cap`, and `intercept` when the bound
theatre is `Syria` (home `Incirlik`; intercept spawn on the Iskenderun
corridor 180° / 40 km — not Hawkinge, not Cherbourg 180/63, not Batumi
270/40). It SHALL refuse `ground_attack`, `escort`, and `recon` on Syria
every turn.

#### Scenario: Syria intercept invent allowed
- **WHEN** invent is asked for an intercept on Syria
- **THEN** the planner MUST be allowed to emit `theatre: Syria` with
  `airfield: Incirlik` (MUST NOT be required to emit TheChannel, Hawkinge,
  Cherbourg, or Batumi spawn)
