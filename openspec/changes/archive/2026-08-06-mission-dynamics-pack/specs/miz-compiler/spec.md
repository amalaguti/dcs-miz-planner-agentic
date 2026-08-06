## ADDED Requirements

### Requirement: Compiler expands dynamics before .miz emit
The PyDCS compiler path MUST run the same dynamics expansion used by validation so the
saved `.miz` contains the expanded native trigger tables (dice and/or radio + activate),
not an unexpanded `dynamics` declaration alone.

#### Scenario: Live dynamics example compiles with Set Flag Random
- **WHEN** a packaged live-dynamics example Spec is compiled
- **THEN** the mission member MUST include Set Flag Random (or equivalent PyDCS emit)
  and activate-group actions for pool branches
