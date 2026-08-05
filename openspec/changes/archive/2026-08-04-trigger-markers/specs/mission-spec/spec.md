## ADDED Requirements

### Requirement: Triggers may use map marks and zone smoke
When a Mission Spec includes a trigger action `mark`, it MUST identify the location by
Spec zone name and provide mark `text`. When it includes `smoke`, it MUST identify the
location by Spec zone name and a curated smoke `color`. The Spec MUST NOT carry raw map
coordinates or free-form Lua for these actions.

#### Scenario: Mark fields
- **WHEN** a Spec declares `type: mark` with `zone` and `text`
- **THEN** loading MUST succeed when the rest of the Spec is valid

#### Scenario: Smoke fields
- **WHEN** a Spec declares `type: smoke` with `zone` and a curated `color`
- **THEN** loading MUST succeed when the rest of the Spec is valid
