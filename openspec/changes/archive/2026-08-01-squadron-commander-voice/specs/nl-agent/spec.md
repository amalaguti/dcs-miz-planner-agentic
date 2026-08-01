## ADDED Requirements

### Requirement: Planner applies squadron voice
The planning entrypoint SHALL resolve a squadron voice (CLI/API override, else
`squadron_voice` pref, else default `raf`) before the LLM loop and MUST use a system prompt
composed for that voice. Voice application MUST NOT change the requirement that the final
accepted Spec output is a validated Mission Spec (not DCS Lua).

#### Scenario: Stub plan uses composed voice prompt
- **WHEN** tests run the planner in stub mode with an explicit voice `usaaf`
- **THEN** the system prompt provided to the LLM MUST be the composed USAAF persona prompt
  (base rules + USAAF pack)

#### Scenario: Spec remains valid under voice
- **WHEN** a stub plan succeeds under voice `raf` or `usaaf`
- **THEN** the written Mission Spec MUST still validate under the shared validation engine

### Requirement: Planner surfaces commander brief
After a planning run successfully writes a validated Spec, the planner SHALL attach a
commander operational brief (summary, tactics, procedures, watch-outs) to the plan result
and the plan CLI MUST display it when present. The brief MUST be agent/CLI-side only in
this change (not compiled into `.miz` dictionary keys).

#### Scenario: Stub success includes brief sections
- **WHEN** a stub plan succeeds for a Manston free-flight style request
- **THEN** the plan result MUST include a brief containing tactics, procedures, and
  watch-outs content

### Requirement: Planner may research guidance
During planning (especially when preparing the commander brief), the agent SHALL be able
to invoke a research-guidance tool. Stub mode MUST exercise the tool bridge with offline
fixtures. Live mode MAY perform web-backed retrieval. Tool failure MUST NOT by itself mark
a validated Spec plan as failed.

#### Scenario: Stub can call research guidance tool
- **WHEN** tests run the planner with a stub LLM configured to call the research guidance tool
- **THEN** the tool bridge MUST invoke the real stub/offline implementation and return its
  result to the loop

## MODIFIED Requirements

### Requirement: Tool-using agent loop
The planning agent SHALL be able to invoke the existing agent tools
(`find_airfield`, `get_aircraft_details`, `list_mission_options`, `validate_mission_spec`,
optionally `compile_mission`, the user-memory tools, and research guidance when available)
during planning. The agent MUST prefer tool results over invented DCS identifiers.

#### Scenario: Stub exercises tool bridge
- **WHEN** tests run the planner with a stub LLM configured to call `find_airfield`
- **THEN** the tool bridge MUST invoke the real `find_airfield` implementation and return its result to the loop

### Requirement: Natural language planning entrypoint
The system SHALL accept a natural-language mission request via a Python API and a CLI
command and produce a Mission Spec YAML path (or structured failure). The agent MUST NOT
emit DCS mission Lua or write `.miz` contents directly; compilation MUST use the existing
compiler when requested. The plan CLI/API SHOULD accept an optional voice override that
selects the squadron-commander persona for that run.

#### Scenario: Plan writes a Spec file
- **WHEN** a user runs the plan command with a free-flight Manston-style prompt (stub or live)
- **THEN** the system MUST write a Mission Spec YAML that loads as `schema_version` `"1"`

#### Scenario: Compile remains deterministic
- **WHEN** planning is invoked with compile enabled
- **THEN** any `.miz` MUST be produced by the existing PyDCS compiler path, not by the LLM

#### Scenario: Out-of-period date warns but succeeds
- **WHEN** a planned Channel Spec uses a date year outside the usual WWII backdrop
  (about 1939–1945)
- **THEN** the plan MUST still succeed and MUST include a user-visible warning that the
  date does not match that historical backdrop, while noting other eras or modern dates
  remain allowed

#### Scenario: Period date has no realism warning
- **WHEN** a planned Channel Spec uses a date year in 1939–1945
- **THEN** the plan MUST NOT emit that Channel era/date mismatch warning

#### Scenario: Plan accepts voice override
- **WHEN** a user runs the plan command with an explicit `--voice usaaf` (or API equivalent)
- **THEN** the planner MUST resolve voice `usaaf` for that run’s system prompt
