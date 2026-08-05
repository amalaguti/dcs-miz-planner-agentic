## ADDED Requirements

### Requirement: Spec schema notes include mark and smoke
When `get_mission_spec_schema` describes typed triggers, it MUST mention optional actions
`mark` (zone name + text for F10 map mark) and `smoke` (zone name + curated color for ME
Smoke Marker) alongside existing dead, life-less, flag, sound, and radio notes. Notes MUST
NOT invent Lua, raw map coordinates, or author mark ids.

#### Scenario: Schema mentions mark and smoke
- **WHEN** an agent requests the Spec schema for a mission type that supports triggers
- **THEN** the notes MUST reference `mark` and `smoke` without inventing unsupported fields
