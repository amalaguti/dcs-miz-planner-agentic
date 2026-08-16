## ADDED Requirements

### Requirement: Compile ground-attack at Needs Oar Point
The compiler SHALL compile a Normandy ground-attack Mission Spec that
cold-starts the player Spitfire at Needs Oar Point with the named Channel
crossing payload, GroundAttack tasking toward the airfield-relative strike
point inland of Maupertus, and declared Axis land target groups. It MUST bind
PyDCS `Normandy` terrain (not `Normandy2` or TheChannel). It MUST NOT write
Channel Hawkinge/Dover intercept coordinates. WWII Axis ground units MUST use
PyDCS country `ThirdReich` on red when the Spec says so.

#### Scenario: Needs Oar Point ground-attack contracts
- **WHEN** `examples/needs_oar_point_ground_attack.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Normandy`, player type
  `SpitfireLFMkIX`, `airdromeId` 28, cold parking, start_time 32400, player
  radio 124.0 MHz, GroundAttack tasking, and target types `Blitz_36-6700A`
  and `flak18`

### Requirement: Human acceptance for Normandy ground-attack in DCS
A compiled Needs Oar Point ground-attack `.miz` MUST be openable in the DCS
Mission Editor and flyable as Instant Action with Normandy 2.0 and Spitfire
LF Mk IX installed. This is human do-soon after merge, not a hermetic merge
gate.

#### Scenario: Load Normandy ground-attack in DCS
- **WHEN** a user opens the compiled Normandy ground-attack `.miz` in DCS ME
  or Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Needs Oar Point with a strike inland of Maupertus
