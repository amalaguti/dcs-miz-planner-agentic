## MODIFIED Requirements

### Requirement: Normandy invent is free_flight or CAP
Invent/chat SHALL allow `free_flight`, `cap`, `ground_attack`, `intercept`,
and `escort` when the bound theatre is `Normandy` (home `NeedsOarPoint`;
CAP/intercept/escort station from Normandy `channel_place` meta — 180° / 63 km
— not Manston 135/25, Hawkinge, or escort 120/55; GA strike 180° / 133 km
inland of Maupertus). It SHALL refuse `recon` on Normandy every turn (never
capture or write a refused Spec). Repair for refused types MUST nudge toward
NeedsOarPoint free_flight, CAP, ground_attack, intercept, or escort, or
switching theatre to TheChannel. Invent MUST NOT copy Channel `channel_place`
geometry (french coast belts, Hawkinge/Dunkirk bearings) onto Normandy.

#### Scenario: Normandy escort invent allowed
- **WHEN** invent is asked for an escort on Normandy
- **THEN** the planner MUST be allowed to emit `theatre: Normandy` with
  `airfield: NeedsOarPoint` (MUST NOT be required to emit TheChannel or
  Manston 120/55)

#### Scenario: Normandy recon invent still refused every turn
- **WHEN** invent is asked for recon on Normandy
- **THEN** it MUST NOT emit a combat Mission Spec and MUST surface a repair
  toward NeedsOarPoint free_flight, CAP, ground_attack, intercept, or escort
  (or TheChannel combat)
