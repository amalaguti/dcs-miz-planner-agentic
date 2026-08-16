## ADDED Requirements

### Requirement: Cold parking freeflight at Mozdok
The compiler SHALL place the player Su-25T as a cold start from parking at
Mozdok on Caucasus when the Spec requests that combination. Group radio MUST
be 251.0 MHz. Player country `Russia` MUST be on coalition red. It MUST bind
PyDCS `Caucasus` terrain. It MUST NOT write Normandy `airdromeId` 28 as
Needs Oar Point.

#### Scenario: Needs Mozdok contracts
- **WHEN** `examples/mozdok_cold_freeflight.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Caucasus`, player type `Su-25T`,
  `airdromeId` 28, cold parking, start_time 32400, player radio 251.0 MHz,
  and country `Russia`
