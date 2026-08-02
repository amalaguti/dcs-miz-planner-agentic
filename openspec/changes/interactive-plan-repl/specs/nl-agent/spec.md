## ADDED Requirements

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
