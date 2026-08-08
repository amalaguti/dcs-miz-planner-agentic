## ADDED Requirements

### Requirement: NL invent prefers catalog strike targets
The invent path SHALL be instructed to call `list_strike_targets` (or equivalent
catalog list) before inventing GA/recon `targets[]`, and MUST prefer returned
exact DCS ids rather than inventing unit strings.

#### Scenario: Schema or prompts mention list_strike_targets
- **WHEN** invent prompts or Spec schema notes for ground_attack/recon are loaded
- **THEN** they MUST mention querying strike targets from the catalog tool
