## ADDED Requirements

### Requirement: Catalog lists extra Nevada airfields
After catalog sync from the packaged registry, known airfields MUST include
`GroomLake` with `airdromeId` 2 and theatre `Nevada` (and the other curated
Nevada keys besides `Nellis`).

#### Scenario: GroomLake is a known Nevada airfield
- **WHEN** catalog sync runs after the Nevada Stage B airfield table is present
- **THEN** airfield listing MUST include `GroomLake` with theatre `Nevada`
  and `airdromeId` 2
