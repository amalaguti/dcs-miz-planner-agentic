## ADDED Requirements

### Requirement: Late activation on combat groups
`EnemyFlight` and `GroundTarget` entries MAY set `late_activation` (boolean, default
false). When true, the compiler MUST place the group as late-activated (dormant until an
`activate_group` action references it). When false or omitted, groups MUST remain
immediately active as today.

#### Scenario: Late enemy defaults off
- **WHEN** an enemy flight omits `late_activation`
- **THEN** loading MUST treat it as false and compile MUST not mark the group late-activated

#### Scenario: Late enemy accepted
- **WHEN** an enemy flight sets `late_activation: true`
- **THEN** structural load MUST succeed when the rest of the Spec is valid
