## ADDED Requirements

### Requirement: Ground targets MAY declare motion
Each `targets[]` entry MAY include optional motion. Omit or `motion: static` MUST
mean a single placement (current behaviour). `motion: patrol` MUST include
`patrol_radius_m` within an allowed range. `motion: path` MUST include a list of
2–6 airfield-relative `{bearing_deg, distance_km}` waypoints (loop implied).
`patrol` and `path` MUST NOT be combined on the same target. Unknown motion values
MUST be rejected. Moving targets MAY set optional `speed_kmh` (clamped to a curated
unit speed band) and optional `disperse_under_fire_s` (land only; omit = default
disperse duration for moving land, `0` disables).

#### Scenario: Static omit accepted
- **WHEN** a GA or recon Spec lists targets without a motion field
- **THEN** the Spec MUST validate (identical to pre-motion behaviour)

#### Scenario: Patrol shape accepted
- **WHEN** a target has `motion: patrol` and a valid `patrol_radius_m`
- **THEN** validation MUST succeed when other target rules pass

#### Scenario: Path shape accepted
- **WHEN** a target has `motion: path` with 2–6 airfield-relative points
- **THEN** validation MUST succeed when other target rules pass
