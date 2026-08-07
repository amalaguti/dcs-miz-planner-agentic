## ADDED Requirements

### Requirement: Recon mission type
The Mission Spec SHALL support `mission_type` value `recon` in addition to `free_flight`,
`intercept`, `cap`, `ground_attack`, and `escort`. A recon Spec MUST include a nested
`recon` object (airfield-relative AOI and altitude), a non-empty `objectives` list including
`recon_area`, and MUST omit `player.payload`, `strike`, `cap`, and `escort`. Air `enemies`
MUST be empty. Optional `targets` MAY list enemy visual contacts. Existing mission types
MUST remain unchanged. The `recon` block MUST be forbidden on non-recon types.

#### Scenario: Manston recon Spec accepted
- **WHEN** a Mission Spec sets `mission_type` to `recon`, player `SpitfireLFMkIX` at
  Manston, a valid `recon` block, empty `enemies`, no payload, and a `recon_area` objective
- **THEN** the Spec MUST load as structurally valid for recon compilation

#### Scenario: Recon block forbidden on free flight
- **WHEN** a Mission Spec sets `mission_type` to `free_flight` and includes a `recon` object
- **THEN** loading or validation MUST fail with a clear error

#### Scenario: Payload forbidden on recon
- **WHEN** a recon Spec sets `player.payload`
- **THEN** loading or validation MUST fail stating payload is not supported for recon

### Requirement: Recon AOI is airfield-relative
The `recon` block SHALL express the AOI centre as `bearing_deg` (0–360) and a positive
`distance_km` relative to the player departure airfield, plus a positive `altitude_m` for
ingress/observe. It MUST include a positive `radius_m` for the AOI zone (or apply a
documented default). The Spec MUST NOT require raw Channel map x/y or invented WGS84
coordinates.

#### Scenario: Bearing and distance required
- **WHEN** a recon Spec omits `bearing_deg` or `distance_km`, or sets a non-positive
  distance, altitude, or radius
- **THEN** loading MUST fail with a structural validation error identifying the `recon`
  fields

### Requirement: Optional visual contacts
A recon Spec MAY declare an empty or non-empty `targets` list. When non-empty, each entry
MUST use a known Channel strike-unit id (land or sea), positive count, and opposing
coalition relative to `player.coalition`. Air `enemies` MUST remain empty. Contacts are
observe-only — Spec MUST NOT treat them as strike/destroy objectives.

#### Scenario: Area recon with empty targets
- **WHEN** a recon Spec omits targets or sets `targets: []`
- **THEN** the Spec MUST load as structurally valid (area recon)

#### Scenario: Enemy truck contacts accepted
- **WHEN** a recon Spec lists known Channel ground unit ids with opposing coalition and
  empty `enemies`
- **THEN** the Spec MUST load as structurally valid for compilation

#### Scenario: Same-coalition contact rejected
- **WHEN** a recon Spec includes a target whose coalition equals `player.coalition`
- **THEN** loading or validation MUST fail (contacts must be opposing coalition)

#### Scenario: Non-empty air enemies refused for recon
- **WHEN** a recon Spec sets a non-empty `enemies` list
- **THEN** loading or validation MUST fail stating air enemies are not supported for recon
  in this schema version

### Requirement: Recon objective
A recon Spec MUST declare a non-empty `objectives` list that includes `recon_area`.
Unsupported objective types for recon (including `attack_ground`) MUST be rejected.

#### Scenario: recon_area required
- **WHEN** a recon Spec has empty objectives or only non-`recon_area` objective types
- **THEN** loading or validation MUST fail requiring `recon_area`

#### Scenario: attack_ground rejected on recon
- **WHEN** a recon Spec includes an `attack_ground` objective
- **THEN** loading or validation MUST fail
