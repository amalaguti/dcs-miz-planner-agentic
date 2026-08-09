## ADDED Requirements

### Requirement: Normandy theatre in packaged registry
The packaged reference registry SHALL list Spec theatre id `Normandy` as
planner-supported alongside `TheChannel`. Data MUST use the verified DCS/PyDCS
theatre id only.

#### Scenario: Normandy is supported
- **WHEN** a caller checks theatre `Normandy`
- **THEN** the registry MUST treat it as supported

### Requirement: Needs Oar Point airfield registered
The packaged registry SHALL map curated airfield key `NeedsOarPoint` to DCS
`airdromeId` 28 (PyDCS Normandy airport Needs Oar Point).

#### Scenario: NeedsOarPoint resolves
- **WHEN** the registry is queried for airfield `NeedsOarPoint`
- **THEN** it MUST return `airdromeId` 28
