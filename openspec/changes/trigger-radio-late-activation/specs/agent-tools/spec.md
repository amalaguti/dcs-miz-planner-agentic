## ADDED Requirements

### Requirement: Spec schema notes include radio and late activation
When `get_mission_spec_schema` describes combat mission types that support enemies or
targets, it MUST mention optional `late_activation` on those entries and optional trigger
actions `radio_item_add` / `radio_item_remove` / `activate_group` / `deactivate_group`
(native ME; no Lua).

#### Scenario: CAP or intercept schema mentions radio actions
- **WHEN** an agent requests the Spec schema for `cap` or `intercept`
- **THEN** the notes MUST reference radio and/or late activation without inventing Lua
  fields
