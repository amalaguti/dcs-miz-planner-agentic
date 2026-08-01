# User Memory

## Purpose

Local user preferences, mission-generation history, and satisfaction feedback in the
same SQLite file as install inventory and the agent catalog — distinct table namespaces
so catalog sync never wipes user data.

## Requirements

### Requirement: User memory lives in local SQLite
The system SHALL persist user preferences, generation history, and satisfaction feedback
in the same local SQLite database file used for install inventory and the agent catalog,
under tables that are distinct from `catalog_*` and install theatre tables. Catalog sync
MUST NOT delete or replace user-memory tables.

#### Scenario: Catalog sync preserves prefs
- **WHEN** user preferences exist in the database and `catalog sync` runs
- **THEN** those preferences MUST still be readable afterward

#### Scenario: Shared database path
- **WHEN** the memory store opens without an explicit path override
- **THEN** it MUST use the same default inventory database path as install/catalog

### Requirement: Preference key-value storage
The system SHALL store preferences as string keys mapped to JSON values with an updated
timestamp. Reading prefs MUST return the stored map (empty when none are set). Writing
prefs MUST upsert the provided keys without requiring a full replace of all keys.

#### Scenario: Round-trip preferred airfield
- **WHEN** a preference key such as preferred airfield is set and then read
- **THEN** the stored value MUST match what was written

#### Scenario: Partial upsert
- **WHEN** one preference key is updated while others already exist
- **THEN** the other keys MUST remain unchanged

### Requirement: Generation history recording
The system SHALL append generation history rows that include at least a creation timestamp,
Spec path (when written), outcome, and optional prompt / theatre / mission type / detail
JSON. Outcomes MUST distinguish success from validation or compile failure when those
paths apply.

#### Scenario: Successful plan is recorded
- **WHEN** a generation completes successfully with a written Spec path
- **THEN** a history row MUST exist with a success outcome and that Spec path

#### Scenario: Failed validation can be recorded
- **WHEN** a generation ends in validation failure and is recorded
- **THEN** the history row MUST use a non-success outcome suitable for validation failure

### Requirement: Satisfaction feedback
The system SHALL accept satisfaction feedback with an optional link to a generation history
id, an optional numeric score, an optional note, and a source label (for example post_gen
or cli). Feedback MUST persist for later readback.

#### Scenario: Feedback linked to generation
- **WHEN** feedback is recorded with a known generation id and a score
- **THEN** that feedback MUST be stored and retrievable with the generation id and score

### Requirement: User schema versioning
The system SHALL track a user-memory schema version separate from catalog and install
schema versions. A user schema mismatch MUST NOT wipe `catalog_*` or install theatre data.

#### Scenario: User schema bump leaves catalog intact
- **WHEN** the user-memory schema version changes and the store reconnects
- **THEN** catalog tables MUST remain present if they were already populated
