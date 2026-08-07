## ADDED Requirements

### Requirement: Compile recon missions
The compiler SHALL compile a validated `mission_type: recon` Spec into a Channel `.miz`
with player `SpitfireLFMkIX` cold at the declared airfield, group task
`Reconnaissance`, ingress toward the airfield-relative AOI, an AOI trigger zone sized from
`recon.radius_m`, weapons-hold (or equivalent observe) ROE, and no bomb/payload CLSIDs.
When `targets` is non-empty, the compiler MUST place contact groups near the AOI without
GroundAttack/Bombing/AttackGroup tasking. The compiler MUST emit a native find beat:
player-coalition `coalition_in_zone` on the AOI → message instructing observe complete /
RTB (and MAY set a reserved flag). Free-form Lua MUST NOT be used.

#### Scenario: Manston recon compiles
- **WHEN** `examples/manston_recon.yaml` (or equivalent) is compiled
- **THEN** the `.miz` MUST include Reconnaissance tasking, an AOI zone, no bomb CLSIDs, and
  a find-zone message (or equivalent trigger comment/text)

#### Scenario: Contacts placed without attack tasking
- **WHEN** a recon Spec includes opposing-coalition truck contacts
- **THEN** the `.miz` MUST contain those unit types near the AOI and MUST NOT attach
  GroundAttack or Bombing attack tasks for the player strike path
