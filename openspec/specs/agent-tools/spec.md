# Agent Tools

## Purpose

Stable, agent-facing callables over the known catalog and the existing validate/compile
path. Results are structured for later LLM tool calling. No LLM or MCP wiring in this
capability.

## Requirements

### Requirement: Catalog lookup tools
The system SHALL expose callable tools `find_airfield` and `get_aircraft_details` that query
the known agent catalog (after ensuring it is synced). Results MUST be structured and MUST NOT
invent DCS identifiers absent from the known catalog.

#### Scenario: Find Manston
- **WHEN** `find_airfield` is called with a query that matches Manston
- **THEN** the result MUST include airfield name Manston and its known airdrome id

#### Scenario: Find Mozdok on Caucasus
- **WHEN** `find_airfield` is called for `Mozdok`
- **THEN** the result MUST include `airdromeId` 28 and theatre `Caucasus`
  and MUST NOT be a Normandy Needs Oar Point row

#### Scenario: Aircraft details for Spitfire
- **WHEN** `get_aircraft_details` is called for `SpitfireLFMkIX`
- **THEN** the result MUST include that aircraft id and its known radio frequency

#### Scenario: Unknown aircraft
- **WHEN** `get_aircraft_details` is called for an id not in the known catalog
- **THEN** the result MUST indicate failure without inventing aircraft data

### Requirement: List mission options tool
The system SHALL expose `list_mission_options` that returns known planning enumerations from
the catalog (at least mission types, start types, weather presets) and offerable theatres
from the catalog/install join, **and** an enriched planning-options collection with family,
id, description, and support level (`supported` | `advisory` | `future`).

#### Scenario: Options include free flight and intercept
- **WHEN** `list_mission_options` is called after catalog sync
- **THEN** the result MUST include mission types `free_flight` and `intercept`

#### Scenario: Offerable theatres reflected
- **WHEN** TheChannel is offerable on the local machine
- **THEN** `list_mission_options` MUST list TheChannel among offerable theatres

#### Scenario: Enriched planning options present
- **WHEN** `list_mission_options` is called after catalog sync
- **THEN** the result MUST include planning option rows with support levels for agent use

### Requirement: Validate and compile tools
The system SHALL expose `validate_mission_spec` and `compile_mission` tools that wrap the
existing shared validation engine and PyDCS compiler. Validate/compile MUST remain
registry- and install-backed; tools MUST NOT bypass those engines or emit LLM-authored Lua.

#### Scenario: Validate Manston free flight Spec
- **WHEN** `validate_mission_spec` is given the checked-in Manston cold free-flight Spec path
- **THEN** the result MUST report ok (valid)

#### Scenario: Compile Manston free flight Spec
- **WHEN** `compile_mission` is given that Spec path and an output path
- **THEN** the tool MUST write a `.miz` at the output path (or a clear structured failure)

### Requirement: Prefs and history tools
The system SHALL expose callable tools `get_user_prefs`, `set_user_prefs`,
`record_generation`, `record_feedback`, and `list_generation_history` that read and write
user-memory tables. Results MUST be structured `{ok: …}` dicts consistent with other
agent tools. These tools MUST NOT invent DCS identifiers or bypass validation/compile.

#### Scenario: Get prefs when empty
- **WHEN** `get_user_prefs` is called with no prefs stored
- **THEN** the result MUST report ok and an empty prefs map

#### Scenario: Set and get prefs
- **WHEN** `set_user_prefs` writes a preference and `get_user_prefs` is called
- **THEN** the result MUST include that preference

#### Scenario: List recent history
- **WHEN** at least one generation has been recorded and `list_generation_history` is called
- **THEN** the result MUST include that generation in the recent list

### Requirement: Research guidance tool
The system SHALL expose a callable `research_guidance` tool that returns short notes on
flight procedures, combat manoeuvres, pilot accounts, or historical context for commander
briefs. Offline/stub mode MUST use fixtures without network access. Live mode MUST attempt
web-backed retrieval (best-effort free providers; no research API key required). When live
retrieval succeeds, notes MUST include at least one non-fixture source. When live was
requested and retrieval fails or returns no snippets, the result MUST still be structured
ok with fixture notes AND MUST include a clear `warning` stating that live research was
unavailable and fixtures are being used. Failures MUST soft-fail and MUST NOT invent DCS
identifiers or Spec field authority. Live fetch queries MUST incorporate available
`mission_type`, `theatre`, and `aircraft` context when provided.

#### Scenario: Offline research returns notes
- **WHEN** `research_guidance` is called in offline mode for an intercept-oriented query
- **THEN** the result MUST report ok with non-empty notes and MUST NOT require network access

#### Scenario: Live success returns web-sourced notes
- **WHEN** `research_guidance` is called with live enabled and the injectable/live fetch
  returns non-empty web notes
