## ADDED Requirements

### Requirement: Showers scattered weather pattern id
The Mission Spec `weather` field SHALL accept `showers_scattered` as a
`WeatherPreset` value for Channel light-rain / showery gallery weather, in
addition to existing packaged patterns. Unknown weather ids MUST still fail
validation.

#### Scenario: Showers Spec loads
- **WHEN** a Spec sets `weather: showers_scattered` with an otherwise valid
  free-flight Channel Spec
- **THEN** loading and validation MUST succeed

#### Scenario: Unknown weather still rejected
- **WHEN** a Spec sets `weather` to an id not in the WeatherPreset enum
- **THEN** loading or validation MUST fail with a clear weather error
