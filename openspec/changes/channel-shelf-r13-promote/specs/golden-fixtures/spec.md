## ADDED Requirements

### Requirement: R13 promote examples compile
Repository SHALL include Manston GA examples exercising R13-promoted AAA and sea
units that validate and compile under Channel inventory.

#### Scenario: Flak41 and LST examples compile
- **WHEN** examples/manston_ground_attack_flak41.yaml and
  examples/manston_ground_attack_lst.yaml are validated and compiled
- **THEN** each MUST succeed and produce a .miz
