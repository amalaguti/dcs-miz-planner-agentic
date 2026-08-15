## ADDED Requirements

### Requirement: Curated Normandy airfields beyond Needs Oar Point
The packaged `Normandy` theatre airfield table SHALL map these curated Spec
keys to DCS `airdromeId` values from PyDCS `Normandy.airport_list()` (never
invented): `NeedsOarPoint` 28, `Chailey` 27, `Funtington` 29, `Tangmere` 30,
`FordAF` 31 (PyDCS name `Ford_AF`), `Maupertus` 4, `SaintPierreduMont` 1,
`Carpiquet` 19. The registry MUST NOT dump every Normandy airport. Lookup MUST
remain theatre-scoped (Normandy id 4 is Maupertus, not Channel Abbeville).

#### Scenario: FordAF resolves on Normandy
- **WHEN** the registry is queried for airfield `FordAF` with theatre
  `Normandy`
- **THEN** it MUST return `airdromeId` 31

#### Scenario: Maupertus is not Channel Abbeville
- **WHEN** the registry is queried for `Maupertus` with theatre `Normandy`
- **THEN** it MUST return `airdromeId` 4 and MUST NOT treat that id as a
  TheChannel airfield
