## ADDED Requirements

### Requirement: Land path place recipe for invent
Packaged `french_coast_strike_belt` (or equivalent inland place) SHALL expose
`path_point_deltas` suitable for inventing soft-vehicle path motion near the
strike, and place description/notes MUST state that invent SHOULD prefer 2–3
path points derived from strike + those deltas (not mid-Channel distances).

#### Scenario: Inland place exposes path deltas
- **WHEN** catalog sync loads french_coast_strike_belt
- **THEN** meta MUST include path_point_deltas with at least two entries usable
  relative to strike bearing/distance

### Requirement: Harbour place binds sea class
`coastal_harbour` place meta/description SHALL state that harbour/dock invent
MUST use `sea_craft` / sea-domain units only (via strike catalog), with static
motion and harbour_static, and MUST NOT use soft land vehicles.

#### Scenario: Coastal harbour notes sea-only units
- **WHEN** channel_place coastal_harbour is listed after sync
- **THEN** description or meta MUST require sea_craft / sea domain units for
  harbour invent
