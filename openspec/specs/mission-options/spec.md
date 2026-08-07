# Mission Options

## Purpose

Packaged Channel planning-option catalog with support levels so agents and users can
discover creative mission knobs without inventing DCS ids or claiming unsupported
fields compile.

## Requirements

### Requirement: Packaged planning option catalog
The system SHALL maintain packaged planning-option definitions for Channel mission
planning (families of knobs with ids, human labels, descriptions, and a support level of
`supported`, `advisory`, or `future`). Definitions MUST NOT invent DCS type ids.
`future` options MUST NOT be treated as compile-supported.

#### Scenario: Sync loads planning options
- **WHEN** catalog sync runs
- **THEN** the local catalog MUST contain planning options including at least weather and
  start-type entries marked `supported`

### Requirement: Query planning options
The system SHALL allow listing planning options (CLI and/or agent tool) filtered by family
and/or support level, returning structured rows suitable for agent reasoning.

#### Scenario: List supported weather options
- **WHEN** a caller lists planning options for family weather with support supported
- **THEN** results MUST include `sunny_clear` (or the packaged weather preset id)

#### Scenario: Future options are labeled
- **WHEN** a caller lists options that include a `future` entry
- **THEN** each such row MUST report support `future`

### Requirement: Honest support levels for the agent
Agent-facing option listing MUST expose support levels so planners can prefer `supported`
and `advisory` values and avoid claiming `future` knobs as compile-backed.

#### Scenario: list_mission_options includes enriched options
- **WHEN** `list_mission_options` is called after sync
- **THEN** the result MUST include an enriched options collection (or equivalent) with
  family, id, and support fields in addition to any legacy enum lists

### Requirement: CAP mission type in planning options
The packaged planning-option catalog SHALL include `mission_type` id `cap` marked
`supported`, describing Channel CAP / patrol planning.

#### Scenario: List supported mission types includes cap
- **WHEN** a caller lists planning options for family `mission_type` with support `supported`
- **THEN** results MUST include `cap` in addition to `free_flight` and `intercept`

### Requirement: ROE seeds are Spec-backed for CAP
Planning options in family `roe_seed` (`weapons_hold`, `weapons_free`, and any other
packaged ROE ids agreed in design) SHALL be marked `supported` (or `advisory` with
`meta.engagement` mapping) so agents can map them onto CAP Spec `cap.engagement`. They
MUST NOT be presented as free-floating compile fields for free_flight.

#### Scenario: ROE options no longer future-only
- **WHEN** catalog sync runs after this change
- **THEN** packaged `roe_seed` entries MUST NOT all remain `future`; at least the CAP-mapped
  engagement values MUST be discoverable as non-`future` support

### Requirement: Ground-attack mission type in planning options
The packaged planning-option catalog SHALL include `mission_type` id `ground_attack` marked
`supported`, describing Channel ground-attack / strike planning with targets and payload
selection.

#### Scenario: List supported mission types includes ground_attack
- **WHEN** a caller lists planning options for family `mission_type` with support `supported`
- **THEN** results MUST include `ground_attack` in addition to `free_flight`, `intercept`,
  and `cap`

### Requirement: Payload families are Spec-backed for ground attack
Planning options in family `payload_family` SHALL include at least the named Spitfire bomb
presets agreed in design (including a Channel-crossing preset with slipper tank), marked
`supported` (or `advisory` with `meta.payload` mapping) so agents can map them onto
ground-attack Spec `player.payload`. They MUST NOT be presented as compile-backed for
free_flight when the Spec forbids player payloads.

#### Scenario: Payload options no longer future-only
- **WHEN** catalog sync runs after this change
- **THEN** packaged `payload_family` entries MUST NOT all remain `future`; at least the
  Spitfire bomb and slipper-tank presets MUST be discoverable as non-`future` support

### Requirement: Escort mission type in planning options
The planning-options catalog SHALL list `mission_type` value `escort` as `supported`,
describing Channel escort / package-protection planning.

#### Scenario: escort listed as supported
- **WHEN** an agent or CLI lists mission-type planning options
- **THEN** `escort` MUST appear with status `supported`

### Requirement: Supported weather planning options for new presets
Planning options SHALL list `dawn_clear` and `marginal_vfr` under the `weather` family
with support level `supported` (compile-backed), alongside existing `sunny_clear`.

#### Scenario: List mission options includes new weather
- **WHEN** `list_mission_options` (or equivalent) is invoked
- **THEN** weather options MUST include `dawn_clear` and `marginal_vfr` as `supported`

