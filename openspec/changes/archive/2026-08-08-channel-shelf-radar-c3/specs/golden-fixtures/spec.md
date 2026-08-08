## ADDED Requirements

### Requirement: Radar GA example compiles
Repository SHALL include a Manston ground_attack example Spec that uses a
packaged radar unit with static (default) motion and convoy_transit, and that
example MUST validate and compile under Channel inventory.

#### Scenario: Radar example validates and compiles
- **WHEN** examples/manston_ground_attack_radar.yaml is validated and compiled
  with Channel inventory
- **THEN** validation MUST succeed and a .miz file MUST be produced