- **THEN** the result MUST report ok with at least one note whose source is not a fixture
  id, and MUST NOT set a live-unavailable warning

#### Scenario: Live empty soft-fails with warning
- **WHEN** `research_guidance` is called with live enabled and the live fetch returns no
  snippets
- **THEN** the result MUST report ok with fixture notes and MUST include a warning that live
  research returned no snippets (or equivalent live-unavailable wording)

#### Scenario: Live error soft-fails with warning
- **WHEN** `research_guidance` is called with live enabled and the live fetch raises a
  network or parse error
- **THEN** the result MUST report ok with fixture notes and MUST include a warning that
  mentions the live fetch failure

### Requirement: Research notes are sanitized before agent use
`research_guidance` MUST sanitize each returned note’s `title` and `snippet` by stripping
ASCII control characters (except tab and newline), normalizing runs of whitespace, and
enforcing maximum lengths so untrusted live web text cannot freely inject arbitrary
control sequences or unbounded payloads into tool results.

#### Scenario: Control characters stripped
- **WHEN** live or fixture notes contain control characters in title or snippet
- **THEN** the tool result notes MUST omit those control characters (tab/newline MAY remain)

#### Scenario: Length caps applied
- **WHEN** a note snippet exceeds the configured maximum length
- **THEN** the returned snippet MUST be truncated to that maximum

### Requirement: Research results label retrieval mode
`research_guidance` results MUST expose a clear retrieval mode (`live`, `fixture`, or
`mixed`) derived from note sources, and MUST keep soft-fail `warning` text when live was
requested but fixtures were used. Fixture-backed notes MUST retain `fixture:` sources;
live notes MUST NOT be labeled as fixtures.

#### Scenario: Offline returns fixture mode
- **WHEN** `research_guidance` runs offline/stub
- **THEN** the result MUST report retrieval mode `fixture` (or equivalent) and fixture
  sources on notes

#### Scenario: Live soft-fail still labeled
- **WHEN** live fetch fails or is empty and fixtures are returned with a warning
- **THEN** the result MUST still label notes as fixture-backed and include the warning

### Requirement: Mission Spec schema tool
The system SHALL expose `get_mission_spec_schema` that, given a supported
`mission_type` (`free_flight`, `intercept`, `cap`, or `ground_attack`), returns a compact
Mission Spec example JSON object plus human-readable notes and anti-patterns for that type.
The example MUST validate as a `MissionSpec` under the shared schema. The payload MUST be
derived from packaged examples and/or the Pydantic Spec model — not from a hand-edited
SQLite schema as source of truth. Unsupported or unknown `mission_type` MUST return a
structured error without inventing a Spec.

#### Scenario: CAP schema example validates
- **WHEN** `get_mission_spec_schema` is called with `mission_type` `cap` after the tool
  is registered
- **THEN** the result MUST be ok and MUST include an `example` object that validates as
  Mission Spec `schema_version` `"1"` with `mission_type` `cap`

#### Scenario: Ground-attack schema example validates
- **WHEN** `get_mission_spec_schema` is called with `mission_type` `ground_attack` after the
  tool is registered
- **THEN** the result MUST be ok and MUST include an `example` object that validates as
  Mission Spec `schema_version` `"1"` with `mission_type` `ground_attack`

#### Scenario: Unknown mission type errors
- **WHEN** `get_mission_spec_schema` is called with an unsupported `mission_type`
- **THEN** the result MUST not be ok and MUST include a clear error (no fabricated Spec)

#### Scenario: Tool available on bridge
- **WHEN** the standard agent tool definitions are listed
- **THEN** `get_mission_spec_schema` MUST be among the registered function tools

### Requirement: Escort schema via get_mission_spec_schema
The `get_mission_spec_schema` agent tool SHALL support `mission_type` `escort`, returning a
derived example shape consistent with the checked-in escort example (nested `escort`,
`package`, optional `enemies`, `escort_package` objective).

#### Scenario: Escort schema example validates
- **WHEN** an agent or test requests `get_mission_spec_schema` for `escort`
- **THEN** the returned example MUST load as a structurally valid escort Mission Spec
  (subject to registry checks)

### Requirement: Stable import surface
Agent-facing callers MUST be able to import the tool callables from a single package surface
(e.g. `dcs_miz_planner.tools`) without depending on unrelated internal modules for catalog
lookup, validate/compile, user-memory, and research-guidance operations.

#### Scenario: Import tools package
- **WHEN** a test imports the tools surface
- **THEN** the catalog, validate/compile, user-memory, and research guidance tools MUST be
  available for invocation

### Requirement: Randomize mission tool
The system SHALL expose a callable tool `randomize_mission` that accepts a Mission Spec
(path or structured body), an integer `seed`, and optional `axes`, and returns a
structured result containing the randomized Spec (as data), the seed, and the axes
applied. The tool MUST use the shared seeded Spec→Spec transform and MUST NOT compile a
`.miz` itself. On failure (invalid Spec, unknown axis, validation failure of output) the
result MUST indicate failure with a clear message and MUST NOT invent DCS identifiers.

