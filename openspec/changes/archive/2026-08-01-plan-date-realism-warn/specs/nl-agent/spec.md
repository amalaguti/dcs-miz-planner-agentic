## MODIFIED Requirements

### Requirement: Natural language planning entrypoint
The system SHALL accept a natural-language mission request via a Python API and a CLI
command and produce a Mission Spec YAML path (or structured failure). The agent MUST NOT
emit DCS mission Lua or write `.miz` contents directly; compilation MUST use the existing
compiler when requested.

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
