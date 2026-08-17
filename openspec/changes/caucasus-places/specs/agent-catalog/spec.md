## ADDED Requirements

### Requirement: Caucasus CAP places sync into catalog
After `dcs-miz catalog sync`, `channel_place` rows `batumi_home` and
`batumi_black_sea_cap` SHALL be queryable with theatre `Caucasus`.

#### Scenario: Batumi CAP place listed
- **WHEN** catalog planning options are queried after sync
- **THEN** `batumi_black_sea_cap` MUST appear with theatre Caucasus and CAP
  meta 270° / 40 km
