## ADDED Requirements

### Requirement: Channel aircraft failure catalog
The Channel reference data SHALL include a curated catalog of DCS failure ids for
supported player aircraft (at least `SpitfireLFMkIX` in v1), exposed via the registry
API for validation and agent listing. Catalog entries MUST use exact DCS ids from
verified Spitfire mission/ME sources.

#### Scenario: Spitfire magneto id known
- **WHEN** a client queries known failures for `SpitfireLFMkIX`
- **THEN** the catalog MUST include `ENG0_MAGNETO0` (and other curated v1 ids)
