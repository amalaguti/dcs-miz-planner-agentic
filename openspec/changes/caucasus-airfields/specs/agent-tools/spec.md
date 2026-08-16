## ADDED Requirements

### Requirement: find_airfield resolves curated Caucasus keys
`find_airfield` SHALL resolve curated Caucasus Spec keys (including `Mozdok`)
when queried with theatre `Caucasus`. Lookup MUST remain theatre-scoped.

#### Scenario: Mozdok find on Caucasus
- **WHEN** `find_airfield` is called for `Mozdok` with theatre `Caucasus`
- **THEN** the result MUST include `airdromeId` 28 and MUST NOT be a
  Normandy Needs Oar Point row
