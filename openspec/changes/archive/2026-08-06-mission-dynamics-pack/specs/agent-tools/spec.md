## ADDED Requirements

### Requirement: Tool surface describes dynamics expand
Agent-facing tool descriptions (`list_mission_options` / schema tool notes as applicable)
MUST mention that `dynamics_mode` catalog rows correspond to Spec `dynamics` expand once
this capability ships.

#### Scenario: list_mission_options description stays honest
- **WHEN** tool definitions are listed after this change
- **THEN** `list_mission_options` description MUST still surface `dynamics_mode` and MUST
  not claim dynamics cannot be emitted if Spec expand exists
