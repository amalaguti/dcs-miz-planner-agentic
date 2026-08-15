## ADDED Requirements

### Requirement: Catalog countries come from era YAML
Catalog sync SHALL load known country ids from the packaged WWII era countries
table (`UK`, `ThirdReich` only). It MUST NOT invent country ids. `Germany`
MUST NOT appear as a known catalog country.

#### Scenario: Sync lists UK and ThirdReich
- **WHEN** catalog sync runs after the WWII countries package is present
- **THEN** catalog country listing MUST include `UK` and `ThirdReich` and
  MUST NOT include `Germany` as a known id

### Requirement: Strike units carry era_id and stay Channel-tagged
After catalog sync, strike-unit rows SHALL expose `era_id` `wwii` and SHALL
keep combat `theatre_id` `TheChannel` until a Normandy target batch ships.
Sync MUST NOT stamp `theatre_id` `Normandy` on those rows in this change.

#### Scenario: Strike unit era and Channel tag
- **WHEN** catalog sync runs
- **THEN** a known land strike unit (e.g. Blitz) MUST have `era_id` `wwii`
  and `theatre_id` `TheChannel`
