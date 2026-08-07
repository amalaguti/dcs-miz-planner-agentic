## ADDED Requirements

### Requirement: Commander brief includes synthetic METAR
The host-side commander operational brief SHALL include the same synthetic
METAR line required by mission-briefing (from invent `WeatherSnapshot`, offline,
deterministic, simulated remark). Spec field values MUST remain free of
METAR prose.

#### Scenario: CLI brief shows METAR
- **WHEN** `build_commander_brief` runs for a valid Spec with weather set
- **THEN** the brief string MUST include the synthetic METAR line with station id
  and `NOSIG` (or equivalent simulated marker)
