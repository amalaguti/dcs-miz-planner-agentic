## ADDED Requirements

### Requirement: Compile intercept at Batumi
The compiler SHALL compile a Caucasus intercept Mission Spec that cold-starts
the player Su-25T at Batumi and places Russia Su-25T enemies inflight on the
packaged Black Sea recipe (Batumi + 270° / 40 km). It MUST bind PyDCS
`Caucasus` terrain. It MUST NOT write Channel Hawkinge/Dover coordinates.

#### Scenario: Batumi intercept contracts
- **WHEN** `examples/batumi_dawn_intercept.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Caucasus`, player type `Su-25T`,
  `airdromeId` 22, cold parking, start_time 21600, player radio 251.0 MHz,
  country `Russia`, and enemy coordinates `-355810.6875`, `577386.1875`

### Requirement: Human acceptance for Caucasus intercept in DCS
A compiled Batumi intercept `.miz` MUST be openable in the DCS Mission Editor
and flyable as Instant Action with Caucasus and Su-25T installed. This is
human do-soon after merge, not a hermetic merge gate.

#### Scenario: Load Caucasus intercept in DCS
- **WHEN** a user opens the compiled Caucasus intercept `.miz` in DCS ME or
  Instant Action
- **THEN** the mission MUST load without editor errors and present the player
  cold-started at Batumi with bandits west over the Black Sea

## MODIFIED Requirements

### Requirement: Intercept enemy spawn is TheChannel-only
The compiler SHALL use the packaged intercept spawn recipe for Spec theatre
`TheChannel` (Hawkinge + Dover-approach offset), `Normandy` (NeedsOarPoint +
180° / 63 km), and `Caucasus` (Batumi + 270° / 40 km). Other theatres MUST
fail closed. Channel enemy coordinates MUST remain the existing Hawkinge
golden pair.

#### Scenario: Channel intercept still uses Hawkinge recipe
- **WHEN** a TheChannel intercept Spec is compiled
- **THEN** enemy placement MUST still use the existing Hawkinge anchor plus
  Dover-approach offset
