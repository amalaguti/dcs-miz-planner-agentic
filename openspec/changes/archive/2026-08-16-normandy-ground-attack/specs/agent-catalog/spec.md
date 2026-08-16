## MODIFIED Requirements

### Requirement: Strike units carry era_id and stay Channel-tagged
After catalog sync, strike-unit rows SHALL expose `era_id` `wwii` and SHALL
keep stored combat `theatre_id` `TheChannel`. Sync MUST NOT stamp
`theatre_id` `Normandy` on those rows. `list_strike_targets(theatre="Normandy")`
MUST still return WWII **land** units (query-time offer). Sea-domain rows
MUST NOT be returned for Normandy.

#### Scenario: Strike unit era and Channel tag
- **WHEN** catalog sync runs
- **THEN** a known land strike unit (e.g. Blitz) MUST have `era_id` `wwii`
  and `theatre_id` `TheChannel`

#### Scenario: Normandy filter offers land units
- **WHEN** `list_strike_targets` is called with theatre `Normandy` after sync
- **THEN** the listing MUST include Blitz (land) and MUST NOT include
  sea_craft
