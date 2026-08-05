## ADDED Requirements

### Requirement: Triggers may use player altitude and speed gates
When a Mission Spec includes a trigger condition `unit_altitude_higher` or
`unit_altitude_lower`, it MUST provide `altitude_m` (> 0) and MAY set `agl` (default
true). When it includes `unit_speed_higher` or `unit_speed_lower`, it MUST provide
`speed_kmh` (> 0). These conditions MUST refer to the player aircraft only. The Spec MUST
NOT carry raw DCS unit ids or free-form Lua for these conditions.

#### Scenario: Altitude gate fields
- **WHEN** a Spec declares `type: unit_altitude_higher` with `altitude_m` and optional
  `agl`
- **THEN** loading MUST succeed when the rest of the Spec is valid

#### Scenario: Speed gate fields
- **WHEN** a Spec declares `type: unit_speed_lower` with `speed_kmh`
- **THEN** loading MUST succeed when the rest of the Spec is valid
