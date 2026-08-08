## ADDED Requirements

### Requirement: Troops GA example compiles
Repository SHALL include a Manston ground_attack example Spec that uses a
packaged infantry unit on path motion with convoy_transit, and that example
MUST validate and compile under Channel inventory.

#### Scenario: Troops example validates and compiles
- **WHEN** examples/manston_ground_attack_troops.yaml is validated and compiled
  with Channel inventory
- **THEN** validation MUST succeed and a .miz file MUST be produced
