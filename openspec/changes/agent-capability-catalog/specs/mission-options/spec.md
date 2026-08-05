## ADDED Requirements

### Requirement: Mission behaviour capability cards
The packaged Channel planning-option catalog SHALL include a `mission_behaviour` family of
curated capability cards for native Spec behaviours the agent may apply when inventing
mission challenges or immersion. Each card MUST have `id`, `label`, `description`,
`support` (`supported` for compile-backed behaviours), and `meta` that includes at least:
intent tags, applicable `mission_types` (or equivalent), Spec type names or recipe hints,
and an example Spec path when one exists. Cards MUST NOT invent unsupported Spec types or
Lua. v1 MUST include cards covering player altitude/speed gates, mark/smoke, narrative
packs, radio+late activation, sound callouts, and group_life_less.

#### Scenario: Behaviour family lists altitude/speed gate
- **WHEN** a caller lists planning options for family `mission_behaviour` with support
  `supported`
- **THEN** results MUST include a card for altitude/speed ingress gates

#### Scenario: Behaviour cards carry recipe meta
- **WHEN** a `mission_behaviour` option is returned after sync
- **THEN** its `meta` MUST include recipe or Spec-type hints suitable for agent emission
  without inventing Lua

### Requirement: Mission inspiration pattern cards
The packaged Channel planning-option catalog SHALL include a `mission_inspiration` family
of curated pattern cards that describe mission-design ideas drawn from stock Channel
missions, campaign/user-mission research notes, ME references, or patterns previously
promoted from web/community discovery. Cards SHOULD use support `advisory` (ideas, not
new compile fields). Each card MUST include `meta` that points at one or more
`mission_behaviour` ids (or equivalent Spec recipes) that realize the idea, and MAY
include a human-readable `source` label (e.g. stock IA pattern, research note, DCS User
Files audit). Cards MUST NOT embed raw `.miz` contents, MUST NOT require redistributing
third-party mission files, and MUST NOT authorize Lua or unsupported Spec types.

#### Scenario: Inspiration family present after sync
- **WHEN** a caller lists planning options for family `mission_inspiration`
- **THEN** results MUST include at least one advisory pattern card with behaviour linkage
  in `meta`

#### Scenario: Inspiration maps to behaviour, not Lua
- **WHEN** an inspiration card is returned
- **THEN** its guidance MUST map to packaged behaviour recipes or existing Spec vocabulary
  rather than free-form script

### Requirement: Behaviour and inspiration cards stay aligned with Spec vocabulary
When a new compile-backed trigger or narrative behaviour ships, the packaged
`mission_behaviour` catalog SHOULD gain or update a matching card in the same change
process. Inspiration cards that depend on that behaviour SHOULD be updated or added when
research promotes a durable pattern. Cards MUST remain recipes/ideas pointing at Spec
vocabulary; Mission Spec models and validation remain the compile source of truth.
Promoting patterns from user-mission or campaign audits MUST be a human-curated packaging
step (YAML/LESSONS), not automatic `.miz` import.

#### Scenario: Card does not invent Spec fields
- **WHEN** a behaviour or inspiration card lists Spec types or behaviour ids in `meta`
- **THEN** those references MUST resolve to types or cards already accepted by the product
  package