#### Scenario: Tool returns a Spec dict
- **WHEN** `randomize_mission` is called with a valid free-flight Spec path and seed `42`
- **THEN** the result MUST report ok and include a Spec-shaped payload whose
  `player.airfield` matches the base Spec

#### Scenario: Unknown axis fails cleanly
- **WHEN** `randomize_mission` is called with an unknown axis name
- **THEN** the result MUST report failure without writing files or inventing Spec fields

### Requirement: Spec schema notes include triggers
When `get_mission_spec_schema` (or equivalent prompt fragment) describes a mission type, it
MUST mention that optional typed `zones` / `triggers` may appear, MUST NOT encourage Lua or
script fields, and MUST note that validated non-empty triggers compile to native ME trigger tables.

#### Scenario: Schema notes mention triggers
- **WHEN** an agent requests the Spec schema for `free_flight` or `cap`
- **THEN** the notes or example guidance MUST reference optional triggers/zones without
  inventing unsupported condition types

### Requirement: Spec schema notes include narrative
When `get_mission_spec_schema` (or equivalent prompt fragment) describes combat mission
types, it MUST mention optional opt-in `narrative.enabled` for CAP, intercept, escort, and
ground_attack (expands to typed zones/triggers), MUST NOT encourage Lua, and MUST note
that narrative conflicts with hand-authored non-empty zones/triggers.

#### Scenario: Schema notes mention narrative
- **WHEN** an agent requests the Spec schema for `cap`, `intercept`, `escort`, or
  `ground_attack`
- **THEN** the notes MUST reference optional narrative without inventing unsupported
  trigger types

### Requirement: Spec schema notes include intercept narrative
When `get_mission_spec_schema` describes `intercept`, it MUST mention optional
`narrative.enabled` (expands to typed triggers; conflicts with hand-authored
zones/triggers; requires enemies).

#### Scenario: Intercept schema notes mention narrative
- **WHEN** an agent requests the Spec schema for `intercept`
- **THEN** the notes MUST reference optional narrative without inventing unsupported
  trigger types

### Requirement: Spec schema notes include escort narrative
When `get_mission_spec_schema` describes `escort`, it MUST mention optional
`narrative.enabled` (expands to typed zones/triggers; conflicts with hand-authored
zones/triggers; requires escort, package, and enemies).

#### Scenario: Escort schema notes mention narrative
- **WHEN** an agent requests the Spec schema for `escort`
- **THEN** the notes MUST reference optional narrative without inventing unsupported
  trigger types

### Requirement: Spec schema notes include ground-attack narrative
When `get_mission_spec_schema` describes `ground_attack`, it MUST mention optional
`narrative.enabled` (expands to typed zones/triggers; conflicts with hand-authored
zones/triggers; requires strike and targets).

#### Scenario: Ground-attack schema notes mention narrative
- **WHEN** an agent requests the Spec schema for `ground_attack`
- **THEN** the notes MUST reference optional narrative without inventing unsupported
  trigger types beyond the documented v1 vocabulary (including `target_dead`)

### Requirement: Spec schema notes include radio and late activation
When `get_mission_spec_schema` describes combat mission types that support enemies or
targets, it MUST mention optional `late_activation` on those entries and optional trigger
actions `radio_item_add` / `radio_item_remove` / `activate_group` / `deactivate_group`
(native ME; no Lua).

#### Scenario: CAP or intercept schema mentions radio actions
- **WHEN** an agent requests the Spec schema for `cap` or `intercept`
- **THEN** the notes MUST reference radio and/or late activation without inventing Lua
  fields

### Requirement: Spec schema notes include sound and numeric flags
When `get_mission_spec_schema` describes typed triggers, it MUST mention optional action
`sound` (curated `asset_id` only) and optional numeric/timed flag vocabulary
(`flag_equals` / `flag_more` / `flag_less` / `time_since_flag`, `inc_flag` /
`set_flag_value`) alongside existing bool flags and radio/late-activation notes. Notes
MUST NOT invent Lua or arbitrary sound path fields.

#### Scenario: Schema mentions sound and numeric flags
- **WHEN** an agent requests the Spec schema for a mission type that supports triggers
- **THEN** the notes MUST reference sound `asset_id` and numeric flag types without
  inventing unsupported fields

### Requirement: Spec schema notes include group life less
When `get_mission_spec_schema` describes typed triggers, it MUST mention optional
condition `group_life_less` (`enemy_index` or `target_index` plus `percent` 1–100 for
remaining group life) alongside existing dead, flag, sound, and radio notes. Notes MUST
NOT invent Lua or raw DCS group ids.

