## ADDED Requirements

### Requirement: Validate target AI options by domain and class
Validation MUST expand presets, then enforce allowlists by registry domain and
unit class heuristic (soft land vs AAA land vs sea per R12). Soft land MUST
reject interception_range and ARM-style keys if exposed. Sea MUST reject
`move_formation`, restrict_targets, and disperse-oriented fields that are
land-only (except existing `disperse_under_fire_s` already ignored/skipped for
sea emit). AAA land MAY accept interception_range. Errors MUST name field path
and reason (class/domain mismatch).

#### Scenario: Soft truck interception rejected
- **WHEN** a soft-vehicle land target sets `ai.interception_range` (or equivalent)
- **THEN** validation MUST fail with a class/domain allowlist error

#### Scenario: Sea move_formation rejected
- **WHEN** a sea-domain target sets `move_formation`
- **THEN** validation MUST fail

#### Scenario: Flak interception accepted
- **WHEN** an AAA land unit sets allowlisted interception range with valid ROE/alarm
- **THEN** validation MUST succeed when other rules pass
