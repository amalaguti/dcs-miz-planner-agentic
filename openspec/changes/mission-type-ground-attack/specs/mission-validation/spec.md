## ADDED Requirements

### Requirement: Validate ground-attack Specs
The shared validation engine SHALL accept ground-attack Mission Specs that satisfy
ground-attack schema rules and registry/install checks, including a valid `strike` block,
known `player.payload` for the player aircraft, known ground unit ids in `targets`, enemy
(opposing) coalition on every target, and an `attack_ground` objective. It MUST reject
unknown payloads or ground units, MUST reject same-coalition / friendly targets, MUST reject
non-empty air `enemies` on ground_attack, MUST reject `strike` / `player.payload` /
`attack_ground` on unsupported mission types, and MUST keep free-flight / intercept / CAP
validation behaviour unchanged.

#### Scenario: Valid ground-attack example passes validate
- **WHEN** the checked-in ground-attack example is validated with Channel available inventory
- **THEN** validation MUST succeed with no errors

#### Scenario: Unknown payload fails
- **WHEN** a ground-attack Spec sets `player.payload` to a name absent from the Channel
  payload registry
- **THEN** validation MUST fail with a clear error identifying the unknown payload

#### Scenario: Unknown ground unit fails
- **WHEN** a ground-attack Spec names a target unit absent from the Channel ground-unit
  registry
- **THEN** validation MUST fail with a clear error identifying the unknown unit

#### Scenario: Friendly target coalition fails
- **WHEN** a combat ground-attack Spec (`strike.practice` false/omitted) includes a target
  coalition matching `player.coalition`
- **THEN** validation MUST fail stating targets must be enemy (opposing coalition) only
  unless practice is set

#### Scenario: Practice same-coalition target passes
- **WHEN** a ground-attack Spec sets `strike.practice` true with same-coalition targets
- **THEN** validation MUST succeed for the coalition rule (subject to other checks)
