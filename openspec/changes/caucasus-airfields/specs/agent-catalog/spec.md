## MODIFIED Requirements

### Requirement: Catalog lists Caucasus and Batumi
After catalog sync from the packaged registry, known theatres MUST include
`Caucasus` and known airfields MUST include `Batumi` with `airdromeId` 22
and theatre `Caucasus`. Known airfields MUST also include the other curated
Caucasus keys (`Kobuleti`, `SenakiKolkhi`, `Kutaisi`, `TbilisiLochini`,
`Vaziani`, `SochiAdler`, `Mozdok`). Known countries for era `modern` MUST
include `Russia`.

#### Scenario: Sync populates Batumi
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain theatre `Caucasus` and airfield `Batumi`
  with `airdromeId` 22

#### Scenario: Sync populates Mozdok and Russia
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain airfield `Mozdok` with `airdromeId` 28
  and theatre `Caucasus`, and country `Russia`
