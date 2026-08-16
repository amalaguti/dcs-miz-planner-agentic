## ADDED Requirements

### Requirement: Compile intercept at Needs Oar Point
The compiler SHALL compile a Normandy intercept Mission Spec that cold-starts
the player Spitfire at Needs Oar Point and places Bf-109K-4 enemies inflight
on the packaged Cherbourg-corridor recipe (NeedsOarPoint + 180° / 63 km). It
MUST bind PyDCS `Normandy` terrain. It MUST NOT write Channel Hawkinge/Dover
coordinates.

#### Scenario: Needs Oar Point intercept contracts
- **WHEN** `examples/needs_oar_point_dawn_intercept.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Normandy`, player type
  `SpitfireLFMkIX`, `airdromeId` 28, cold parking, start_time 21600, player
  radio 124.0 MHz, and enemy `Bf-109K-4` at 40.0 MHz

## MODIFIED Requirements

### Requirement: Intercept enemy spawn is TheChannel-only
The compiler SHALL use the packaged intercept spawn recipe for Spec theatre
`TheChannel` (Hawkinge + Dover-approach offset) and `Normandy` (NeedsOarPoint
+ 180° / 63 km). Other theatres MUST fail closed. Channel enemy coordinates
MUST remain the existing Hawkinge golden pair.

#### Scenario: Channel intercept still uses Hawkinge recipe
- **WHEN** a TheChannel intercept Spec is compiled
- **THEN** enemy placement MUST still use the existing Hawkinge anchor plus
  Dover-approach offset
