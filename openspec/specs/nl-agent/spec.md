# NL Agent

## Purpose

Natural-language planning that uses agent tools and emits a validated Mission Spec.
The LLM never writes DCS Lua or `.miz` contents; compilation stays deterministic.

## Requirements

### Requirement: Natural language planning entrypoint
The system SHALL accept a natural-language mission request via a Python API and a CLI
command and produce a Mission Spec YAML path (or structured failure). The agent MUST NOT
emit DCS mission Lua or write `.miz` contents directly; compilation MUST use the existing
compiler when requested. The plan CLI/API SHOULD accept an optional voice override that
selects the squadron-commander persona for that run.

#### Scenario: Plan writes a Spec file
- **WHEN** a user runs the plan command with a free-flight Manston-style prompt (stub or live)
- **THEN** the system MUST write a Mission Spec YAML that loads as `schema_version` `"1"`

#### Scenario: Compile remains deterministic
- **WHEN** planning is invoked with compile enabled
- **THEN** any `.miz` MUST be produced by the existing PyDCS compiler path, not by the LLM

#### Scenario: Out-of-period date warns but succeeds
- **WHEN** a planned Channel Spec uses a date year outside the usual WWII backdrop
  (about 1939–1945)
- **THEN** the plan MUST still succeed and MUST include a user-visible warning that the
  date does not match that historical backdrop, while noting other eras or modern dates
  remain allowed

#### Scenario: Period date has no realism warning
- **WHEN** a planned Channel Spec uses a date year in 1939–1945
- **THEN** the plan MUST NOT emit that Channel era/date mismatch warning

#### Scenario: Plan accepts voice override
- **WHEN** a user runs the plan command with an explicit `--voice usaaf` (or API equivalent)
- **THEN** the planner MUST resolve voice `usaaf` for that run’s system prompt

### Requirement: Tool-using agent loop
The planning agent SHALL be able to invoke the existing agent tools
(`find_airfield`, `get_aircraft_details`, `list_mission_options`, `validate_mission_spec`,
optionally `compile_mission`, the user-memory tools, and research guidance when available)
during planning. The agent MUST prefer tool results over invented DCS identifiers.

#### Scenario: Stub exercises tool bridge
- **WHEN** tests run the planner with a stub LLM configured to call `find_airfield`
- **THEN** the tool bridge MUST invoke the real `find_airfield` implementation and return its result to the loop

### Requirement: Planner consults user preferences
During natural-language planning, the agent SHALL be able to read user preferences via
the prefs tools (or equivalent host-provided prefs context). When the user leaves a
planning knob unspecified, the agent MUST prefer stored prefs over inventing a default,
without overriding an explicit user request.

#### Scenario: Stub can read prefs tool
- **WHEN** tests run the planner with a stub LLM configured to call `get_user_prefs`
- **THEN** the tool bridge MUST invoke the real prefs implementation and return its result
  to the loop

### Requirement: Planner records generation history
After a planning attempt reaches a terminal outcome (successful Spec write, or recorded
validation/compile failure), the system SHALL append a generation history row. Recording
MUST be performed by the host planner path and MUST NOT rely solely on the LLM choosing
to call `record_generation`.

#### Scenario: Successful stub plan writes history
- **WHEN** the planner succeeds in stub mode and writes a Spec
- **THEN** generation history MUST contain a success row referencing that Spec path

### Requirement: Planner applies squadron voice
The planning entrypoint SHALL resolve a squadron voice (CLI/API override, else
`squadron_voice` pref, else default `raf`) before the LLM loop and MUST use a system prompt
composed for that voice. Voice application MUST NOT change the requirement that the final
accepted Spec output is a validated Mission Spec (not DCS Lua).

#### Scenario: Stub plan uses composed voice prompt
- **WHEN** tests run the planner in stub mode with an explicit voice `usaaf`
- **THEN** the system prompt provided to the LLM MUST be the composed USAAF persona prompt
  (base rules + USAAF pack)

#### Scenario: Spec remains valid under voice
- **WHEN** a stub plan succeeds under voice `raf` or `usaaf`
- **THEN** the written Mission Spec MUST still validate under the shared validation engine

