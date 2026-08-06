## ADDED Requirements

### Requirement: Expanded Channel weather pattern ids
The Mission Spec `weather` field SHALL accept additional named Channel weather
pattern ids beyond `sunny_clear`, `dawn_clear`, and `marginal_vfr`, including at
least campaign-seeded patterns for light scattered, high scattered, broken,
overcast, rain overcast, and scattered summer (exact enum snake_case ids as
packaged). Unknown weather ids MUST still fail validation.

#### Scenario: New pattern Spec loads
- **WHEN** a Spec sets `weather` to a packaged expanded pattern id
- **THEN** loading and validation MUST succeed when the rest of the Spec is valid

#### Scenario: Unknown weather still rejected
- **WHEN** a Spec sets `weather` to an id not in the WeatherPreset enum
- **THEN** loading or validation MUST fail with a clear weather error
