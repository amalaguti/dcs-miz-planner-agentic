## MODIFIED Requirements

### Requirement: Planner consults behaviour and inspiration options assertively
Planning and interactive chat system guidance MUST instruct the agent to call
`list_mission_options` and consider `mission_inspiration` and `mission_behaviour` rows
when the user leaves challenge/immersion details unspecified. The agent SHOULD pick an
inspiration pattern that fits the mission type, map it to supported behaviour recipes, and
emit typically one or two behaviours as valid Spec fields—unless the user forbids extras
or supplies conflicting hand-written triggers. Guidance MUST also direct the agent to call
`research_guidance` when tactics, procedures, historical colour, **or external mission
examples** would help, and to consult the **local installed campaign index**—including
campaign names, `.miz` filenames, `.cmp` short text when present, and **`Doc/` PDF
filenames/titles** (not extracted briefing body text)—when local DCS campaigns can inspire
structure or naming—while treating research notes, `.cmp` playlists, Doc filenames, and
campaign listings as non-authoritative for Spec fields. The agent MUST NOT invent Lua or
unsupported Spec types, MUST NOT download or emit third-party `.miz` as Spec, MUST NOT
force narrative packs when zones/triggers are already non-empty, and MUST NOT use
`randomize_mission` as a substitute for choosing behaviour recipes on a fresh vague ask.

#### Scenario: Prompt guidance mentions assertive creative selection
- **WHEN** the planning or chat system prompt is built
- **THEN** it MUST include guidance to consult `mission_inspiration` and
  `mission_behaviour` options (and research / local campaigns when inventing) and apply
  fitting supported behaviours when the user is vague about immersion/challenge

#### Scenario: Conflicts with hand triggers avoided
- **WHEN** guidance describes narrative or behaviour packs
- **THEN** it MUST retain the rule that narrative expansion conflicts with non-empty
  hand-authored zones/triggers

#### Scenario: Campaign Doc guidance is filename-honest
- **WHEN** the planning or chat system prompt mentions local campaigns or `Doc/`
- **THEN** it MUST refer to Doc PDF filenames/titles (or equivalent listing) and MUST NOT
  instruct the agent to prefer extracted Doc briefing themes or PDF body text

#### Scenario: Randomize not used as authoring
- **WHEN** the planning or chat system prompt describes `randomize_mission`
- **THEN** it MUST state that randomize is for rerolling an accepted Spec, not for inventing
  immersion on a vague first ask

## ADDED Requirements

### Requirement: Spec shape reminder allows immersion triggers
The always-on Spec shape reminder injected into planning prompts MUST NOT require
`triggers` to be an empty list. It MUST state that `triggers` (and `zones` when needed)
may be populated for supported immersion behaviours, and that `[]` is used when unused.

#### Scenario: Reminder does not force empty triggers
- **WHEN** the Spec shape reminder text is composed into the system prompt
- **THEN** it MUST NOT contain the phrase that triggers must be empty, and MUST allow
  non-empty triggers for behaviours
