## ADDED Requirements

### Requirement: Soft-warn non-integer altitude/speed gate thresholds
Validation MUST soft-warn (MUST NOT fail solely for this reason) when a trigger uses
`unit_altitude_higher`, `unit_altitude_lower`, `unit_speed_higher`, or `unit_speed_lower`
with a non-integer `altitude_m` or `speed_kmh`, because the compiler emits integer metres
or truncated speed values. Warnings MUST use a stable code (e.g.
`gate_threshold_truncated`).

#### Scenario: Fractional altitude soft-warns
- **WHEN** a Spec uses `unit_altitude_higher` with `altitude_m: 300.7`
- **THEN** validation MUST still be ok for this reason alone and MUST include a
  truncation soft-warn

#### Scenario: Integer altitude does not warn
- **WHEN** a Spec uses `unit_altitude_higher` with `altitude_m: 300`
- **THEN** validation MUST NOT emit `gate_threshold_truncated` for that condition