#### Scenario: Schema mentions group_life_less
- **WHEN** an agent requests the Spec schema for a mission type that supports triggers
- **THEN** the notes MUST reference `group_life_less` without inventing unsupported fields

### Requirement: Spec schema notes include mark and smoke
When `get_mission_spec_schema` describes typed triggers, it MUST mention optional actions
`mark` (zone name + text for F10 map mark) and `smoke` (zone name + curated color for ME
Smoke Marker) alongside existing dead, life-less, flag, sound, and radio notes. Notes MUST
NOT invent Lua, raw map coordinates, or author mark ids.

#### Scenario: Schema mentions mark and smoke
- **WHEN** an agent requests the Spec schema for a mission type that supports triggers
- **THEN** the notes MUST reference `mark` and `smoke` without inventing unsupported fields

### Requirement: Spec schema notes include altitude and speed gates
When `get_mission_spec_schema` describes typed triggers, it MUST mention optional
conditions `unit_altitude_higher` / `unit_altitude_lower` (`altitude_m`, optional `agl`)
and `unit_speed_higher` / `unit_speed_lower` (`speed_kmh`) as player-unit gates alongside
existing dead, life-less, flag, sound, mark/smoke, and radio notes. Notes MUST NOT invent
Lua, raw unit ids, or enemy-targeted altitude/speed fields.

#### Scenario: Schema mentions altitude and speed gates
- **WHEN** an agent requests the Spec schema for a mission type that supports triggers
- **THEN** the notes MUST reference altitude and speed gate conditions without inventing
  unsupported fields

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

### Requirement: Offline research includes indexed QAG fixtures
Offline `research_guidance` MUST return notes drawn from a packaged **index** of
local DCS Quick Action Generator (QAG) educational HTML pages when those files
are present under the gitignored `research/` dump (era + generator mission/class
colour), in addition to any canned Channel/Spitfire fixtures. The HTML pages
MUST NOT be shipped in the package. Notes MUST use `fixture:` sources
(e.g. `fixture:qag:<id>`). Snippets MUST state that QAG UI names, site templates,
and internal template strings are not Mission Spec or PyDCS catalog identifiers.
The tool MUST NOT write QAG names into registry YAML or invent Spec
`mission_type` values from QAG generator families (Dogfight, Bomber Escort,
Bomber Intercept, Anti-Ship SR, SEAD SR). A known duplicate/mis-copied HTML page
MUST NOT be served as a second fixture. Matching MUST use the caller query and,
when provided, `mission_type`, theatre, and `focus=mission_design`. When the
local dump is absent, the tool MUST still report ok with canned fixtures and
MUST NOT fail. Live success/soft-fail contracts are unchanged.

#### Scenario: Offline ground-attack query returns QAG ground colour
- **WHEN** `research_guidance` is called in offline mode with a ground-attack or
  artillery/armor-oriented query and the matching local QAG HTML is present
- **THEN** the result MUST report ok with at least one note whose source starts
  with `fixture:qag:` and whose snippet warns that QAG names are not Spec ids

#### Scenario: Offline mission-design focus can return QAG pages
- **WHEN** `research_guidance` is called in offline mode with `focus=mission_design`
  (or equivalent) and a non-empty query and a matching local QAG page is present
- **THEN** the result MUST include at least one `fixture:qag:` note

#### Scenario: Duplicate Cold War anti-ship page is not served
- **WHEN** offline notes are gathered for an anti-ship oriented query and local
  QAG HTML is present
- **THEN** the result MUST NOT include two fixtures that are the same WWII
  anti-ship HTML document (the mis-copied Cold War anti-ship file MUST be skipped)

#### Scenario: Missing research dump skips QAG notes
- **WHEN** `research_guidance` is called in offline mode and the local `research/`
  dump is absent
- **THEN** the result MUST report ok without `fixture:qag:` notes and MUST still
  include canned fixture notes

#### Scenario: QAG fixtures remain untrusted colour
- **WHEN** a QAG fixture note is returned
- **THEN** its source MUST be a `fixture:` id and its snippet MUST NOT authorize
  new Spec mission types or catalog unit keys

### Requirement: List installed campaign missions for inspiration
The system SHALL expose an agent-callable tool (e.g. `list_installed_campaigns`) that
discovers the local DCS World install root (reuse existing install discovery) and lists
campaigns under `Mods/campaigns`, including campaign display name when available, mission
`.miz` filenames, short description text when obtainable from lightweight `.cmp`
metadata, and Doc PDF filenames under each campaign’s `Doc/` folder when present.
By default the tool MUST NOT extract PDF body text (filenames / null excerpts only).
When an explicit opt-in flag (e.g. `include_doc_text`) is set, the tool MAY return short
text excerpts from local `Doc/*.pdf` files subject to size/page/length caps. Extracted
excerpts MUST be cached keyed by file path and content identity (at least mtime and size)
so unchanged PDFs are not re-read on later calls. The tool MUST be read-only, MUST NOT
compile or import campaign `.miz` files into Mission Specs, and MUST NOT require network
access. When no DCS root or campaigns folder is found, the tool MUST return a structured
empty/failure result without inventing campaigns. Tests MUST use a hermetic fixture tree
rather than a machine-specific path.

