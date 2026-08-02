## ADDED Requirements

### Requirement: Compile ground-attack Mission Spec to .miz
The compiler SHALL transform a validated ground-attack Mission Spec into a DCS `.miz` that
places the player flight cold at the Spec airfield on The Channel, applies the named
registry payload (verified bomb and — when selected — slipper-tank CLSIDs on Spitfire
pylons), sets the flight main task to GroundAttack, does not restrict fuel-tank jettison
(player may jettison in cockpit), adds ingress/target waypoints at the airfield-relative
strike point, and places
the declared **enemy** ground target unit group(s) on the opposing coalition only. It MUST
NOT invent DCS identifiers, MUST NOT place targets on the player's coalition, and MUST NOT
re-enable PyDCS install payload-directory scanning. Free-flight, intercept, and CAP compile
behaviour MUST remain unchanged for those Spec types. WWII Axis ground units MUST use PyDCS
country `ThirdReich` on red when the Spec says so.

#### Scenario: Manston ground-attack example compiles
- **WHEN** the checked-in Manston ground-attack example Spec is compiled with Channel
  available in inventory
- **THEN** the system MUST write a `.miz` containing required zip members, player
  `SpitfireLFMkIX` at Manston cold parking with bomb and slipper-tank loadout CLSIDs from
  the Channel-crossing payload preset, GroundAttack tasking toward the resolved strike
  point, placed ground targets, and in-band Spitfire group frequency from the Channel
  registry

#### Scenario: Prior mission types still compile
- **WHEN** the checked-in Manston free-flight, intercept, or CAP Spec is compiled
- **THEN** the compiler MUST still produce the previously accepted behaviour for that type

### Requirement: Human acceptance for ground-attack in DCS
A compiled ground-attack example `.miz` MUST be openable in the DCS Mission Editor and
flyable as Instant Action / single mission with The Channel and Spitfire LF Mk IX available.

#### Scenario: Load ground-attack in DCS
- **WHEN** a user opens the compiled ground-attack `.miz` in DCS Mission Editor or Instant
  Action
- **THEN** the mission MUST load without editor errors and present the player strike route,
  bomb loadout, and ground targets
