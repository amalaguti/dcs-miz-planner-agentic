## MODIFIED Requirements

### Requirement: Normandy invent is free_flight or CAP
Invent/chat SHALL allow `free_flight`, `cap`, `ground_attack`, and `intercept`
when the bound theatre is `Normandy` (home `NeedsOarPoint`; CAP/intercept
station from Normandy `channel_place` meta — 180° / 63 km — not Manston
135/25 or Hawkinge; GA strike 180° / 133 km inland of Maupertus). It SHALL
refuse `escort` and `recon` on Normandy every turn (never capture or write a
refused Spec). Repair for refused types MUST nudge toward NeedsOarPoint
free_flight, CAP, ground_attack, or intercept, or switching theatre to
TheChannel. Invent MUST NOT copy Channel `channel_place` geometry (french
coast belts, Hawkinge/Dunkirk bearings) onto Normandy.

#### Scenario: Normandy intercept invent allowed
- **WHEN** invent is asked for an intercept on Normandy
- **THEN** the planner MUST be allowed to emit `theatre: Normandy` with
  `airfield: NeedsOarPoint` (MUST NOT be required to emit TheChannel or
  Hawkinge spawn)

#### Scenario: Normandy escort invent still refused every turn
- **WHEN** invent is asked for an escort on Normandy
- **THEN** it MUST NOT emit a combat Mission Spec and MUST surface a repair
  toward NeedsOarPoint free_flight, CAP, ground_attack, or intercept (or
  TheChannel combat)