#### Scenario: Campaigns listed from a fixture root
- **WHEN** the local campaign index is pointed at a test tree containing a campaign folder
  with a `.miz`, optional `.cmp`, and optional `Doc/*.pdf`
- **THEN** the result MUST include that campaign, its mission filename(s), and Doc
  filename(s) when present

#### Scenario: Missing install is non-fatal
- **WHEN** no DCS World root is discoverable
- **THEN** the tool MUST report a clear structured failure or empty list without crashing
  the agent loop

#### Scenario: Default Doc entries omit body text
- **WHEN** a campaign folder contains `Doc/*.pdf` files and Doc text extract is not opted in
- **THEN** the tool result MUST expose those PDF filenames and MUST NOT return extracted
  PDF body text

#### Scenario: Opt-in Doc extract returns excerpt
- **WHEN** Doc text extract is opted in against a hermetic campaign tree with a readable PDF
- **THEN** the tool result MUST include a non-empty excerpt for that Doc (subject to caps)

#### Scenario: Unchanged PDF uses cache
- **WHEN** Doc text extract is opted in twice for the same unchanged PDF path
- **THEN** the second call MUST return the cached excerpt without re-parsing the PDF file


### Requirement: Creative bias from history and feedback
The system SHALL provide a deterministic helper (callable from tests and planning hosts)
that, given recent generation history rows (with optional `creative` detail) and
linked satisfaction feedback, returns soft `prefer` and `avoid` lists of
`mission_behaviour` ids for an optional mission type filter. Higher scores and
liked-style tags MUST bias toward prefer; low scores and avoid-style tags toward
avoid. Empty history MUST yield empty prefer/avoid lists.

#### Scenario: High score with behaviours prefers them
- **WHEN** a success generation detail lists behaviours and feedback score is high
- **THEN** the bias helper MUST include at least one of those behaviours in prefer
  (for matching mission type when filtered)

#### Scenario: Empty history yields no bias
- **WHEN** no generations exist
- **THEN** prefer and avoid MUST be empty

### Requirement: Agent tools document creative detail and bias
Planning guidance MUST state that generation `detail` MAY carry `creative`
inspiration/behaviour ids, and that `list_generation_history` (plus feedback when
available) SHOULD inform creative picks on vague asks. Host-owned mutating tool
definitions (when present for admin/tests) MUST still document optional creative detail
on `record_generation`.

#### Scenario: record_generation description mentions creative detail
- **WHEN** mutating/admin tool definitions are inspected
- **THEN** `record_generation` guidance MUST mention optional creative decision detail
  (or an equivalent documented host convention tested in prompts)

### Requirement: Default agent tools are read-only
The default LLM tool list for planning and chat MUST omit mutating tools
(`compile_mission`, `set_user_prefs`, `record_generation`, `record_feedback`). Those
operations MUST remain available to host code via Python APIs or an explicit
`allow_mutating` dispatch flag for tests/admin, not via the default agent tool surface.

#### Scenario: Default tools exclude compile and prefs write
- **WHEN** the default planning tool definitions are listed
- **THEN** they MUST NOT include `compile_mission`, `set_user_prefs`, `record_generation`,
  or `record_feedback`

#### Scenario: Mutating dispatch blocked by default
- **WHEN** `dispatch_tool` is called for `compile_mission` without mutating allowed
- **THEN** it MUST return a structured error and MUST NOT write a `.miz`

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

### Requirement: Compile output path allowlist
When `compile_mission` runs (host or allowed dispatch), the output path MUST resolve to a
location under an allowed `out/` directory. Paths outside that tree MUST be rejected.

#### Scenario: Compile outside out rejected
- **WHEN** compile is requested with an output path outside the allowed `out/` tree
- **THEN** the call MUST fail with a clear path error and MUST NOT write the file

### Requirement: list_mission_options surfaces mission-designer shelves
`list_mission_options` MUST return packaged `dynamics_mode`, `strike_target_class`, and
`channel_place` planning options (family, id, description, support, meta) after catalog
sync so agents can co-author recommendations from declared shelves. The tool description
MUST mention these designer shelves (not only envelope enums and behaviour cards) and that
`dynamics_mode` corresponds to Spec `dynamics` expand.

#### Scenario: Tool returns dynamics_mode rows
- **WHEN** `list_mission_options` is called after catalog sync with dynamics modes packaged
- **THEN** the enriched options collection MUST include `dynamics_mode` rows for
  `fixed`, `live`, `choose`, and `hybrid`

