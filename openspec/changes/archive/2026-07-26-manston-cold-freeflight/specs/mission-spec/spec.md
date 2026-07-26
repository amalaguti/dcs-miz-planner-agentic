## ADDED Requirements

### Requirement: Free-flight Mission Spec schema
The system SHALL define a Mission Spec for free-flight missions that includes theatre, date, start time, weather preset, and a single player aircraft placement.

#### Scenario: Manston cold free-flight example is representable
- **WHEN** an author provides a free-flight Mission Spec for Channel with player `SpitfireLFMkIX`, airfield `Manston`, start type cold parking, start time 09:00, and weather preset `sunny_clear`
- **THEN** the Mission Spec SHALL be accepted as structurally valid for compilation

### Requirement: Exact DCS identifiers in the Mission Spec
The Mission Spec SHALL use verified DCS identifiers for theatre and aircraft type and SHALL NOT invent alternate spellings.

#### Scenario: Theatre and aircraft ids
- **WHEN** a free-flight Mission Spec targets The Channel and Spitfire LF Mk IX
- **THEN** theatre MUST be `TheChannel` and player aircraft type MUST be `SpitfireLFMkIX`

### Requirement: Airfield referenced by name in the Mission Spec
The Mission Spec SHALL allow the player departure airfield to be specified by display name (e.g. `Manston`), with mapping to DCS `airdromeId` performed by the compiler layer.

#### Scenario: Manston by name
- **WHEN** the Mission Spec sets player airfield to `Manston`
- **THEN** the compiled mission MUST place the player at Manston (`airdromeId` 5)

### Requirement: Checked-in example Mission Spec
The repository SHALL include a checked-in example Mission Spec that encodes the Manston cold free-flight acceptance mission.

#### Scenario: Example file present
- **WHEN** a developer clones the repository
- **THEN** an example Mission Spec for Manston cold free flight MUST be present and usable as compile input