### Requirement: Planner surfaces commander brief
After a planning run successfully writes a validated Spec, the planner SHALL attach a
commander operational brief (summary, tactics, procedures, watch-outs) to the plan result
and the plan CLI MUST display it when present. The brief MUST be agent/CLI-side only in
this change (not compiled into `.miz` dictionary keys).

#### Scenario: Stub success includes brief sections
- **WHEN** a stub plan succeeds for a Manston free-flight style request
- **THEN** the plan result MUST include a brief containing tactics, procedures, and
  watch-outs content

### Requirement: Planner may research guidance
During planning (especially when preparing the commander brief), the agent SHALL be able
to invoke a research-guidance tool. Stub mode MUST exercise the tool bridge with offline
fixtures. Live mode MAY perform web-backed retrieval. Tool failure MUST NOT by itself mark
a validated Spec plan as failed.

#### Scenario: Stub can call research guidance tool
- **WHEN** tests run the planner with a stub LLM configured to call the research guidance tool
- **THEN** the tool bridge MUST invoke the real stub/offline implementation and return its
  result to the loop

### Requirement: Validate before accepting Spec
Before treating a planned Spec as successful output, the system SHALL validate it with the
shared validation engine. Invalid Specs MUST NOT be written as success without surfacing
errors (a single automated repair attempt after validation failure is allowed).

#### Scenario: Invalid Spec is not silently accepted
- **WHEN** the model proposes a Spec that fails validation
- **THEN** the planner MUST NOT report overall success without either a successful repair
  or a structured failure including validation errors

### Requirement: Offline stub for CI
The system SHALL provide a stub/fake LLM mode that requires no network and no API key so
CI and local tests can exercise the planner loop, YAML write, and validate/compile path.

#### Scenario: Stub plans Manston free flight
- **WHEN** the planner runs in stub mode for a Manston cold free-flight style request
- **THEN** it MUST produce a Spec that validates and can compile under test inventory

### Requirement: Live provider configuration
Live planning SHALL read API credentials and model settings from environment (or explicit
config), MUST NOT hard-code secrets, and MUST fail clearly when the key is missing for
non-stub runs.

#### Scenario: Missing API key in live mode
- **WHEN** live mode is requested without an API key configured
- **THEN** the system MUST fail with a clear error directing the user to set the key or use stub mode

### Requirement: Planner may emit CAP Specs
The NL planning rules SHALL allow Mission Spec `mission_type` `cap` with a nested `cap`
block (airfield-relative bearing/distance, altitude, pattern, engagement) and MUST NOT
instruct the model to invent raw map coordinates or unsupported mission types beyond the
allow-list. CAP Specs MUST still pass host validation before acceptance.

#### Scenario: Stub or documented allow-list includes cap
- **WHEN** planning rules / system prompt are composed for Channel MVP planning
- **THEN** `cap` MUST be listed among supported mission types alongside `free_flight` and
  `intercept`

### Requirement: Planner may emit ground-attack Specs
The NL planning rules SHALL allow Mission Spec `mission_type` `ground_attack` with a nested
`strike` block (airfield-relative bearing/distance, altitude), non-empty `targets`, named
`player.payload`, and `attack_ground` objective, and MUST NOT instruct the model to invent
raw map coordinates, CLSIDs, ground unit ids, or unsupported mission types beyond the
allow-list. Planning rules MUST require strike `targets` to be the opposing coalition to the
player (no friendly fire). For Channel-crossing ground-attack, planning guidance MUST prefer
a slipper-tank payload preset and MUST remind that the tank is jettisoned by the pilot
before the attack (not via invented Lua). Ground-attack Specs MUST still pass host
validation before acceptance.

#### Scenario: Stub or documented allow-list includes ground_attack
- **WHEN** planning rules / system prompt are composed for Channel MVP planning
- **THEN** `ground_attack` MUST be listed among supported mission types alongside
  `free_flight`, `intercept`, and `cap`

### Requirement: Escort in agent planning allow-list
Natural-language planning rules SHALL allow `mission_type: escort` and describe the
required `escort` block, friendly `package`, optional `enemies`, and `escort_package`
objective. The agent MUST NOT invent WGS84 coordinates or unregistered aircraft ids; package
destination MUST use airfield-relative bearing/distance.

