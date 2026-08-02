## ADDED Requirements

### Requirement: Ground-attack mission type
The Mission Spec SHALL support `mission_type` value `ground_attack` in addition to
`free_flight`, `intercept`, and `cap`. A ground-attack Spec MUST include a nested `strike`
object (airfield-relative target area and altitude), a non-empty `targets` list of ground
units, a named `player.payload` preset, and a non-empty `objectives` list including
`attack_ground`. Air `enemies` MUST be empty. Free-flight, intercept, and CAP rules MUST
remain unchanged. The `strike` block MUST be forbidden on non–ground_attack types.

#### Scenario: Manston ground-attack Spec accepted
- **WHEN** a Mission Spec sets `mission_type` to `ground_attack`, player `SpitfireLFMkIX` at
  Manston with a known payload preset, a valid `strike` block, non-empty `targets`, and an
  `attack_ground` objective
- **THEN** the Spec MUST load as structurally valid for ground-attack compilation

#### Scenario: Strike block forbidden on free flight
- **WHEN** a Mission Spec sets `mission_type` to `free_flight` and includes a `strike` object
- **THEN** loading or validation MUST fail with a clear error

### Requirement: Strike target area is airfield-relative
The `strike` block SHALL express the target area as `bearing_deg` (0–360) and a positive
`distance_km` relative to the player departure airfield, plus a positive `altitude_m` for
ingress. The Spec MUST NOT require raw Channel map x/y or invented WGS84 coordinates.

#### Scenario: Bearing and distance required
- **WHEN** a ground-attack Spec omits `bearing_deg` or `distance_km`, or sets a non-positive
  distance or altitude
- **THEN** loading MUST fail with a structural validation error identifying the `strike` fields

### Requirement: Ground targets collection
A ground-attack Mission Spec MUST declare a non-empty `targets` list. Each target entry MUST
include an exact DCS land-vehicle or ship type id and a positive count. Unknown unit ids MUST
be rejected by validation against the Channel strike-target registry (land + sea). Air
`enemies` MUST remain empty for ground_attack. Land vehicles are for enemy-held territory;
over-water placements MUST use sea-domain ship ids.

#### Scenario: Soft truck targets accepted
- **WHEN** a ground-attack Spec lists known Channel ground unit ids with valid counts and
  empty `enemies`
- **THEN** the Spec MUST load as structurally valid for compilation

#### Scenario: Unknown ground unit rejected
- **WHEN** a ground-attack Spec names a ground unit absent from the Channel registry
- **THEN** validation MUST fail identifying the unknown unit

#### Scenario: Non-empty air enemies refused for ground attack
- **WHEN** a ground-attack Spec sets a non-empty `enemies` list
- **THEN** loading or validation MUST fail stating air enemies are not supported for
  ground_attack in this schema version

### Requirement: Enemy-only strike targets
Every ground-attack `targets` entry MUST belong to the coalition opposing `player.coalition`
(no same-side / friendly targets) **unless** `strike.practice` is true (bombing-practice /
training narrative). When `practice` is false or omitted, validation MUST reject any target
whose coalition matches the player. When `practice` is true, same-coalition targets MUST be
accepted (e.g. UK-side range targets for a blue player). The compiler MUST place target
groups on the coalition declared in each target entry.

#### Scenario: Blue player with red targets accepted
- **WHEN** a ground-attack Spec has `player.coalition` `blue` and all `targets` use coalition
  `red`
- **THEN** the Spec MUST load as structurally valid (subject to other ground-attack rules)

#### Scenario: Friendly / same-coalition target rejected in combat
- **WHEN** a ground-attack Spec has `strike.practice` false or omitted and includes a target
  whose coalition equals `player.coalition`
- **THEN** loading or validation MUST fail with a clear error that strike targets must be
  enemy (opposing coalition) only unless practice is set

#### Scenario: Practice strike allows same-coalition targets
- **WHEN** a ground-attack Spec sets `strike.practice` true and includes same-coalition
  targets (e.g. blue player, blue UK-side trucks)
