## ADDED Requirements

### Requirement: Invent maps cues to unit motion and AI preset
The invent path SHALL instruct the agent to consult mission-option shelves and
`list_strike_targets` before emitting GA/recon `targets[]`, and SHALL document a
cue table: inland convoy → soft + path + `convoy_transit`; flak/AAA → aaa +
static + `aaa_alert`; mid-Channel U-boat under way → sea + patrol +
`ship_under_way`; harbour/dock → sea + static + `harbour_static`. The agent MUST
prefer tool-returned unit ids and allowlisted presets only.

#### Scenario: Prompts or schema include cue table
- **WHEN** invent prompts or ground_attack/recon Spec schema notes are loaded
- **THEN** they MUST mention the convoy / flak / U-boat / harbour cue mapping
  (or equivalent) and MUST NOT encourage free-form ME Opt* names
