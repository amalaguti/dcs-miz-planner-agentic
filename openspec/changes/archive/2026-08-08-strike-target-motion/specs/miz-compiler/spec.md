## ADDED Requirements

### Requirement: Compiler emits native waypoints for target motion
For each non-static `targets[]` entry, the compiler MUST add native ME route
waypoints on the placed ship or vehicle group (PyDCS `add_waypoint` or equivalent).
`patrol` MUST produce a looping route around the AOI/strike placement within
`patrol_radius_m`. `path` MUST place the group along the Spec waypoints and loop.
Static/omit MUST NOT add motion waypoints. Free-form Lua MUST NOT be required.
Player GroundAttack Bombing MAY remain aimed at the fixed strike point in v1.
Cruise speeds MUST come from curated bands (seeded pick or Spec `speed_kmh`).
Moving land groups MUST receive Disperse Under Fire (ME option) by default unless
disabled via Spec.

#### Scenario: U-boat patrol compiles with ship waypoints
- **WHEN** a mid-Channel Spec with `Uboat_VIIC` and `motion: patrol` is compiled
- **THEN** the `.miz` MUST contain `Uboat_VIIC` and multiple route points for that group

#### Scenario: Truck path compiles with vehicle waypoints
- **WHEN** a land GA Spec with soft-vehicle `motion: path` is compiled
- **THEN** the `.miz` MUST contain that vehicle type and multiple route points

#### Scenario: Moving land convoy gets Disperse Under Fire
- **WHEN** a soft-vehicle path Spec is compiled without disabling disperse
- **THEN** the `.miz` MUST include Disperse Under Fire / option id 8 on the group route

#### Scenario: Static target unchanged
- **WHEN** a Spec target omits motion
- **THEN** the group MUST be placed without a multi-point motion route (same as today)
