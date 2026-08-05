## ADDED Requirements

### Requirement: Spec schema tool prefers immersion examples
`get_mission_spec_schema` MUST return a validated example Spec for the mission type that
prefers a packaged immersion example when one exists for that type (e.g. altitude/speed
gates for free_flight, mark/smoke for ground_attack), while remaining loadable as a
Mission Spec. Bare compile acceptance examples MAY remain separate files for goldens.

#### Scenario: Free_flight schema includes gate immersion
- **WHEN** `get_mission_spec_schema` is called with `free_flight`
- **THEN** the returned example MUST include altitude and/or speed gate trigger conditions
  (or equivalent packaged gates example content)

### Requirement: Invent tool surface omits randomize_mission
The default agent invent tool list MUST NOT include `randomize_mission`. Seeded rerolls
remain available via host CLI. Planning prompts MUST NOT instruct the model to call
`randomize_mission` during vague first invent.

#### Scenario: Default tools exclude randomize
- **WHEN** the default planning tool definitions are listed
- **THEN** `randomize_mission` MUST NOT appear
