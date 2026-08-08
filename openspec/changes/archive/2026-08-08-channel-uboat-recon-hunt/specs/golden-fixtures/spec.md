## ADDED Requirements

### Requirement: Surfaced U-boat recon example
The repository SHALL include a checked-in Channel `mission_type: recon` Spec that places
one or more opposing-coalition `Uboat_VIIC` contacts near a mid-Channel water AOI
(airfield-relative geometry that validates as sea domain), with no `player.payload`, and
a `recon_area` objective. The compiled `.miz` MUST include Reconnaissance tasking, the
recon AOI find beat, and ship-group contact(s) of type `Uboat_VIIC` without Bombing
tasking.

#### Scenario: U-boat recon Spec validates and compiles
- **WHEN** the checked-in U-boat recon example is validated and compiled
- **THEN** validation MUST succeed and the `.miz` MUST contain `Uboat_VIIC` and
  Reconnaissance / AOI find wiring without bomb CLSIDs

### Requirement: Surfaced U-boat hunt (GA) example
The repository SHALL include a checked-in Channel `mission_type: ground_attack` Spec that
targets one or more opposing-coalition `Uboat_VIIC` units on mid-Channel (or other
validated sea) geometry with a named Spitfire bomb payload and `attack_ground` objective.
The compiled `.miz` MUST include GroundAttack / bomb loadout and `Uboat_VIIC` ship group(s).

#### Scenario: U-boat hunt Spec validates and compiles
- **WHEN** the checked-in U-boat hunt example is validated and compiled
- **THEN** validation MUST succeed and the `.miz` MUST contain `Uboat_VIIC` and bomb
  CLSID(s)
