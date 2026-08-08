## ADDED Requirements

### Requirement: Catalog sync includes strike units
`dcs-miz catalog sync` (and `ensure_synced`) SHALL replace `catalog_strike_units`
rows from the Channel registry land + sea strike units, including `unit_id`,
`label`, `domain`, `theatre` (TheChannel), and optional class id tags derived from
packaged `strike_target_class` planning options. Compile/validate MUST continue to
use the registry as SoT.

#### Scenario: Sync includes U-boat
- **WHEN** catalog sync runs against packaged Channel data
- **THEN** `catalog_strike_units` MUST contain `Uboat_VIIC` with domain `sea`

#### Scenario: Sync includes soft truck
- **WHEN** catalog sync runs against packaged Channel data
- **THEN** `catalog_strike_units` MUST contain a known soft land unit (e.g. Blitz)
  with domain `land`
