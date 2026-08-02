## ADDED Requirements

### Requirement: Planner may emit ground-attack Specs
The NL planning rules SHALL allow Mission Spec `mission_type` `ground_attack` with a nested
`strike` block (airfield-relative bearing/distance, altitude), non-empty `targets`, named
`player.payload`, and `attack_ground` objective, and MUST NOT instruct the model to invent
raw map coordinates, CLSIDs, ground unit ids, or unsupported mission types beyond the
allow-list. Planning rules MUST require strike `targets` to be the opposing coalition to the
player (no friendly fire). For Channel-crossing ground-attack, planning guidance MUST prefer
a slipper-tank payload preset and MUST remind that the tank is jettisoned by the pilot
before the attack (not via invented Lua). Ground-attack Specs MUST still pass host
validation before acceptance.

#### Scenario: Stub or documented allow-list includes ground_attack
- **WHEN** planning rules / system prompt are composed for Channel MVP planning
- **THEN** `ground_attack` MUST be listed among supported mission types alongside
  `free_flight`, `intercept`, and `cap`
