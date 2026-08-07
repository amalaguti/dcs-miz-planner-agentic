## ADDED Requirements

### Requirement: Showers invent stays in light-rain family
For `showers_scattered`, invent MUST pick `cloud_preset` only from that
pattern’s allowed light-rain gallery family and MUST NOT select
`RainyPreset1`–`3` (overcast rain) or non-rainy presets.

#### Scenario: Showers seed stays light rain
- **WHEN** invent resolves `showers_scattered` for any season/seed
- **THEN** the resolved `cloud_preset` MUST be one of the pattern’s declared
  light-rain gallery ids
