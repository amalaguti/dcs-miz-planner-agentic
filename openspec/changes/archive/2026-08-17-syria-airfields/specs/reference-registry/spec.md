## ADDED Requirements

### Requirement: Curated Syria airfields beyond Incirlik
The packaged `Syria` theatre airfield table SHALL map these curated Spec
keys to DCS `airdromeId` values from PyDCS `Syria.airport_list()` (never
invented): `Incirlik` 16, `RamatDavid` 30 (PyDCS name `Ramat David`),
`Damascus` 7, `BeirutRaficHariri` 6 (`Beirut-Rafic Hariri`), `Aleppo` 27,
`BasselAlAssad` 21 (`Bassel Al-Assad`), `Palmyra` 28,
`KingHusseinAirCollege` 19 (`King Hussein Air College`). The registry
MUST NOT dump every Syria airport. Lookup MUST remain theatre-scoped
(Syria id 28 is Palmyra, not Caucasus Mozdok, not Normandy Needs Oar Point).

#### Scenario: Palmyra resolves on Syria
- **WHEN** the registry is queried for airfield `Palmyra` with theatre
  `Syria`
- **THEN** it MUST return `airdromeId` 28

#### Scenario: Palmyra is not Mozdok
- **WHEN** the registry is queried for `Palmyra` with theatre `Syria`
- **THEN** it MUST return `airdromeId` 28 and MUST NOT treat that id as a
  Caucasus or Normandy airfield