#### Scenario: Tool returns strike_target_class rows
- **WHEN** `list_mission_options` is called after catalog sync with strike classes packaged
- **THEN** the enriched options collection MUST include at least one
  `strike_target_class` row whose meta includes `domain`

#### Scenario: Tool returns channel_place rows
- **WHEN** `list_mission_options` is called after catalog sync with places packaged
- **THEN** the enriched options collection MUST include at least one `channel_place` row

### Requirement: Tool surface describes dynamics expand
Agent-facing tool descriptions (`list_mission_options` / schema tool notes as applicable)
MUST mention that `dynamics_mode` catalog rows correspond to Spec `dynamics` expand once
this capability ships.

#### Scenario: list_mission_options description stays honest
- **WHEN** tool definitions are listed after this change
- **THEN** `list_mission_options` description MUST still surface `dynamics_mode` and MUST
  not claim dynamics cannot be emitted if Spec expand exists

### Requirement: Agent tool reweathers mission files
The agent tool surface SHALL expose a mutating tool to re-weather an existing
`.miz` (optional Spec path, weather pattern id, optional seed) that invokes the
same library API as the CLI. The tool MUST report overwrite path and whether
Spec recompile or miz patch was used.

#### Scenario: Tool reweather with pattern
- **WHEN** the agent tool is called with a `.miz` path and `broken_channel`
- **THEN** the result MUST be ok on success and include the overwritten path

### Requirement: Tools surface player flight options
Agent-facing tools that expose planning options or Spec shape MUST surface the player
flight size/role knobs once present in planning-options / schema, without adding compile
or write tools beyond the existing host trust boundary.

#### Scenario: List options returns flight knobs
- **WHEN** `list_mission_options` (or equivalent) runs after catalog sync
- **THEN** results MUST include the player flight size and role options

### Requirement: Agent tools aware of recon
Agent-facing tools and derived Spec schema SHALL allow `mission_type` `recon` and document
the nested `recon` block, `recon_area` objective, no-payload rule, and optional observe-only
contacts.

#### Scenario: Schema mentions recon
- **WHEN** `get_mission_spec_schema` (or equivalent) is asked for recon / general shape
- **THEN** the result MUST describe recon fields and forbid payload on recon

### Requirement: Agent schema warns surfaced-only U-boat
Derived Spec schema / planning notes SHALL state that Channel U-boat missions use
existing `recon` or `ground_attack` with `Uboat_VIIC` sea contacts/targets, that attacks
are **surfaced only**, and that submerged ASW / depth charges are out of scope.

#### Scenario: Schema mentions surfaced U-boat
- **WHEN** `get_mission_spec_schema` notes are requested for recon or ground_attack
- **THEN** notes MUST mention surfaced-only U-boat / sea_craft guidance (or a shared
  common note to that effect)

### Requirement: Schema documents target motion
Derived Spec schema notes SHALL document optional `targets[].motion`
(`static` | `patrol` | `path`), required companion fields, and heuristics
(sea/soft vehicles move; harbour/AAA static).

#### Scenario: Schema mentions motion
- **WHEN** `get_mission_spec_schema` notes are requested for ground_attack or recon
- **THEN** notes MUST mention optional target motion fields

### Requirement: Schema documents target AI options
Derived Spec schema notes SHALL document optional `ai_preset`, `ai` allowlisted
keys, `move_formation`, class/domain restrictions, and that ME UI lists are not
capability guarantees.

#### Scenario: Schema mentions target AI
- **WHEN** `get_mission_spec_schema` notes are requested for ground_attack or recon
- **THEN** notes MUST mention target AI / move_formation allowlists

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

### Requirement: Tool guidance for target invent order
Agent tool descriptions (or invent-facing notes) for `list_strike_targets` and
`list_mission_options` SHALL state that GA/recon invent should call those tools
before emitting `targets[]`, preferring returned unit ids and shelf presets
(motion / ai_preset) over invented strings.

#### Scenario: list_strike_targets and list_mission_options mention invent order
- **WHEN** TOOL_DEFINITIONS for those tools are loaded
- **THEN** descriptions MUST mention calling before inventing targets[] and
  preferring returned unit ids / shelf presets

### Requirement: Options tool surfaces place geometry
`list_mission_options` results (via catalog sync) SHALL include the numeric
geometry fields on `channel_place` rows so invent can read recipes without
hardcoding bearings in prompts alone.

#### Scenario: Place options include bearing distance meta
- **WHEN** list_mission_options returns channel_place rows after sync
- **THEN** french coast and mid-Channel rows MUST expose strike/AOI bearing and
  distance fields in meta

### Requirement: list_mission_options includes offerable Normandy
When Normandy is offerable on the local machine, `list_mission_options` MUST
list `Normandy` among offerable theatres.

#### Scenario: Offerable Normandy reflected
- **WHEN** Normandy is offerable on the local machine
- **THEN** `list_mission_options` MUST list Normandy among offerable theatres

