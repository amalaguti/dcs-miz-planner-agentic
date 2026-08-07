## ADDED Requirements

### Requirement: Tools surface player flight options
Agent-facing tools that expose planning options or Spec shape MUST surface the player
flight size/role knobs once present in planning-options / schema, without adding compile
or write tools beyond the existing host trust boundary.

#### Scenario: List options returns flight knobs
- **WHEN** `list_mission_options` (or equivalent) runs after catalog sync
- **THEN** results MUST include the player flight size and role options
