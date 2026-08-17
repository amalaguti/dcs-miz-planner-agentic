## ADDED Requirements

### Requirement: Compile ground-attack at Batumi
The compiler SHALL compile a Caucasus ground-attack Mission Spec that
cold-starts the player Su-25T at Batumi with the named FAB-250 payload,
GroundAttack tasking toward the airfield-relative strike point inland past
Kutaisi, and declared Russia land target groups. It MUST bind PyDCS
`Caucasus` terrain (not TheChannel or Normandy). It MUST NOT write Channel
Hawkinge/Dover intercept coordinates. Modern ground units MUST use PyDCS
country `Russia` on red when the Spec says so.

#### Scenario: Batumi ground-attack contracts
- **WHEN** `examples/batumi_kutaisi_ground_attack.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Caucasus`, player type `Su-25T`,
  `airdromeId` 22, cold parking, start_time 32400, player radio 251.0 MHz,
  GroundAttack tasking, target type `Ural-375`, country Russia, and FAB-250
  CLSID `{3C612111-C7AD-476E-8A8E-2485812F4E5C}`

### Requirement: Human acceptance for Caucasus ground-attack in DCS
A compiled Batumi ground-attack `.miz` MUST be openable in the DCS Mission
Editor and flyable as Instant Action with Caucasus and Su-25T installed. This
is human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Caucasus ground-attack in DCS
- **WHEN** a user opens the compiled Caucasus ground-attack `.miz` in DCS ME
  or Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Batumi with a strike inland past Kutaisi