### Requirement: Spec schema tool accepts theatre
`get_mission_spec_schema` SHALL accept an optional theatre id. When theatre is
`Normandy` and mission type is `free_flight`, the derived example MUST follow
the Needs Oar Point envelope (not Manston). When theatre is `Normandy` and
mission type is `cap`, the derived example MUST follow the Needs Oar Point CAP
envelope (not Manston). When theatre is `Normandy` and mission type is
`ground_attack`, the derived example MUST follow the Needs Oar Point
ground-attack envelope (not Manston). When theatre is `Normandy` and mission
type is `intercept`, the derived example MUST follow the Needs Oar Point
intercept envelope (not Manston or Hawkinge). When theatre is `Normandy` and
mission type is `escort`, the derived example MUST follow the Needs Oar Point
escort envelope (not Manston 120/55). When theatre is `Normandy` and
mission type is `recon`, the tool MUST NOT return a Channel
combat skeleton.

#### Scenario: Normandy free_flight schema uses NeedsOarPoint
- **WHEN** a caller requests the free_flight Spec schema with theatre
  `Normandy`
- **THEN** the example/notes MUST use `NeedsOarPoint` (not `Manston`)

#### Scenario: Normandy CAP schema uses NeedsOarPoint
- **WHEN** a caller requests the cap Spec schema with theatre `Normandy`
- **THEN** the example MUST use `NeedsOarPoint` and MUST NOT use Manston
  CAP station 135° / 25 km

#### Scenario: Normandy recon schema has no Manston skeleton
- **WHEN** a caller requests a recon schema with theatre `Normandy`
- **THEN** the result MUST NOT present a Manston combat example as the
  template to copy

### Requirement: list_mission_options can filter channel_place by theatre
`list_mission_options` SHALL accept an optional theatre id. When theatre is
set, returned `channel_place` rows MUST have `meta.theatre` equal to that id.
Other option families MUST still be returned. When theatre is omitted, the
tool MAY return all `channel_place` rows (backward compatible).

#### Scenario: Channel filter omits Cherbourg CAP place
- **WHEN** `list_mission_options` is called with theatre `TheChannel`
- **THEN** results MUST NOT include `cherbourg_channel_cap` or
  `needs_oar_point_home`

#### Scenario: Normandy filter omits french coast belt
- **WHEN** `list_mission_options` is called with theatre `Normandy`
- **THEN** results MUST NOT include `manston_home` or
  `french_coast_strike_belt`

### Requirement: list_strike_targets can filter theatre
`list_strike_targets` SHALL accept an optional theatre filter. For theatre
`Normandy`, the result MUST include packaged WWII **land** strike units (not
an empty list). Sea-domain units MUST remain omitted for Normandy. For
Caucasus, Syria, Nevada, and Falklands the result MUST remain empty.

#### Scenario: Normandy strike list includes land units
- **WHEN** `list_strike_targets` is called with theatre `Normandy` after sync
- **THEN** the result MUST include a known land unit (e.g. `Blitz_36-6700A`)
  and MUST NOT include sea_craft

### Requirement: Spec schema tool accepts Normandy intercept
`get_mission_spec_schema` SHALL accept theatre `Normandy` with mission type
`intercept`. The derived example MUST follow the Needs Oar Point intercept
envelope (not Manston) and notes MUST NOT concatenate Channel template
bundles that cite Hawkinge. When mission type is `recon` on
Normandy, the tool MUST NOT return a Channel combat skeleton.

#### Scenario: Normandy intercept schema uses NeedsOarPoint
- **WHEN** a caller requests the intercept Spec schema with theatre
  `Normandy`
- **THEN** the example MUST use `NeedsOarPoint` and theatre `Normandy` (not
  Manston)

### Requirement: Spec schema tool accepts Normandy escort
`get_mission_spec_schema` SHALL accept theatre `Normandy` with mission type
`escort`. The derived example MUST follow the Needs Oar Point escort envelope
(not Manston) and notes MUST NOT concatenate Channel template bundles that
cite Manston 120/55. When mission type is `recon` on Normandy, the tool MUST
NOT return a Channel combat skeleton.

#### Scenario: Normandy escort schema uses NeedsOarPoint
- **WHEN** a caller requests the escort Spec schema with theatre `Normandy`
- **THEN** the example MUST use `NeedsOarPoint`, theatre `Normandy`, and
  escort geometry 180° / 63 km (not Manston 120° / 55 km)

### Requirement: Spec schema tool accepts Normandy recon
`get_mission_spec_schema` SHALL accept theatre `Normandy` with mission type
`recon`. The derived example MUST follow the Needs Oar Point recon envelope
(not Manston) and notes MUST NOT concatenate Channel template bundles that
cite french-coast belts or Manston 125/76.

