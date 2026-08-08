## ADDED Requirements

### Requirement: Options tool surfaces place geometry
`list_mission_options` results (via catalog sync) SHALL include the numeric
geometry fields on `channel_place` rows so invent can read recipes without
hardcoding bearings in prompts alone.

#### Scenario: Place options include bearing distance meta
- **WHEN** list_mission_options returns channel_place rows after sync
- **THEN** french coast and mid-Channel rows MUST expose strike/AOI bearing and
  distance fields in meta
