# NL Agent

## Purpose

Natural-language planning that uses agent tools and emits a validated Mission Spec.
The LLM never writes DCS Lua or `.miz` contents; compilation stays deterministic.

## Requirements

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

### Requirement: Tool-using agent loop
The planning agent SHALL be able to invoke the existing agent tools
(`find_airfield`, `get_aircraft_details`, `list_mission_options`, `validate_mission_spec`,
optionally `compile_mission`, the user-memory tools, and research guidance when available)
during planning. The agent MUST prefer tool results over invented DCS identifiers.

#### Scenario: Stub exercises tool bridge
- **WHEN** tests run the planner with a stub LLM configured to call `find_airfield`
- **THEN** the tool bridge MUST invoke the real `find_airfield` implementation and return its result to the loop

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

### Requirement: Validate before accepting Spec
Before treating a planned Spec as successful output, the system SHALL validate it with the
shared validation engine. Invalid Specs MUST NOT be written as success without surfacing
errors (a single automated repair attempt after validation failure is allowed).

#### Scenario: Invalid Spec is not silently accepted
- **WHEN** the model proposes a Spec that fails validation
- **THEN** the planner MUST NOT report overall success without either a successful repair
  or a structured failure including validation errors

### Requirement: Offline stub for CI
The system SHALL provide a stub/fake LLM mode that requires no network and no API key so
CI and local tests can exercise the planner loop, YAML write, and validate/compile path.

#### Scenario: Stub plans Manston free flight
- **WHEN** the planner runs in stub mode for a Manston cold free-flight style request
- **THEN** it MUST produce a Spec that validates and can compile under test inventory

### Requirement: Live provider configuration
Live planning SHALL read API credentials and model settings from environment (or explicit
config), MUST NOT hard-code secrets, and MUST fail clearly when the key is missing for
non-stub runs.

#### Scenario: Missing API key in live mode
- **WHEN** live mode is requested without an API key configured
- **THEN** the system MUST fail with a clear error directing the user to set the key or use stub mode

### Requirement: Planner may emit CAP Specs
The NL planning rules SHALL allow Mission Spec `mission_type` `cap` with a nested `cap`
block (airfield-relative bearing/distance, altitude, pattern, engagement) and MUST NOT
instruct the model to invent raw map coordinates or unsupported mission types beyond the
allow-list. CAP Specs MUST still pass host validation before acceptance.

#### Scenario: Stub or documented allow-list includes cap
- **WHEN** planning rules / system prompt are composed for Channel MVP planning
- **THEN** `cap` MUST be listed among supported mission types alongside `free_flight` and
  `intercept`

### Requirement: Planner may emit ground-attack Specs
The NL planning rules SHALL allow Mission Spec `mission_type` `ground_attack` with a nested
`strike` block (airfield-relative bearing/distance, altitude), non-empty `targets`, named
`player.payload`, and `attack_ground` objective, and MUST NOT instruct the model to invent
raw map coordinates, CLSIDs, ground unit ids, or unsupported mission types beyond the
allow-list. Planning rules MUST require strike `targets` to be the opposing coalition to the
player (no friendly fire). For Channel-crossing ground-attack, planning guidance MUST prefer
a slipper-tank payload preset and MUST remind that the tank is jettisoned by the pilot
before the attack (not via invented Lua). Ground-attack Specs MUST still pass host
validation before acceptance.

#### Scenario: Stub or documented allow-list includes ground_attack
- **WHEN** planning rules / system prompt are composed for Channel MVP planning
- **THEN** `ground_attack` MUST be listed among supported mission types alongside
  `free_flight`, `intercept`, and `cap`

### Requirement: Interactive chat coexists with one-shot plan
The NL agent layer SHALL support both a one-shot planning entrypoint and a multi-turn
interactive chat session. Interactive chat MUST reuse the same tool bridge, preference
consultation, squadron voice composition, validation-before-accept, and generation-history
recording contracts as one-shot planning when a Spec is accepted. Chat-specific REPL UX
is specified under the `plan-repl` capability.

#### Scenario: Shared tools available in chat
- **WHEN** an interactive chat session runs with the standard tool set enabled
- **THEN** registered planning tools (including catalog and prefs tools) MUST be
  dispatchable under the same bridge rules as one-shot planning

### Requirement: Derived Spec shape for planning prompts
The NL agent system prompt SHALL include a short always-on reminder of Mission Spec
anti-patterns (nested `player`, `date` as `{year,month,day}`, top-level `objectives`,
no flat `airfield`/`aircraft`) and MUST instruct the model to obtain the type-specific
example via `get_mission_spec_schema` (or an equivalent host-injected derived fragment)
before emitting Spec JSON. The prompt MUST NOT rely on a hand-maintained full CAP (or
other mission-type) JSON skeleton as the sole Spec shape authority.

#### Scenario: Composed prompt points at schema tool or derived shape
- **WHEN** the system prompt is composed for one-shot or chat planning
- **THEN** it MUST mention `get_mission_spec_schema` (or clearly state that the host
  provides the derived Spec example) and MUST include anti-pattern guidance for nested
  `player` and object `date`

### Requirement: Host repair uses derived Spec example
When the host rejects assistant Spec JSON during one-shot planning or chat, the repair
nudge MUST include a derived compact Spec example for the relevant `mission_type`
(inferred from the rejected JSON when present) rather than only a prose error string.

#### Scenario: Parse failure nudge includes example
- **WHEN** the model emits Spec-like JSON that fails Mission Spec validation
- **THEN** the next host repair message MUST include a derived example Spec (or
  equivalent fragment) for a supported mission type alongside the error
