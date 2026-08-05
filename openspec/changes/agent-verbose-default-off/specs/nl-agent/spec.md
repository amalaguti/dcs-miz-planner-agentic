## ADDED Requirements

### Requirement: One-shot plan verbose defaults off
One-shot `plan` MUST default tool-trace / debug stderr output to off. Passing `--verbose`
MUST enable the same tracing used by interactive chat. The shared `DEFAULT_VERBOSE`
constant MUST be false.

#### Scenario: Default plan is quiet
- **WHEN** a user runs plan without `--verbose`
- **THEN** the planner MUST run with verbose off

#### Scenario: Plan --verbose enables traces
- **WHEN** a user runs plan with `--verbose`
- **THEN** LLM round / tool-call tracing MUST be enabled for that run
