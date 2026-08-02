## ADDED Requirements

### Requirement: Supported weather planning options for new presets
Planning options SHALL list `dawn_clear` and `marginal_vfr` under the `weather` family
with support level `supported` (compile-backed), alongside existing `sunny_clear`.

#### Scenario: List mission options includes new weather
- **WHEN** `list_mission_options` (or equivalent) is invoked
- **THEN** weather options MUST include `dawn_clear` and `marginal_vfr` as `supported`
