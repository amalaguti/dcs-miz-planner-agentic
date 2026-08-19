## ADDED Requirements

### Requirement: Class shelves list R13 leftover units
Mission options SHALL list `v1_launcher` and `SK_C_28_naval_gun` on
`artillery` unit_ids, and the three leftover Coach ids on `trains` unit_ids.
French-coast place cues SHALL include noball / V-1 / coastal gun language.

#### Scenario: Artillery includes v1_launcher
- **WHEN** catalog sync loads artillery
- **THEN** unit_ids MUST include v1_launcher and SK_C_28_naval_gun

#### Scenario: Trains include tank coaches
- **WHEN** catalog sync loads trains
- **THEN** unit_ids MUST include Coach a tank yellow
