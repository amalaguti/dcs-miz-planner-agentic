## ADDED Requirements

### Requirement: Brief mentions discipline when armed
When `player.flight.discipline` is armed, generated briefing/voice text SHALL
mention that leaving the section may trigger rejoin warnings or mission
consequences. Specs without discipline MUST keep prior brief behaviour for this
topic.

#### Scenario: Discipline brief note
- **WHEN** briefing a Spec with discipline armed
- **THEN** Procedures or Watch-outs MUST indicate section-discipline / rejoin expectations
