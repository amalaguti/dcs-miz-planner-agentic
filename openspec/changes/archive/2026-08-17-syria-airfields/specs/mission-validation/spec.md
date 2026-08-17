## ADDED Requirements

### Requirement: Syria Palmyra freeflight validates
Shared validation SHALL accept a well-formed Syria free-flight Spec with
airfield `Palmyra` and player country `Syria` on coalition red when inventory
agrees. Channel/Normandy MUST still reject country `Syria` as unknown-country.

#### Scenario: Palmyra freeflight validates
- **WHEN** `examples/palmyra_cold_freeflight.yaml` is validated against
  an inventory that includes offerable Syria
- **THEN** validation MUST succeed

#### Scenario: Channel rejects country Syria
- **WHEN** a TheChannel Mission Spec sets player country `Syria`
- **THEN** validation MUST fail with an unknown-country error
