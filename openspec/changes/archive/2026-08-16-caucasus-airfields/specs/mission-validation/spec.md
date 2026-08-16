## ADDED Requirements

### Requirement: Caucasus Mozdok freeflight validates
Shared validation SHALL accept a well-formed Caucasus free-flight Spec with
airfield `Mozdok` and player country `Russia` on coalition red when inventory
agrees. Channel/Normandy MUST still reject `Russia` as unknown-country.

#### Scenario: Needs Mozdok freeflight validates
- **WHEN** `examples/mozdok_cold_freeflight.yaml` is validated against an
  inventory that includes offerable Caucasus
- **THEN** validation MUST succeed

#### Scenario: Channel rejects Russia
- **WHEN** a TheChannel Mission Spec sets player country `Russia`
- **THEN** validation MUST fail with an unknown-country error
