## ADDED Requirements

### Requirement: Spec schema notes include triggers
When `get_mission_spec_schema` (or equivalent prompt fragment) describes a mission type, it
MUST mention that optional typed `zones` / `triggers` may appear, MUST NOT encourage Lua or
script fields, and MUST note that compiling non-empty triggers awaits native trigger
compilation.

#### Scenario: Schema notes mention triggers
- **WHEN** an agent requests the Spec schema for `free_flight` or `cap`
- **THEN** the notes or example guidance MUST reference optional triggers/zones without
  inventing unsupported condition types
