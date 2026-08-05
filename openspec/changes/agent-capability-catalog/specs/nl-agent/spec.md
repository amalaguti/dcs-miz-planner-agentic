## ADDED Requirements

### Requirement: Planner consults behaviour and inspiration options assertively
Planning and interactive chat system guidance MUST instruct the agent to call
`list_mission_options` and consider `mission_inspiration` and `mission_behaviour` rows
when the user leaves challenge/immersion details unspecified. The agent SHOULD pick an
inspiration pattern that fits the mission type, map it to supported behaviour recipes, and
emit typically one or two behaviours as valid Spec fields—unless the user forbids extras
or supplies conflicting hand-written triggers. Guidance MUST also direct the agent to call
`research_guidance` when tactics, procedures, historical colour, **or external mission
examples** would help, and to consult the **local installed campaign index**—especially
each campaign’s **`Doc/` briefing PDFs**—when local DCS campaigns can inspire structure or
theme—while treating research notes, `.cmp` playlists, Doc titles/text, and campaign
listings as non-authoritative for Spec fields. The agent MUST NOT invent Lua or unsupported
Spec types, MUST NOT download or emit third-party `.miz` as Spec, and MUST NOT force
narrative packs when zones/triggers are already non-empty.

#### Scenario: Prompt guidance mentions assertive creative selection
- **WHEN** the planning or chat system prompt is built
- **THEN** it MUST include guidance to consult `mission_inspiration` and
  `mission_behaviour` options (and research / local campaigns when inventing) and apply
  fitting supported behaviours when the user is vague about immersion/challenge

#### Scenario: Conflicts with hand triggers avoided
- **WHEN** guidance describes narrative or behaviour packs
- **THEN** it MUST retain the rule that narrative expansion conflicts with non-empty
  hand-authored zones/triggers
