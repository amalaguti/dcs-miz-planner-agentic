## ADDED Requirements

### Requirement: Compile ground_attack at Nellis
The compiler SHALL compile a Nevada ground_attack Mission Spec that cold-starts
the player Su-25T at Nellis with payload `su25t_2x_fab250` and places Russia
Ural-375 (and companions) at the packaged Creech inland station (303° / 85 km
/ 2000 m). It MUST bind PyDCS `Nevada` terrain. It MUST NOT write Channel
Manston french-coast 125/76, Syria Aleppo 121/200, Caucasus Kutaisi 43/110, or
the Nevada CAP 350/40 station as the required destination.

#### Scenario: Nellis Creech ground_attack contracts
- **WHEN** `examples/nellis_creech_ground_attack.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Nevada`, player type `Su-25T`,
  `airdromeId` 4, cold parking, start_time 32400, player radio 251.0 MHz,
  FAB-250 stores, Ground Attack tasking, and country `Russia` on land targets

### Requirement: Human acceptance for Nevada ground_attack in DCS
A compiled Nellis Creech ground_attack `.miz` MUST be openable in the DCS
Mission Editor and flyable as Instant Action with Nevada and Su-25T installed.
This is human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Nevada ground_attack in DCS
- **WHEN** a user opens the compiled Nevada GA `.miz` in DCS ME or Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Nellis with a land strike inland past Creech
