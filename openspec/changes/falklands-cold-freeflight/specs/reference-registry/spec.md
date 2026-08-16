## ADDED Requirements

### Requirement: Falklands theatre in packaged registry
The packaged registry SHALL list Spec theatre id `Falklands` as
planner-supported. Folder name under `data/theatres/` MUST match the Spec id.
Era MUST be `modern`. Data MUST use the verified DCS/PyDCS theatre id only.

#### Scenario: Falklands is supported
- **WHEN** a caller checks theatre `Falklands`
- **THEN** the registry MUST treat it as supported and MUST report era
  `modern`

### Requirement: Mount Pleasant airfield registered
The packaged registry SHALL map curated airfield key `MountPleasant` to DCS
`airdromeId` 2 (PyDCS Falklands airport Mount Pleasant) in the `Falklands`
theatre package. It MUST NOT dump every Falklands airport. The Spec key MUST
be `MountPleasant`, not `Mount_Pleasant`.

#### Scenario: MountPleasant resolves
- **WHEN** the registry is queried for airfield `MountPleasant` with theatre
  `Falklands`
- **THEN** it MUST return `airdromeId` 2

## MODIFIED Requirements

### Requirement: Modern era countries and aircraft are era-keyed
Era `modern` SHALL include PyDCS countries `Georgia`, `Turkey`, `USA`, and
`UK` and aircraft `Su-25T` with group radio 251.0 MHz. `UK` MUST remain in
the WWII era package as well. Spitfire types MUST NOT be added to modern.
`usaaf` MUST NOT be a known country.

#### Scenario: Modern smoke identity includes UK
- **WHEN** the registry lists countries for era `modern`
- **THEN** the set MUST include `Georgia`, `Turkey`, `USA`, and `UK`

#### Scenario: WWII countries still exclude modern-only hosts
- **WHEN** the registry lists countries for era `wwii`
- **THEN** the set MUST be `UK` and `ThirdReich` and MUST NOT include
  `Georgia`, `Turkey`, `USA`, or `Germany`
