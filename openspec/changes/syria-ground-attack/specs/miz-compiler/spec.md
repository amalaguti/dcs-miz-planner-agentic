## ADDED Requirements

### Requirement: Compile ground_attack at Incirlik
The compiler SHALL compile a Syria ground_attack Mission Spec that cold-starts
the player Su-25T at Incirlik with payload `su25t_2x_fab250` and places Syria
Ural-375 (and companions) at the packaged Aleppo inland station (121° / 200 km
/ 2000 m). It MUST bind PyDCS `Syria` terrain. It MUST NOT write Channel
Manston french-coast 125/76 or Caucasus Kutaisi 43/110 as the required
destination.

#### Scenario: Incirlik Aleppo ground_attack contracts
- **WHEN** `examples/incirlik_aleppo_ground_attack.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Syria`, player type `Su-25T`,
  `airdromeId` 16, cold parking, start_time 32400, player radio 251.0 MHz,
  FAB-250 stores, Ground Attack tasking, and country `Syria` on land targets

### Requirement: Human acceptance for Syria ground_attack in DCS
A compiled Incirlik Aleppo ground_attack `.miz` MUST be openable in the DCS
Mission Editor and flyable as Instant Action with Syria and Su-25T installed.
This is human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Syria ground_attack in DCS
- **WHEN** a user opens the compiled Syria GA `.miz` in DCS ME or Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Incirlik with a land strike inland past Aleppo
