## ADDED Requirements

### Requirement: Prefs and history tools
The system SHALL expose callable tools `get_user_prefs`, `set_user_prefs`,
`record_generation`, `record_feedback`, and `list_generation_history` that read and write
user-memory tables. Results MUST be structured `{ok: …}` dicts consistent with other
agent tools. These tools MUST NOT invent DCS identifiers or bypass validation/compile.

#### Scenario: Get prefs when empty
- **WHEN** `get_user_prefs` is called with no prefs stored
- **THEN** the result MUST report ok and an empty prefs map

#### Scenario: Set and get prefs
- **WHEN** `set_user_prefs` writes a preference and `get_user_prefs` is called
- **THEN** the result MUST include that preference

#### Scenario: List recent history
- **WHEN** at least one generation has been recorded and `list_generation_history` is called
- **THEN** the result MUST include that generation in the recent list

## MODIFIED Requirements

### Requirement: Stable import surface
Agent-facing callers MUST be able to import the tool callables from a single package surface
(e.g. `dcs_miz_planner.tools`) without depending on unrelated internal modules for catalog
lookup, validate/compile, and user-memory operations.

#### Scenario: Import tools package
- **WHEN** a test imports the tools surface
- **THEN** the catalog, validate/compile, and user-memory tools MUST be available for
  invocation
