## ADDED Requirements

### Requirement: Curated Nevada airfields beyond Nellis
The packaged `Nevada` theatre airfield table SHALL map these curated Spec
keys to DCS `airdromeId` values from PyDCS `Nevada.airport_list()` (never
invented): `Nellis` 4, `GroomLake` 2 (PyDCS name `Groom Lake`), `Creech` 1,
`TonopahTestRange` 18 (`Tonopah Test Range`), `NorthLasVegas` 15
(`North Las Vegas`), `HendersonExecutive` 8 (`Henderson Executive`),
`BoulderCity` 6 (`Boulder City`), `Mesquite` 13. The registry MUST NOT dump
every Nevada airport. Lookup MUST remain theatre-scoped (Nevada id 2 is
Groom Lake, not Falklands Mount Pleasant, not Channel Merville Calonne).

#### Scenario: GroomLake resolves on Nevada
- **WHEN** the registry is queried for airfield `GroomLake` with theatre
  `Nevada`
- **THEN** it MUST return `airdromeId` 2

#### Scenario: GroomLake is not MountPleasant
- **WHEN** the registry is queried for `GroomLake` with theatre `Nevada`
- **THEN** it MUST return `airdromeId` 2 and MUST NOT treat that id as a
  Falklands or Channel airfield