### Requirement: Planning options list expanded weather patterns
Packaged planning options for family `weather` MUST include the expanded pattern
ids as `supported` (or honestly labeled) with descriptions aligned to registry
weather descriptions after catalog sync.

#### Scenario: Expanded weather listable
- **WHEN** `list_mission_options` runs after catalog sync
- **THEN** results MUST include the new weather pattern ids as well as the
  original trio

### Requirement: Seeded reroll planning option
The packaged Channel planning options SHALL include a `randomization` family entry that
describes seeded Spec rerolls (tool/CLI), with support level at least `advisory` once the
randomize tool exists. The entry MUST NOT claim a Mission Spec field mapping for the seed
itself (seed remains a transform argument).

#### Scenario: List options includes randomization
- **WHEN** `list_mission_options` is called after catalog sync
- **THEN** the result MUST include a planning option with family `randomization`

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

### Requirement: Mission-designer shelf families in planning options
The packaged planning-option catalog SHALL include families `dynamics_mode`,
`strike_target_class`, and `channel_place` for mission-designer co-authoring. Entries
MUST use support `supported`, `advisory`, or `future` honestly. `dynamics_mode` rows
MUST be Spec-backed (`supported`, or `advisory` with `meta` pointing at Spec
`dynamics.mode`) once dynamics expand ships. `strike_target_class` meta MUST NOT invent
DCS unit/ship ids (only ids present in packaged Channel ground/ship YAML).
`channel_place` MUST NOT invent airdromeIds.

#### Scenario: Dynamics modes packaged
- **WHEN** catalog sync runs after this change
- **THEN** listing planning options for family `dynamics_mode` MUST include ids
  `fixed`, `live`, `choose`, and `hybrid`

#### Scenario: Strike target classes packaged
- **WHEN** a caller lists planning options for family `strike_target_class`
- **THEN** results MUST include at least one land-domain class and one sea-domain class
  with meta that names domain and verified unit or ship ids where applicable

#### Scenario: Channel places packaged
- **WHEN** a caller lists planning options for family `channel_place`
- **THEN** results MUST include at least one place referencing Manston or another known
  Channel airfield without inventing airdrome ids

### Requirement: Dynamics mode options reflect Spec-backed expand
After dynamics expand ships, packaged `dynamics_mode` planning options MUST be marked so
agents do not treat them as emit-deferred-only: prefer `supported` (or `advisory` with
`meta` pointing at Spec `dynamics.mode`) consistently with other Spec-backed knobs.

#### Scenario: Catalog lists dynamics modes after sync
- **WHEN** catalog sync runs after this change
- **THEN** `dynamics_mode` rows MUST remain listable and describe Spec `dynamics.mode`
  values `fixed`, `live`, `choose`, `hybrid`

### Requirement: Player flight planning options
The Channel planning-options catalog SHALL expose player flight knobs the agent can ask
about: flight size (2–4 / solo by omission) and role (`lead` / `wingman`), with short
pilot-facing descriptions. Catalog sync MUST include these options for list/ask tools.

#### Scenario: Options list includes flight role
- **WHEN** a client lists mission planning options after this change
- **THEN** the catalog MUST include player flight size and role entries

### Requirement: Join-up planning option
Planning-options SHALL expose a supported knob for player flight join-up / follow
the lead (wingman), with a short description that lead same-group cohesion does not
need this flag.

#### Scenario: Options include join-up
- **WHEN** listing mission options after this change
- **THEN** a player-flight join-up (or equivalent) option MUST appear

### Requirement: Failure planning options
Planning-options SHALL expose supported failure-related knobs or example failure ids
the agent can discover (family for aircraft failures / training), without inventing
ids outside the catalog.

#### Scenario: Options list failures family
- **WHEN** listing mission options after catalog sync
- **THEN** failure-related supported entries MUST appear for Channel Spitfire

### Requirement: Section order planning options
Planning-options SHALL expose supported `player_flight_order` (or equivalent)
entries for curated section orders the agent can discover without inventing ids.

#### Scenario: Options list order family
- **WHEN** listing mission options after catalog sync
- **THEN** supported section-order entries MUST appear for Channel player flight

### Requirement: Planning options list showers scattered
Packaged planning options for family `weather` MUST include
`showers_scattered` as `supported` with a description aligned to the registry
weather description after catalog sync.

#### Scenario: Showers listable
- **WHEN** `list_mission_options` runs after catalog sync
- **THEN** weather results MUST include `showers_scattered` as `supported`
