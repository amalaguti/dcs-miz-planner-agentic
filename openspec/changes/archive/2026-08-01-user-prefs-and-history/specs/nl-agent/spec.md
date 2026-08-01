## ADDED Requirements

### Requirement: Planner consults user preferences
During natural-language planning, the agent SHALL be able to read user preferences via
the prefs tools (or equivalent host-provided prefs context). When the user leaves a
planning knob unspecified, the agent MUST prefer stored prefs over inventing a default,
without overriding an explicit user request.

#### Scenario: Stub can read prefs tool
- **WHEN** tests run the planner with a stub LLM configured to call `get_user_prefs`
- **THEN** the tool bridge MUST invoke the real prefs implementation and return its result
  to the loop

### Requirement: Planner records generation history
After a planning attempt reaches a terminal outcome (successful Spec write, or recorded
validation/compile failure), the system SHALL append a generation history row. Recording
MUST be performed by the host planner path and MUST NOT rely solely on the LLM choosing
to call `record_generation`.

#### Scenario: Successful stub plan writes history
- **WHEN** the planner succeeds in stub mode and writes a Spec
- **THEN** generation history MUST contain a success row referencing that Spec path

## MODIFIED Requirements

### Requirement: Tool-using agent loop
The planning agent SHALL be able to invoke the existing agent tools
(`find_airfield`, `get_aircraft_details`, `list_mission_options`, `validate_mission_spec`,
optionally `compile_mission`, and the user-memory tools) during planning. The agent MUST
prefer tool results over invented DCS identifiers.

#### Scenario: Stub exercises tool bridge
- **WHEN** tests run the planner with a stub LLM configured to call `find_airfield`
- **THEN** the tool bridge MUST invoke the real `find_airfield` implementation and return its result to the loop
