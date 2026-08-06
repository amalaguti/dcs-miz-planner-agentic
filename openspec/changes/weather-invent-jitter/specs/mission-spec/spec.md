## ADDED Requirements

### Requirement: Optional weather_opts seed on Mission Spec
The Mission Spec MAY include optional `weather_opts` with integer `seed`.
Omitted `weather_opts` MUST remain valid. Unknown keys under `weather_opts`
MUST be rejected. The top-level `weather` field MUST remain a WeatherPreset
enum id (not a nested object).

#### Scenario: Spec with weather_opts seed loads
- **WHEN** a Spec sets `weather: broken_channel` and `weather_opts: { seed: 42 }`
- **THEN** structural load MUST succeed

#### Scenario: Spec without weather_opts still loads
- **WHEN** a Spec omits `weather_opts`
- **THEN** structural load MUST succeed as today
