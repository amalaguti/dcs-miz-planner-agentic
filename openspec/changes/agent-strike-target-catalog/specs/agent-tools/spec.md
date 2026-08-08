## ADDED Requirements

### Requirement: list_strike_targets tool
The agent tool surface SHALL expose a read-only `list_strike_targets` tool that
queries the catalog SQLite strike-units table (after sync), with optional filters
`domain` (`land`|`sea`), `class_id`, and text `q`. Results MUST include exact DCS
`unit_id`, `label`, `domain`, and class tags when present. The tool MUST NOT scan
registry YAML or PyDCS at call time.

#### Scenario: Sea filter returns U-boat
- **WHEN** `list_strike_targets` is called with `domain=sea` after sync
- **THEN** the result MUST be ok and include `Uboat_VIIC`

#### Scenario: Class filter returns AAA
- **WHEN** `list_strike_targets` is called with class `aaa_guns` after sync
- **THEN** results MUST include known AAA unit ids (e.g. flak18) and MUST NOT
  invent unknown ids
