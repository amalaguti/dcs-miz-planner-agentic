## ADDED Requirements

### Requirement: Structural asserts for wingman Follow
Tests SHALL assert that a wingman+join_up compile emits Follow (or equivalent ME
follow task wiring) tied to the AI lead and that free-flight lead has an outbound
waypoint.

#### Scenario: Wingman join-up golden smoke
- **WHEN** the suite compiles the wingman join-up example
- **THEN** asserts MUST find Follow/groupId linkage and lead outbound content
