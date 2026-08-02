## ADDED Requirements

### Requirement: Seeded reroll planning option
The packaged Channel planning options SHALL include a `randomization` family entry that
describes seeded Spec rerolls (tool/CLI), with support level at least `advisory` once the
randomize tool exists. The entry MUST NOT claim a Mission Spec field mapping for the seed
itself (seed remains a transform argument).

#### Scenario: List options includes randomization
- **WHEN** `list_mission_options` is called after catalog sync
- **THEN** the result MUST include a planning option with family `randomization`
