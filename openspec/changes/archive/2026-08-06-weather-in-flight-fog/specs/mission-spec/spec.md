## ADDED Requirements

### Requirement: Fog dynamics Spec declares burn-off or roll-in
The Mission Spec MAY include optional `fog_dynamics` with `mode` one of
`burn_off` or `roll_in`, `start_after_s` and `duration_s` (non-negative), and
optional end fog numerics. The Spec MUST NOT carry free-form Lua. Omitted
`fog_dynamics` MUST preserve prior behaviour.

#### Scenario: Burn-off Spec loads
- **WHEN** a Spec sets `fog_dynamics.mode: burn_off` with valid timings
- **THEN** structural load MUST succeed

#### Scenario: Free-form script rejected
- **WHEN** a Spec includes an undeclared script or Lua field for fog
- **THEN** loading MUST fail (unknown field / forbid)
