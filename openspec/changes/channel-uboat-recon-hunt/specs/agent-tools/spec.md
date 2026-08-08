## ADDED Requirements

### Requirement: Agent schema warns surfaced-only U-boat
Derived Spec schema / planning notes SHALL state that Channel U-boat missions use
existing `recon` or `ground_attack` with `Uboat_VIIC` sea contacts/targets, that attacks
are **surfaced only**, and that submerged ASW / depth charges are out of scope.

#### Scenario: Schema mentions surfaced U-boat
- **WHEN** `get_mission_spec_schema` notes are requested for recon or ground_attack
- **THEN** notes MUST mention surfaced-only U-boat / sea_craft guidance (or a shared
  common note to that effect)