#### Scenario: Normandy recon schema uses NeedsOarPoint
- **WHEN** a caller requests the recon Spec schema with theatre `Normandy`
- **THEN** the example MUST use `NeedsOarPoint`, theatre `Normandy`, and
  recon AOI 180° / 133 km (not Manston 125° / 76 km)

### Requirement: Spec schema tool accepts Normandy ground_attack
`get_mission_spec_schema` SHALL accept theatre `Normandy` with mission type
`ground_attack`. The derived example MUST follow the Needs Oar Point
ground-attack envelope (not Manston) and notes MUST NOT concatenate Channel
template bundles that cite french-coast belts or Manston YAML paths. When
mission type is `recon` on Normandy, the tool MUST
NOT return a Channel combat skeleton.

#### Scenario: Normandy ground_attack schema uses NeedsOarPoint
- **WHEN** a caller requests the ground_attack Spec schema with theatre
  `Normandy`
- **THEN** the example MUST use `NeedsOarPoint`, theatre `Normandy`, and
  strike geometry inland of Maupertus (not Manston 125° / 76 km)

### Requirement: Spec schema tool accepts Caucasus
`get_mission_spec_schema` SHALL accept theatre `Caucasus`. When mission type
is `free_flight`, the derived example MUST follow the Batumi envelope (not
Manston or NeedsOarPoint) and notes MUST NOT concatenate Channel/Normandy
template bundles (Manston YAML paths, Spitfire failure shelves,
`channel_place`). When mission type is combat including `cap`, the
tool MUST NOT return a Channel or Normandy combat skeleton.

#### Scenario: Caucasus free_flight schema uses Batumi
- **WHEN** a caller requests the free_flight Spec schema with theatre
  `Caucasus`
- **THEN** the example MUST use `Batumi`, `Su-25T`, and `Georgia`

#### Scenario: Caucasus combat schema has no Manston skeleton
- **WHEN** a caller requests a cap or intercept schema with theatre
  `Caucasus`
- **THEN** the result MUST NOT present a Manston or NeedsOarPoint example as
  the template to copy

### Requirement: Spec schema tool accepts Syria
`get_mission_spec_schema` SHALL accept theatre `Syria`. When mission type
is `free_flight`, the derived example MUST follow the Incirlik envelope (not
Manston, NeedsOarPoint, or Batumi) and notes MUST NOT concatenate
Channel/Normandy/Caucasus template bundles. When mission type is combat
including `cap`, the tool MUST NOT return a Channel, Normandy, or Caucasus
combat skeleton.

#### Scenario: Syria free_flight schema uses Incirlik
- **WHEN** a caller requests the free_flight Spec schema with theatre
  `Syria`
- **THEN** the example MUST use `Incirlik`, `Su-25T`, and `Turkey`

#### Scenario: Syria combat schema has no Manston skeleton
- **WHEN** a caller requests a cap or intercept schema with theatre
  `Syria`
- **THEN** the result MUST NOT present a Manston, NeedsOarPoint, or Batumi
  example as the template to copy

### Requirement: Spec schema tool accepts Nevada
`get_mission_spec_schema` SHALL accept theatre `Nevada`. When mission type
is `free_flight`, the derived example MUST follow the Nellis envelope (not
Manston, NeedsOarPoint, Batumi, or Incirlik) and notes MUST NOT concatenate
Channel/Normandy/Caucasus/Syria template bundles. When mission type is combat
including `cap`, the tool MUST NOT return a prior-map combat skeleton.

#### Scenario: Nevada free_flight schema uses Nellis
- **WHEN** a caller requests the free_flight Spec schema with theatre
  `Nevada`
- **THEN** the example MUST use `Nellis`, `Su-25T`, and `USA`

#### Scenario: Nevada combat schema has no Manston skeleton
- **WHEN** a caller requests a cap or intercept schema with theatre
  `Nevada`
- **THEN** the result MUST NOT present a Manston, NeedsOarPoint, Batumi, or
  Incirlik example as the template to copy

### Requirement: Spec schema tool accepts Falklands
`get_mission_spec_schema` SHALL accept theatre `Falklands`. When mission type
is `free_flight`, the derived example MUST follow the Mount Pleasant envelope
(not Manston, NeedsOarPoint, Batumi, Incirlik, or Nellis) and notes MUST NOT
concatenate Channel/prior-map template bundles. When mission type is combat
including `cap`, the tool MUST NOT return a prior-map combat skeleton.

#### Scenario: Falklands free_flight schema uses MountPleasant
- **WHEN** a caller requests the free_flight Spec schema with theatre
  `Falklands`
- **THEN** the example MUST use `MountPleasant`, `Su-25T`, and `UK`

#### Scenario: Falklands combat schema has no Manston skeleton
- **WHEN** a caller requests a cap or intercept schema with theatre
  `Falklands`
- **THEN** the result MUST NOT present a Manston, NeedsOarPoint, Batumi,
  Incirlik, or Nellis example as the template to copy
