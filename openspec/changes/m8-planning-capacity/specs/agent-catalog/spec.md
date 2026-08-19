## MODIFIED Requirements

### Requirement: Catalog countries come from era YAML
Catalog sync SHALL load known country ids from the packaged WWII era countries
table (`UK`, `ThirdReich`, and `USA`). `Germany` MUST NOT appear as a known catalog country.

#### Scenario: Sync lists UK, ThirdReich, and USA
- **WHEN** catalog sync runs after the WWII countries package is present
- **THEN** catalog country listing MUST include `UK`, `ThirdReich`, and `USA` and
  MUST NOT include `Germany` as a known id
