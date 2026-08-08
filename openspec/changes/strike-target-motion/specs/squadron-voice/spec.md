## ADDED Requirements

### Requirement: Brief mentions contacts under way when moving
When a Spec has one or more non-static `targets[]` motion values, squadron-commander
voice SHOULD mention that contacts are under way / on the move (while keeping
surfaced-only U-boat language when `Uboat_VIIC` is present). Static-only Specs
MUST NOT claim movement.

#### Scenario: Moving U-boat brief
- **WHEN** a commander brief is generated for a Spec with `Uboat_VIIC` and patrol/path
- **THEN** the text MUST indicate the contact is under way (and MUST NOT claim ASW)
