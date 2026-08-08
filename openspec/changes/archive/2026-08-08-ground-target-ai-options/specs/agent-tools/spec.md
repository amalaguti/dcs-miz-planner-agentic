## ADDED Requirements

### Requirement: Schema documents target AI options
Derived Spec schema notes SHALL document optional `ai_preset`, `ai` allowlisted
keys, `move_formation`, class/domain restrictions, and that ME UI lists are not
capability guarantees.

#### Scenario: Schema mentions target AI
- **WHEN** `get_mission_spec_schema` notes are requested for ground_attack or recon
- **THEN** notes MUST mention target AI / move_formation allowlists
