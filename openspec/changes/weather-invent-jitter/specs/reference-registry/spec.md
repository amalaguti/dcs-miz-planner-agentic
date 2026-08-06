## ADDED Requirements

### Requirement: Weather patterns declare gallery families for invent
Packaged Channel weather data SHALL allow each gallery-backed WeatherPreset to
declare the set of allowed ME `cloud_preset` ids (within-family) used by invent
priors. Recipe centers remain the default numeric baseline.

#### Scenario: Broken pattern family non-empty
- **WHEN** registry loads weather presets after this change
- **THEN** the broken-channel pattern (or equivalent) MUST expose a non-empty
  allowed gallery family list of Broken-class preset ids
