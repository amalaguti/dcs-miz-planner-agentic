## ADDED Requirements

### Requirement: Curated Falklands airfields beyond MountPleasant
The packaged `Falklands` theatre airfield table SHALL map these curated Spec
keys to DCS `airdromeId` values from PyDCS `Falklands.airport_list()` (never
invented): `MountPleasant` 2 (PyDCS name `Mount Pleasant`), `PortStanley` 1
(`Port Stanley`), `SanCarlosFOB` 3 (`San Carlos FOB`), `RioGallegos` 5
(`Rio Gallegos`), `RioGrande` 6 (`Rio Grande`), `Ushuaia` 7, `PuntaArenas` 9
(`Punta Arenas`), `SanJulian` 11 (`San Julian`). The registry MUST NOT dump
every Falklands airport. It MUST NOT invent airdrome ids 4 or 28. Lookup MUST
remain theatre-scoped (Falklands id 5 is Rio Gallegos, not Channel Manston).
Spec keys MUST be camelCase without underscores (`RioGallegos` ≠
`Rio_Gallegos`; `PortStanley` ≠ `Port_Stanley`).

#### Scenario: RioGallegos resolves on Falklands
- **WHEN** the registry is queried for airfield `RioGallegos` with theatre
  `Falklands`
- **THEN** it MUST return `airdromeId` 5

#### Scenario: RioGallegos is not Manston
- **WHEN** the registry is queried for `RioGallegos` with theatre `Falklands`
- **THEN** it MUST return `airdromeId` 5 and MUST NOT treat that id as a
  Channel airfield

### Requirement: Argentina country in modern era
The packaged modern country table SHALL include PyDCS country class
`Argentina`. WWII country tables MUST NOT include `Argentina`. Chile MUST
NOT be added in this change.

#### Scenario: Argentina is a known modern country
- **WHEN** the registry lists countries for era `modern`
- **THEN** `Argentina` MUST be present and MUST NOT appear in era `wwii`