#### Scenario: Escort mentioned in planning rules
- **WHEN** the planning system prompt / rules are built
- **THEN** they MUST include `escort` among supported mission types with package/destination
  guidance

### Requirement: Interactive chat coexists with one-shot plan
The NL agent layer SHALL support both a one-shot planning entrypoint and a multi-turn
interactive chat session. Interactive chat MUST reuse the same tool bridge, preference
consultation, squadron voice composition, validation-before-accept, and generation-history
recording contracts as one-shot planning when a Spec is accepted. Chat-specific REPL UX
is specified under the `plan-repl` capability.

#### Scenario: Shared tools available in chat
- **WHEN** an interactive chat session runs with the standard tool set enabled
- **THEN** registered planning tools (including catalog and prefs tools) MUST be
  dispatchable under the same bridge rules as one-shot planning

### Requirement: Derived Spec shape for planning prompts
The NL agent system prompt SHALL include a short always-on reminder of Mission Spec
anti-patterns (nested `player`, `date` as `{year,month,day}`, top-level `objectives`,
no flat `airfield`/`aircraft`) and MUST instruct the model to obtain the type-specific
example via `get_mission_spec_schema` (or an equivalent host-injected derived fragment)
before emitting Spec JSON. The prompt MUST NOT rely on a hand-maintained full CAP (or
other mission-type) JSON skeleton as the sole Spec shape authority.

#### Scenario: Composed prompt points at schema tool or derived shape
- **WHEN** the system prompt is composed for one-shot or chat planning
- **THEN** it MUST mention `get_mission_spec_schema` (or clearly state that the host
  provides the derived Spec example) and MUST include anti-pattern guidance for nested
  `player` and object `date`

### Requirement: Host repair uses derived Spec example
When the host rejects assistant Spec JSON during one-shot planning or chat, the repair
nudge MUST include a derived compact Spec example for the relevant `mission_type`
(inferred from the rejected JSON when present) rather than only a prose error string.

#### Scenario: Parse failure nudge includes example
- **WHEN** the model emits Spec-like JSON that fails Mission Spec validation
- **THEN** the next host repair message MUST include a derived example Spec (or
  equivalent fragment) for a supported mission type alongside the error

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

### Requirement: Spec shape reminder allows immersion triggers
The always-on Spec shape reminder injected into planning prompts MUST NOT require
`triggers` to be an empty list. It MUST state that `triggers` (and `zones` when needed)
may be populated for supported immersion behaviours, and that `[]` is used when unused.

#### Scenario: Reminder does not force empty triggers
- **WHEN** the Spec shape reminder text is composed into the system prompt
- **THEN** it MUST NOT contain the phrase that triggers must be empty, and MUST allow
  non-empty triggers for behaviours

### Requirement: Planner biases creative choices from memory
Planning and chat system guidance MUST instruct the agent, when inventing immersion on
vague asks, to consult generation history (and prefs when present) after listing
mission options, and to prefer behaviours that past feedback scored well while
soft-avoiding poorly scored ones — still emitting at most one or two supported
behaviours, never Lua, and never forcing narrative when hand triggers exist.

#### Scenario: Prompt mentions history bias for creativity
- **WHEN** the planning or chat system prompt is built
- **THEN** it MUST mention consulting generation history / feedback (or derived bias)
  when choosing mission_behaviour recipes on vague asks

### Requirement: Prompt states mutate/compile are host-owned
Planning system guidance MUST state that compiling `.miz` files, writing user prefs, and
recording generations/feedback are host/CLI responsibilities — not agent tool calls on the
default planning surface.

#### Scenario: Prompt mentions host-owned compile/prefs
- **WHEN** the planning system prompt is built
- **THEN** it MUST indicate that compile / preference writes / feedback recording are
  outside the default agent tool surface (host or CLI)

### Requirement: One-shot plan verbose defaults off
One-shot `plan` MUST default tool-trace / debug stderr output to off. Passing `--verbose`
MUST enable the same tracing used by interactive chat. The shared `DEFAULT_VERBOSE`
constant MUST be false.

#### Scenario: Default plan is quiet
- **WHEN** a user runs plan without `--verbose`
- **THEN** the planner MUST run with verbose off

#### Scenario: Plan --verbose enables traces
- **WHEN** a user runs plan with `--verbose`
- **THEN** LLM round / tool-call tracing MUST be enabled for that run

