## MODIFIED Requirements

### Requirement: Nevada invent is free_flight only
Invent/chat SHALL allow `free_flight`, `cap`, `intercept`, and `escort` when
the bound theatre is `Nevada` (home `Nellis`, `Su-25T`, `sunny_clear`, USA
blue; CAP/intercept/escort station 350° / 40 km north over desert north-range
land — not Cherbourg 180/63, not Batumi 270/40, not Incirlik 180/40, not
Manston escort 120/55). It SHALL refuse `ground_attack` and `recon` on Nevada
every turn (never capture or write a refused Spec). Repair MUST nudge toward
Nellis free_flight, CAP, intercept, or escort, or switching theatre to
TheChannel — not Incirlik, Batumi, NeedsOarPoint, or Manston. Invent MUST NOT
copy Channel, Normandy, Caucasus, or Syria `channel_place` geometry onto
Nevada.

#### Scenario: Nevada escort invent allowed
- **WHEN** invent is asked for an escort on Nevada
- **THEN** the planner MUST be allowed to emit `theatre: Nevada` with
  `airfield: Nellis` (MUST NOT be required to emit TheChannel or Manston
  120/55)
