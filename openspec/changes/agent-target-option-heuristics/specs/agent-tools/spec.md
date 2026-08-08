## ADDED Requirements

### Requirement: Tool guidance for target invent order
Agent tool descriptions (or invent-facing notes) for `list_strike_targets` and
`list_mission_options` SHALL state that GA/recon invent should call those tools
before emitting `targets[]`, preferring returned unit ids and shelf presets
(motion / ai_preset) over invented strings.

#### Scenario: list_strike_targets description mentions invent order
- **WHEN** TOOL_DEFINITIONS for `list_strike_targets` are loaded
- **THEN** the description MUST mention calling before inventing targets[] and
  preferring returned unit ids