### Requirement: Immersion floor repair for vague invent
When one-shot planning (and chat draft capture when applicable) produces a Spec that
validates structurally but the user prompt cues immersion/challenge and the Spec lacks
matching packaged behaviours (e.g. empty triggers on an “interesting” free_flight, or
ground_attack without mark/smoke when the ask is about finding the target), the host
MUST inject at most one immersion repair nudge naming the expected behaviour recipe and
example Spec path before accepting the bare Spec. If the model still returns a bare Spec
after that nudge, the host MAY accept it (soft floor).

#### Scenario: Interesting free_flight bare Spec nudges once
- **WHEN** the user prompt suggests unspecified immersion (e.g. “interesting”) and the
  model returns a free_flight Spec with empty triggers
- **THEN** the host MUST inject an immersion repair message once before writing the Spec

#### Scenario: After nudge bare Spec may still accept
- **WHEN** the model returns another bare free_flight after the immersion nudge
- **THEN** the host MAY write the Spec (soft floor — not a hard validation failure)

### Requirement: Planner consults mission-designer shelves when co-authoring
Planning and interactive chat system guidance MUST instruct the agent to act as a
mission designer co-author: call `list_mission_options` for families `dynamics_mode`,
`strike_target_class`, and `channel_place` (in addition to existing behaviour/inspiration
consult) when the user discusses play-time variation, ground attack / strike composition,
or where on the Channel to fight. Guidance MUST require recommending only from those
shelves (and other packaged options), explaining tradeoffs before locking Spec fields.
Guidance MUST distinguish CLI/`randomize` (new Spec day) from Spec `dynamics` /
`dynamics_mode` (play-time Layer B). When the user locks play-time variation, the agent
SHOULD emit Spec `dynamics` (mode + pools). The agent MUST NOT invent unit/ship ids or
airdromeIds, and MUST NOT emit LLM Lua.

#### Scenario: Prompt guidance mentions designer shelves
- **WHEN** the planning or chat system prompt is built
- **THEN** it MUST include guidance to consult `dynamics_mode`, `strike_target_class`,
  and `channel_place` options when inventing or discussing dynamics, strike targets, or
  Channel places

#### Scenario: Prompt distinguishes randomize from dynamics palette
- **WHEN** guidance describes variation / replayability
- **THEN** it MUST distinguish seeded Spec reroll (`randomize`) from play-time
  `dynamics_mode` shelves

### Requirement: Schema and invent guidance mention dynamics Spec
`get_mission_spec_schema` notes and invent/chat guidance MUST mention optional Spec
`dynamics` (modes + pools) as the preferred way to declare play-time live/choose/hybrid
variation, distinct from CLI `randomize`. Guidance MUST still require co-author consult of
catalog `dynamics_mode` shelves and MUST NOT invent Lua.

#### Scenario: Prompt mentions dynamics Spec field
- **WHEN** the planning system prompt is built
- **THEN** it MUST mention Spec `dynamics` (or equivalent) for play-time variation

#### Scenario: Schema notes mention dynamics
- **WHEN** `get_mission_spec_schema` is requested for a combat mission type
- **THEN** notes MUST reference optional `dynamics` expand without claiming Mist

### Requirement: Agent schema includes player flight
The derived Mission Spec schema / invent reminders SHALL document optional
`player.flight` (`size`, `role`, `ai_skill`) so the agent can propose multi-ship sections
without inventing free-form skill or aircraft fields.

#### Scenario: Schema tool shows flight fields
- **WHEN** a client requests the Mission Spec shape for invent
- **THEN** the shape MUST include optional `player.flight` with size 2–4 and role
  lead/wingman

### Requirement: Schema notes join-up
Agent Spec schema notes SHALL document optional `player.flight.join_up` (default
true for wingman Follow/shared route).

#### Scenario: Schema mentions join_up
- **WHEN** requesting Spec shape for invent
- **THEN** notes or example guidance MUST mention `join_up`

### Requirement: Schema documents failures list
Agent Spec schema notes SHALL document optional `failures` (`id`, `start_after_s`,
`probability`, `random_pause_s`) and that ids must come from the catalog / tools.