- **THEN** the Spec MUST load as structurally valid (subject to other ground-attack rules)

### Requirement: Named player payload preset
A ground-attack Spec MUST set `player.payload` to a named Channel payload preset that is
valid for the player aircraft. Unknown presets or presets for a different aircraft MUST be
rejected. Free-flight, intercept, and CAP Specs MUST omit `player.payload` (or treat it as
unsupported) for this schema version. Packaged presets MUST include at least one
Channel-crossing Spitfire loadout that combines wing bombs with the verified 45 gal slipper
tank CLSID (centreline tank and centreline 500 lb bomb are mutually exclusive on the same
pylon).

#### Scenario: spitfire_2x250_slipper accepted
- **WHEN** a ground-attack Spec sets `player.payload` to a registered SpitfireLFMkIX preset
  that includes wing bomb CLSIDs and the slipper-tank CLSID
- **THEN** the Spec MUST be structurally valid (subject to other ground-attack rules)

#### Scenario: spitfire bomb-only preset accepted
- **WHEN** a ground-attack Spec sets `player.payload` to a registered SpitfireLFMkIX bomb
  preset without a tank
- **THEN** the Spec MUST be structurally valid (subject to other ground-attack rules)

#### Scenario: Unknown payload rejected
- **WHEN** a ground-attack Spec sets `player.payload` to an undeclared name
- **THEN** validation MUST fail identifying the unknown payload

### Requirement: Ground-attack objective
A ground-attack Mission Spec MUST declare a non-empty `objectives` list including objective
type `attack_ground`. Non-empty `triggers` MUST still be rejected. Objective type
`attack_ground` MUST be rejected on non–ground_attack mission types unless a later change
explicitly allows it.

#### Scenario: attack_ground objective accepted
- **WHEN** a ground-attack Spec includes `attack_ground` and empty `triggers`
- **THEN** validation MUST accept the Spec (subject to other ground-attack and registry rules)

#### Scenario: Non-empty triggers still refused
- **WHEN** a ground-attack Spec sets a non-empty `triggers` list
- **THEN** validation MUST fail stating triggers are not supported yet

### Requirement: Checked-in ground-attack example Spec
The repository SHALL include a checked-in example Mission Spec for a Manston Channel
ground-attack (Spitfire with bomb preset, airfield-relative strike, ground targets) usable as
validate and compile input under schema_version `"1"`.

#### Scenario: Example present
- **WHEN** a developer clones the repository
- **THEN** a ground-attack example Spec MUST be present and loadable under schema_version `"1"`

## MODIFIED Requirements

### Requirement: Reserved extension points for future combat and triggers
The Mission Spec MAY include optional top-level keys `enemies`, `objectives`, `triggers`,
and `targets`. For free-flight missions those combat keys MUST be absent or empty. For
intercept missions, `enemies` and `objectives` MUST be non-empty per intercept rules. For CAP
missions, `objectives` MUST be non-empty per CAP rules and `enemies` MAY be empty or
non-empty; CAP Specs MUST also include the nested `cap` block. For ground-attack missions,
`targets` and `objectives` MUST be non-empty per ground-attack rules, `enemies` MUST be
empty, and the nested `strike` block MUST be present. `triggers` MUST remain empty until a
later change implements the trigger model. The system MUST NOT silently drop unsupported
non-empty values.

#### Scenario: Free flight with absent extensions compiles
- **WHEN** a free-flight Mission Spec omits `enemies`, `objectives`, `triggers`, and
  `targets`
- **THEN** the Spec SHALL be structurally valid and the compiler MUST proceed as for free
  flight

#### Scenario: Free flight refuses non-empty enemies
- **WHEN** a free-flight Mission Spec sets `enemies` to a non-empty value
- **THEN** the system MUST refuse load or validation with a clear error that free_flight
  requires empty combat extensions
