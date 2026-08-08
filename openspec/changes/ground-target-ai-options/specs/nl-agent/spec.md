## ADDED Requirements

### Requirement: NL agent may set target AI presets
The invent path SHALL be allowed to emit curated `ai_preset` / allowlisted `ai`
and land `move_formation` on GA/recon targets per class heuristics (convoy
transit, AAA alert, ship under way), and MUST NOT invent free-form ME option
names or air-only options on ground/sea targets.

#### Scenario: Agent emits convoy transit style
- **WHEN** the pilot asks for a moving truck column inland
- **THEN** the agent MAY emit soft-vehicle targets with transit preset or
  allowlisted ai/move_formation fields
