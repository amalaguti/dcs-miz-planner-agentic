## ADDED Requirements

### Requirement: Spec schema notes include group life less
When `get_mission_spec_schema` describes typed triggers, it MUST mention optional
condition `group_life_less` (`enemy_index` or `target_index` plus `percent` 1–100 for
remaining group life) alongside existing dead, flag, sound, and radio notes. Notes MUST
NOT invent Lua or raw DCS group ids.

#### Scenario: Schema mentions group_life_less
- **WHEN** an agent requests the Spec schema for a mission type that supports triggers
- **THEN** the notes MUST reference `group_life_less` without inventing unsupported fields
