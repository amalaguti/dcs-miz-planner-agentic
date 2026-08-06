## ADDED Requirements

### Requirement: Fog dynamics capability
The system SHALL support invent-time static weather plus optional mid-sortie fog
evolution via curated scripting as specified under mission-spec and miz-compiler.
Cloud preset, precip, and wind MUST remain fixed for the loaded mission.

#### Scenario: Scope honesty
- **WHEN** product docs or catalog describe fog dynamics
- **THEN** they MUST NOT claim mid-flight sunny-to-rain or gallery swaps
