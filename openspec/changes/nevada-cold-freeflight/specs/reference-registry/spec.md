## ADDED Requirements

### Requirement: Nevada theatre in packaged registry
The packaged registry SHALL list Spec theatre id `Nevada` as
planner-supported. Folder name under `data/theatres/` MUST match the Spec id.
Era MUST be `modern`. Data MUST use the verified DCS/PyDCS theatre id only.

#### Scenario: Nevada is supported
- **WHEN** a caller checks theatre `Nevada`
- **THEN** the registry MUST treat it as supported and MUST report era
  `modern`

### Requirement: Nellis airfield registered
The packaged registry SHALL map curated airfield key `Nellis` to DCS
`airdromeId` 4 (PyDCS Nevada airport Nellis) in the `Nevada` theatre
package. It MUST NOT dump every Nevada airport.

#### Scenario: Nellis resolves
- **WHEN** the registry is queried for airfield `Nellis` with theatre
  `Nevada`
- **THEN** it MUST return `airdromeId` 4

## MODIFIED Requirements

### Requirement: Modern era countries and aircraft are era-keyed
The packaged registry SHALL load countries and aircraft from each
`data/era/<era>/` package (`wwii` and `modern`). Era `modern` SHALL include
PyDCS countries `Georgia`, `Turkey`, and `USA` and aircraft `Su-25T` with
group radio 251.0 MHz. It MUST NOT add those ids to the WWII era package.
`usaaf` MUST NOT be a known country. `Germany` MUST NOT be a known country
in any era.

#### Scenario: WWII countries unchanged
- **WHEN** the registry lists countries for era `wwii`
- **THEN** the set MUST be `UK` and `ThirdReich` and MUST NOT include
  `Georgia`, `Turkey`, `USA`, or `Germany`

#### Scenario: Modern smoke identity includes USA
- **WHEN** the registry lists countries and aircraft for era `modern`
- **THEN** countries MUST include `Georgia`, `Turkey`, and `USA` and
  aircraft MUST include `Su-25T` at 251.0 MHz
