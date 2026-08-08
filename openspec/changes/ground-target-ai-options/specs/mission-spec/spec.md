## ADDED Requirements

### Requirement: Ground targets MAY declare AI and move options
Each GA or recon `targets[]` entry MAY include optional `ai_preset` (curated name)
and/or optional `ai` object with allowlisted keys (`roe`, `alarm_state`,
`engage_air_weapons`, `restrict_targets`, `interception_range` as applicable) and
optional land `move_formation` (`off_road` | `on_road` | `rank` | `cone` | `vee` |
documented siblings). Omit means today’s defaults (`#15g` disperse rules unchanged
when motion is non-static land). Explicit fields MUST override colliding preset
keys. Unknown preset or ai keys MUST be rejected. Sea targets MUST NOT set
`move_formation` or disperse-only land fields beyond existing disperse rules
(sea still skips disperse emit).

#### Scenario: Omit ai accepted
- **WHEN** a target omits `ai_preset`, `ai`, and `move_formation`
- **THEN** the Spec MUST validate (pre-`#15h` behaviour plus existing motion rules)

#### Scenario: Convoy preset accepted
- **WHEN** a soft-vehicle land target sets a curated convoy/transit preset or
  equivalent allowlisted `ai` + `move_formation`
- **THEN** validation MUST succeed when other target rules pass

#### Scenario: Unknown ai key rejected
- **WHEN** a target sets an `ai` key outside the allowlist
- **THEN** loading or validation MUST fail naming the unknown key
