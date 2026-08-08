## ADDED Requirements

### Requirement: Train GA example compiles
Repository SHALL include a Manston ground_attack example Spec that uses a
packaged train unit on path motion along the rail-corridor recipe with
convoy_transit, and that example MUST validate and compile under Channel
inventory.

#### Scenario: Train example validates and compiles
- **WHEN** examples/manston_ground_attack_train.yaml is validated and compiled
  with Channel inventory
- **THEN** validation MUST succeed and a .miz file MUST be produced
