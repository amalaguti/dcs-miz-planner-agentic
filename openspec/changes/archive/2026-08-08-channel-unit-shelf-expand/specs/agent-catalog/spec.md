## ADDED Requirements

### Requirement: Catalog lists expanded strike units
After catalog sync, `list_strike_targets` / strike-unit listing SHALL return the
newly promoted Channel soft, AAA, and sea ids with correct domain and class tags.

#### Scenario: Sea filter includes HarborTug
- **WHEN** list_strike_targets is called with domain=sea after sync
- **THEN** results MUST include HarborTug
