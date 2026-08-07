## ADDED Requirements

### Requirement: Voice aware of player flight
Squadron-commander voice helpers SHALL accept Spec `player.flight` context so brief
phrases can refer to section size and lead/wingman role without inventing aircraft or
skill ids.

#### Scenario: Wingman phrasing available
- **WHEN** voice brief generation runs for a Spec with `role: wingman`
- **THEN** the generated copy MUST be able to state the player flies as wingman in the
  section (not as solo)
