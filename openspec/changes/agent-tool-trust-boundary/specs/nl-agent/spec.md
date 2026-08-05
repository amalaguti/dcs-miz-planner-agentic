## ADDED Requirements

### Requirement: Prompt states mutate/compile are host-owned
Planning system guidance MUST state that compiling `.miz` files, writing user prefs, and
recording generations/feedback are host/CLI responsibilities — not agent tool calls on the
default planning surface.

#### Scenario: Prompt mentions host-owned compile/prefs
- **WHEN** the planning system prompt is built
- **THEN** it MUST indicate that compile / preference writes / feedback recording are
  outside the default agent tool surface (host or CLI)
