## ADDED Requirements

### Requirement: Seeded Spec-to-Spec randomization
The system SHALL provide a seeded transform that accepts a valid Mission Spec, an integer
seed, and an optional set of variation axes, and returns another Mission Spec. The same
inputs MUST always produce the same output Spec. The compiler MUST NOT perform this
randomization; it continues to compile only concrete Specs.

#### Scenario: Same seed is stable
- **WHEN** `randomize_mission_spec` is called twice with the same base Spec, seed, and axes
- **THEN** the two output Specs MUST be equal (field-for-field)

#### Scenario: Different seeds may differ
- **WHEN** the same base Spec is randomized with two different seeds and all applicable axes
- **THEN** at least one mutable field (weather, start_time, geometry, or opposition) MUST
  differ between the outputs for a base Spec that has at least one applicable axis

### Requirement: Variation axes
The system SHALL support named axes `weather`, `time`, `geometry`, and `opposition`. When
axes are omitted, all axes that apply to the mission type and Spec contents MUST run.
Axes that do not apply (for example `geometry` on free_flight, or `opposition` when
`enemies` is empty) MUST be no-ops. Unknown axis names MUST fail with a clear error.

#### Scenario: Weather axis picks a registered preset
- **WHEN** the `weather` axis runs
- **THEN** the output `weather` MUST be one of the Spec-allowed weather presets

#### Scenario: Time axis keeps HH:MM
- **WHEN** the `time` axis runs
- **THEN** the output `start_time` MUST remain a valid `HH:MM` string

#### Scenario: Geometry axis jitters present blocks only
- **WHEN** the `geometry` axis runs on a CAP Spec with a `cap` block
- **THEN** `cap.bearing_deg`, `cap.distance_km`, and `cap.altitude_m` MAY change within
  design bounds, and `cap.pattern` / `cap.engagement` MUST be unchanged

#### Scenario: Opposition axis uses registry aircraft
- **WHEN** the `opposition` axis runs on a Spec with non-empty `enemies`
- **THEN** each enemy `aircraft` id MUST remain a Channel registry aircraft id suitable
  for opposing fighters, and `count` MUST stay in 1..16

### Requirement: Identity fields preserved
Randomization MUST NOT change `schema_version`, `mission_type`, `theatre`, `date`, or any
`player` field. It MUST NOT invent unit or airfield identifiers outside the Channel
registry. It MUST NOT populate `triggers`.

#### Scenario: Free flight player placement unchanged
- **WHEN** a Manston free-flight Spec is randomized with all axes
- **THEN** `player.aircraft`, `player.airfield`, and `player.start` MUST match the base Spec

### Requirement: CLI and library entrypoints
The system SHALL expose library function `randomize_mission_spec` and a CLI subcommand
`dcs-miz randomize` that writes a YAML Spec. The CLI MUST accept `--seed` and optional
`--axes`, and MUST validate the randomized Spec with the shared validation engine before
successful write (unless an explicit skip-validate flag is provided for debugging).

#### Scenario: CLI writes a valid Spec
- **WHEN** `dcs-miz randomize` is run on a checked-in example Spec with `--seed 1` and an
  output path
- **THEN** the written YAML MUST load as a Mission Spec and MUST pass validation
