## MODIFIED Requirements

### Requirement: List mission options tool
The system SHALL expose `list_mission_options` that returns known planning enumerations from
the catalog (at least mission types, start types, weather presets) and offerable theatres
from the catalog/install join, **and** an enriched planning-options collection with family,
id, description, and support level (`supported` | `advisory` | `future`).

#### Scenario: Options include free flight and intercept
- **WHEN** `list_mission_options` is called after catalog sync
- **THEN** the result MUST include mission types `free_flight` and `intercept`

#### Scenario: Offerable theatres reflected
- **WHEN** TheChannel is offerable on the local machine
- **THEN** `list_mission_options` MUST list TheChannel among offerable theatres

#### Scenario: Enriched planning options present
- **WHEN** `list_mission_options` is called after catalog sync
- **THEN** the result MUST include planning option rows with support levels for agent use
