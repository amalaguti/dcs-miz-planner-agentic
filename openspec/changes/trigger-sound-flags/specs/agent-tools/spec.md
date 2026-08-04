## ADDED Requirements

### Requirement: Spec schema notes include sound and numeric flags
When `get_mission_spec_schema` describes typed triggers, it MUST mention optional action
`sound` (curated `asset_id` only) and optional numeric/timed flag vocabulary
(`flag_equals` / `flag_more` / `flag_less` / `time_since_flag`, `inc_flag` /
`set_flag_value`) alongside existing bool flags and radio/late-activation notes. Notes
MUST NOT invent Lua or arbitrary sound path fields.

#### Scenario: Schema mentions sound and numeric flags
- **WHEN** an agent requests the Spec schema for a mission type that supports triggers
- **THEN** the notes MUST reference sound `asset_id` and numeric flag types without
  inventing unsupported fields
