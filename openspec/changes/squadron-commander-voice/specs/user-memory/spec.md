## ADDED Requirements

### Requirement: Squadron voice preference values
The user-memory preference key `squadron_voice` SHALL be treated as selecting a squadron
persona. Documented values are `raf`, `usaaf`, and `neutral` (aliases MAY be accepted and
normalized). Setting this preference MUST NOT wipe unrelated prefs. Planning consumers
MUST be able to read `squadron_voice` via the existing prefs tools/API.

#### Scenario: Pref stores squadron voice
- **WHEN** the user sets preference `squadron_voice` to `usaaf`
- **THEN** a subsequent prefs read MUST return `squadron_voice` as `usaaf` (or an
  equivalent normalized form) alongside any other stored prefs
