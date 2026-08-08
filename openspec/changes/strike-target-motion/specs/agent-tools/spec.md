## ADDED Requirements

### Requirement: Schema documents target motion
Derived Spec schema notes SHALL document optional `targets[].motion`
(`static` | `patrol` | `path`), required companion fields, and heuristics
(sea/soft vehicles move; harbour/AAA static).

#### Scenario: Schema mentions motion
- **WHEN** `get_mission_spec_schema` notes are requested for ground_attack or recon
- **THEN** notes MUST mention optional target motion fields