#### Scenario: Schema mentions failures
- **WHEN** requesting Spec shape for invent
- **THEN** notes MUST mention optional `failures` and curated ids

### Requirement: Schema documents section orders
Agent Spec schema notes SHALL document optional `player.flight.orders` curated
ids and that free-form order strings are forbidden.

#### Scenario: Schema mentions orders
- **WHEN** requesting Spec shape for invent
- **THEN** notes MUST mention optional `player.flight.orders` and curated ids

### Requirement: Schema documents discipline
Agent Spec schema notes SHALL document optional `player.flight.discipline`
(radius, soft/hard timing, curated hard actions) and that it applies only to
wingman + join_up.

#### Scenario: Schema mentions discipline
- **WHEN** requesting Spec shape for invent
- **THEN** notes MUST mention optional `player.flight.discipline` and constraints

### Requirement: NL agent may invent recon Specs
The NL invent / planning path SHALL treat `recon` as a supported mission type and MUST NOT
emit `player.payload` or `attack_ground` for recon Specs.

#### Scenario: Recon invent shape
- **WHEN** the agent plans a Channel locate/observe sortie
- **THEN** it MAY emit `mission_type: recon` with a `recon` block and `recon_area`
  objective and MUST omit payload

### Requirement: NL agent may plan surfaced U-boat sorties
The NL invent path SHALL be allowed to emit `recon` or `ground_attack` Specs using
registry `Uboat_VIIC` on mid-Channel water geometry, and MUST NOT invent ASW mission
types, depth-charge payloads, or submerged-detection fields.

#### Scenario: Agent emits recon or GA for U-boat ask
- **WHEN** the pilot asks for a Channel U-boat locate or hunt
- **THEN** the agent MAY emit recon (locate) and/or ground_attack (hunt) Specs with
  `Uboat_VIIC` and MUST omit unsupported ASW fields

### Requirement: NL agent may set target motion
The invent path SHALL be allowed to emit `motion: patrol` or `motion: path` on
`targets[]` for GA and recon when place/class heuristics fit, and MUST prefer
omit/static for harbour and AAA. Paths MUST stay short (≤6 points). The agent
MUST NOT invent rail-mesh trains or ASW motion.

#### Scenario: Agent emits patrol for mid-Channel U-boat
- **WHEN** the pilot asks for a mid-Channel U-boat under way
- **THEN** the agent MAY emit recon or GA with `Uboat_VIIC` and `motion: patrol`

### Requirement: NL agent may set target AI presets
The invent path SHALL be allowed to emit curated `ai_preset` / allowlisted `ai`
and land `move_formation` on GA/recon targets per class heuristics (convoy
transit, AAA alert, ship under way), and MUST NOT invent free-form ME option
names or air-only options on ground/sea targets.

#### Scenario: Agent emits convoy transit style
- **WHEN** the pilot asks for a moving truck column inland
- **THEN** the agent MAY emit soft-vehicle targets with transit preset or
  allowlisted ai/move_formation fields

### Requirement: NL invent prefers catalog strike targets
The invent path SHALL be instructed to call `list_strike_targets` (or equivalent
catalog list) before inventing GA/recon `targets[]`, and MUST prefer returned
exact DCS ids rather than inventing unit strings.

#### Scenario: Schema or prompts mention list_strike_targets
- **WHEN** invent prompts or Spec schema notes for ground_attack/recon are loaded
- **THEN** they MUST mention querying strike targets from the catalog tool

### Requirement: Invent maps cues to unit motion and AI preset
The invent path SHALL instruct the agent to consult mission-option shelves and
`list_strike_targets` before emitting GA/recon `targets[]`, and SHALL document a
cue table: inland convoy → soft + path + `convoy_transit`; flak/AAA → aaa +
static + `aaa_alert`; mid-Channel U-boat under way → sea + patrol +
`ship_under_way`; harbour/dock → sea + static + `harbour_static`. The agent MUST
prefer tool-returned unit ids and allowlisted presets only.

#### Scenario: Prompts or schema include cue table
- **WHEN** invent prompts or ground_attack/recon Spec schema notes are loaded
- **THEN** they MUST mention the convoy / flak / U-boat / harbour cue mapping
  (or equivalent) and MUST NOT encourage free-form ME Opt* names
