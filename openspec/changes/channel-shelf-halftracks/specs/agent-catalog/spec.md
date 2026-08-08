## ADDED Requirements

### Requirement: Catalog lists halftracks_apc strike units
After catalog sync, `list_strike_targets` with class_id `halftracks_apc` SHALL
return the promoted Channel halftrack unit ids.

#### Scenario: Filter by halftracks_apc
- **WHEN** list_strike_targets is called with class_id halftracks_apc
- **THEN** the result MUST include Sd_Kfz_251 among unit_ids
