## ADDED Requirements

### Requirement: Chat verbose defaults off
Interactive plan chat MUST default tool-trace / debug stderr output to off. Users MUST
be able to enable tracing via a CLI flag (`--verbose`) and a slash command (`/verbose on`).
`/verbose off` MUST quiet tracing again. The session banner MUST reflect the current
verbose state.

#### Scenario: Default chat is quiet
- **WHEN** a user starts chat without `--verbose`
- **THEN** the session MUST start with verbose off (banner shows verbose=off) and MUST
  NOT emit `[verbose]` tool-trace lines for normal stub turns

#### Scenario: Enable verbose in chat
- **WHEN** the user enters `/verbose on` (or started with `--verbose`)
- **THEN** subsequent tool-trace lines MAY appear on stderr until `/verbose off`
