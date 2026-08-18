## ADDED Requirements

### Requirement: Infer Falklands from curated airfield keys
When rejected Spec JSON names a curated Falklands airfield and omits a usable
theatre field, theatre inference MUST return `Falklands` (not TheChannel when
the key is `RioGallegos`). The `Mount_Pleasant` alias MUST still infer
`Falklands`. Underscore forms of the new keys (`Rio_Gallegos`,
`Port_Stanley`) MUST NOT infer a theatre. Invent MUST remain free_flight-only
at MountPleasant (UK blue).

#### Scenario: RioGallegos infers Falklands
- **WHEN** rejected JSON contains `"airfield": "RioGallegos"` without theatre
- **THEN** `infer_theatre` MUST return `Falklands`

#### Scenario: Rio_Gallegos does not infer
- **WHEN** rejected JSON contains `"airfield": "Rio_Gallegos"` without theatre
- **THEN** `infer_theatre` MUST return none
