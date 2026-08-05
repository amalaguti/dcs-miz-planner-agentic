## ADDED Requirements

### Requirement: list_mission_options surfaces mission behaviours and inspiration
`list_mission_options` MUST return packaged `mission_behaviour` and `mission_inspiration`
planning options (family, id, description, support, meta) after catalog sync so agents can
discover compile-backed recipes and design-pattern ideas. The tool description MUST mention
behaviour and inspiration capabilities (not only envelope enums).

#### Scenario: Tool returns mission_behaviour rows
- **WHEN** `list_mission_options` is called after catalog sync with behaviour cards packaged
- **THEN** the enriched options collection MUST include at least one `mission_behaviour`
  row with support `supported`

#### Scenario: Tool returns mission_inspiration rows
- **WHEN** `list_mission_options` is called after catalog sync with inspiration cards
  packaged
- **THEN** the enriched options collection MUST include at least one `mission_inspiration`
  row

### Requirement: Spec schema notes point at behaviour and inspiration options
When `get_mission_spec_schema` describes typed triggers or narrative, notes MUST mention
that curated recipes and design patterns are available via `list_mission_options` families
`mission_behaviour` and `mission_inspiration`, and that `research_guidance` may supply
tactics/historical colour **and** live mission-design discovery (DCS User Files, public
repos, references)—without treating research notes as Spec field authority.

#### Scenario: Schema notes mention mission_behaviour
- **WHEN** an agent requests the Spec schema for a mission type that supports triggers
- **THEN** the notes MUST reference `list_mission_options` / `mission_behaviour` (or
  equivalent wording) without inventing unsupported Spec fields

#### Scenario: Schema notes mention inspiration or research for creativity
- **WHEN** an agent requests the Spec schema for a mission type that supports triggers
- **THEN** the notes MUST reference `mission_inspiration` and/or `research_guidance` as
  creativity aids subordinate to Spec validation

### Requirement: research_guidance can target mission-design sources
`research_guidance` MUST support mission-design oriented live queries (via an explicit
focus parameter and/or query enrichment) that bias retrieval toward community and
reference sources useful for inventing missions—such as DCS User Files / mission listings,
public mission repositories, and mission-editor discussions—while retaining theatre,
aircraft, and mission_type context when provided. Offline mode MUST still return fixtures
without network. Live success MUST return structured notes with sources; live empty/error
MUST soft-fail to fixtures with a warning (existing contract). Notes MUST NOT authorize
LLM-authored Lua or invent Spec fields; the agent MUST map useful ideas onto packaged
`mission_behaviour` recipes.

#### Scenario: Mission-design live enrichment is testable
- **WHEN** `research_guidance` is invoked with mission-design focus (or equivalent) and an
  injectable live fetch
- **THEN** the fetch query (or tool result metadata) MUST reflect mission-design / DCS
  mission source bias beyond a bare user phrase alone

#### Scenario: Mission-design live soft-fails like other research
- **WHEN** mission-design live fetch returns empty or errors
- **THEN** the result MUST report ok with fixture notes and a live-unavailable warning

### Requirement: List installed campaign missions for inspiration
The system SHALL expose an agent-callable tool (e.g. `list_installed_campaigns`) that
discovers the local DCS World install root (reuse existing install discovery) and lists
campaigns under `Mods/campaigns`, including campaign display name when available, mission
`.miz` filenames, short description text when obtainable from lightweight `.cmp`
metadata, and filenames under each campaign’s `Doc/` folder when present (briefing PDFs,
intro, maps). The tool MUST be read-only, MUST NOT compile or import campaign `.miz` files into
Mission Specs, and MUST NOT require network access. When no DCS root or campaigns folder
is found, the tool MUST return a structured empty/failure result without inventing
campaigns. Tests MUST use a hermetic fixture tree rather than a machine-specific path.

#### Scenario: Campaigns listed from a fixture root
- **WHEN** the local campaign index is pointed at a test tree containing a campaign folder
  with a `.miz`, optional `.cmp`, and optional `Doc/*.pdf`
- **THEN** the result MUST include that campaign, its mission filename(s), and Doc
  filename(s) when present

#### Scenario: Missing install is non-fatal
- **WHEN** no DCS World root is discoverable
- **THEN** the tool MUST report a clear structured failure or empty list without crashing
  the agent loop
