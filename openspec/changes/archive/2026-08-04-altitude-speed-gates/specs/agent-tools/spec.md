## ADDED Requirements

### Requirement: Spec schema notes include altitude and speed gates
When `get_mission_spec_schema` describes typed triggers, it MUST mention optional
conditions `unit_altitude_higher` / `unit_altitude_lower` (`altitude_m`, optional `agl`)
and `unit_speed_higher` / `unit_speed_lower` (`speed_kmh`) as player-unit gates alongside
existing dead, life-less, flag, sound, mark/smoke, and radio notes. Notes MUST NOT invent
Lua, raw unit ids, or enemy-targeted altitude/speed fields.

#### Scenario: Schema mentions altitude and speed gates
- **WHEN** an agent requests the Spec schema for a mission type that supports triggers
- **THEN** the notes MUST reference altitude and speed gate conditions without inventing
  unsupported fields
