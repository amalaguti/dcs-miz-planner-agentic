## ADDED Requirements

### Requirement: Cold parking Spitfire freeflight at Batumi
The compiler SHALL place the player Spitfire LF Mk IX as a cold start from
parking at Batumi on Caucasus when the Spec requests that combination.
Group radio MUST be 124.0 MHz. It MUST bind PyDCS `Caucasus` terrain.

#### Scenario: Batumi Spitfire contracts
- **WHEN** `examples/batumi_spitfire_freeflight.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Caucasus`, player type
  `SpitfireLFMkIX`, `airdromeId` 22, cold parking, start_time 32400, and
  player radio 124.0 MHz
