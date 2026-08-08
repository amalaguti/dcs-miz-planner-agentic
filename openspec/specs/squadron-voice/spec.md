# Squadron Voice

## Purpose

Selectable squadron-commander persona for agent communication with pilots: RAF or USAAF
period register (jargon and slang guidance), or neutral planner tone — plus operational
commander briefs (tactics, procedures, watch-outs) optionally enriched by research.

## Requirements

### Requirement: Voice identifiers
The system SHALL support squadron voice identifiers `raf`, `usaaf`, and `neutral`. Voice
selection inputs MAY accept common aliases and MUST normalize to one of those identifiers.
Unrecognized values MUST fall back to the default voice without failing planning.

#### Scenario: Alias normalizes to raf
- **WHEN** the selected voice input is `RAF` or `raf`
- **THEN** the resolved voice MUST be `raf`

#### Scenario: Unknown voice falls back
- **WHEN** the selected voice input is not a known id or alias
- **THEN** the system MUST resolve to the default voice and MUST NOT fail the plan solely
  for that reason

### Requirement: Default and resolution order
The default squadron voice SHALL be `raf`. When resolving voice for a planning run, the
system MUST prefer an explicit CLI/API override when provided, otherwise a stored
`squadron_voice` preference when set, otherwise the default.

#### Scenario: CLI overrides pref
- **WHEN** the user pref is `usaaf` and the plan invocation passes voice `raf`
- **THEN** the resolved voice MUST be `raf`

#### Scenario: Pref used when no CLI override
- **WHEN** no CLI/API voice override is provided and the user pref `squadron_voice` is `usaaf`
- **THEN** the resolved voice MUST be `usaaf`

### Requirement: Persona packs and prompt composition
The system SHALL provide curated persona packs for `raf` and `usaaf` that instruct the
agent to address the user as a squadron commander speaking to pilots, using appropriate
period jargon and slang guidance, and a `neutral` mode that omits commander persona
overlay. The planning system prompt MUST be composed from base planning rules plus the
selected pack, and MUST instruct the agent to provide operational guidance appropriate to
the mission type and plan. Mission Spec field names and machine values MUST remain plain
(no slang required inside Spec JSON/YAML).

#### Scenario: RAF prompt includes commander framing
- **WHEN** the system composes a prompt for voice `raf`
- **THEN** the prompt MUST include RAF squadron-commander persona guidance and MUST still
  include the base planning rules (Channel, tools, no Lua)

#### Scenario: Neutral omits commander persona
- **WHEN** the system composes a prompt for voice `neutral`
- **THEN** the prompt MUST include base planning rules and MUST NOT require RAF or USAAF
  commander persona overlay

### Requirement: Commander operational brief
After a successful plan that yields an accepted Mission Spec, the planner host SHALL attach
a commander operational brief suitable for CLI display. The brief MUST include, at minimum,
sections covering Situation/sortie, Tactics, Procedures, and Watch-outs appropriate to the
mission type (including CAP when `mission_type` is `cap`, ground-attack when
`mission_type` is `ground_attack`, and escort when `mission_type` is `escort`). When a
non-neutral voice is selected, the brief SHOULD use that commander register. The brief
MUST NOT replace validation or Spec content. Writing briefing text into `.miz` `l10n` is
owned by the `mission-briefing` / compiler path, which MUST reuse this same brief builder;
the squadron-voice host layer itself is not required to perform that write.

#### Scenario: Successful stub plan exposes a structured brief
- **WHEN** a stub plan succeeds with voice `raf` for a free-flight, intercept, CAP, or
  ground-attack style request
- **THEN** the plan result MUST include a non-empty brief string that contains identifiable
  Situation/Tactics/Procedures/Watch-outs section markers (or equivalent labelled sections)

#### Scenario: Ground-attack brief mentions fuel tank when relevant
- **WHEN** a stub or live plan succeeds for a ground-attack Spec whose payload includes a
  slipper tank (or the brief is built for Channel-crossing ground-attack guidance)
- **THEN** the brief MUST mention external fuel / slipper tank and jettison-before-attack
  procedure in Procedures or Watch-outs (or equivalent labelled sections)

#### Scenario: Brief is not Spec JSON
- **WHEN** a plan succeeds and a brief is attached
- **THEN** the accepted Mission Spec fields MUST remain plain structured values without
  embedding the briefing prose into Spec enums or ids

### Requirement: Optional guidance research
The system SHALL provide a research capability the planning agent can invoke to gather
short guidance notes on flight procedures, combat manoeuvres, pilot accounts, or
historical context relevant to the mission. Live mode MUST attempt web-backed retrieval
when enabled. Stub or offline mode MUST return fixture notes without network access. When
live research fails or returns no snippets, the system MUST soft-fail with a clear warning
and MAY fall back to fixtures; it MUST NOT present that fallback as successful live
retrieval. Research failures MUST NOT fail an otherwise successful Spec plan. Research
results MUST NOT be treated as a source of DCS type ids or Spec field authority.

#### Scenario: Stub research returns offline notes
- **WHEN** the research capability is invoked in stub/offline mode for an intercept-oriented
  query
- **THEN** it MUST return non-empty guidance notes without requiring network access

#### Scenario: Research failure soft-fails
- **WHEN** live research fails (timeout or provider error) after a Spec has already validated
- **THEN** the plan MUST still be able to succeed and MUST still be allowed to produce a
  brief without depending on live research notes

#### Scenario: Live research warning is visible to the agent path
- **WHEN** live research is requested and returns no usable live snippets
- **THEN** the research result MUST include a warning suitable for tool/CLI display stating
  that live research was unavailable

### Requirement: Escort commander brief notes
When squadron-commander voice is enabled and the planned Spec is escort, the commander brief
SHALL include escort-specific tactics, procedures, and watch-outs (stay with the package,
engagement posture, bounce awareness). Host/CLI briefs remain display output; `.miz` `l10n`
population is performed at compile time via the shared brief builder (`mission-briefing`).

#### Scenario: Escort brief branch
- **WHEN** `build_commander_brief` is invoked for a valid escort Spec with voice enabled
- **THEN** the brief MUST include escort-oriented tactics/procedures/watch-outs

### Requirement: Voice aware of player flight
Squadron-commander voice helpers SHALL accept Spec `player.flight` context so brief
phrases can refer to section size and lead/wingman role without inventing aircraft or
skill ids.

#### Scenario: Wingman phrasing available
- **WHEN** voice brief generation runs for a Spec with `role: wingman`
- **THEN** the generated copy MUST be able to state the player flies as wingman in the
  section (not as solo)

### Requirement: Commander brief includes synthetic METAR
The host-side commander operational brief SHALL include the same synthetic
METAR line required by mission-briefing (from invent `WeatherSnapshot`, offline,
deterministic, simulated remark). Spec field values MUST remain free of
METAR prose.

#### Scenario: CLI brief shows METAR
- **WHEN** `build_commander_brief` runs for a valid Spec with weather set
- **THEN** the brief string MUST include the synthetic METAR line with station id
  and `NOSIG` (or equivalent simulated marker)

### Requirement: Commander brief mentions recon observe discipline
When briefing a recon Spec, squadron-commander voice SHALL mention the AOI / observe task
and that the sortie is locate-and-report (RTB after observe), not a bomb run.

#### Scenario: Recon brief language
- **WHEN** a commander brief is generated for a recon Spec
- **THEN** the text MUST indicate observe / recon (not ground-attack jettison/bomb language)

### Requirement: Commander brief mentions surfaced U-boat discipline
When briefing a Spec whose targets/contacts include `Uboat_VIIC` (recon or ground_attack),
squadron-commander voice SHALL mention that the boat is to be observed or attacked
**while surfaced** and MUST NOT instruct depth-charge / submerged ASW procedures.

#### Scenario: U-boat brief language
- **WHEN** a commander brief is generated for a Spec with `Uboat_VIIC` targets or contacts
- **THEN** the text MUST indicate surfaced observe/attack (and MUST NOT claim depth charges)

### Requirement: Brief mentions contacts under way when moving
When a Spec has one or more non-static `targets[]` motion values, squadron-commander
voice SHOULD mention that contacts are under way / on the move (while keeping
surfaced-only U-boat language when `Uboat_VIIC` is present). Static-only Specs
MUST NOT claim movement.

#### Scenario: Moving U-boat brief
- **WHEN** a commander brief is generated for a Spec with `Uboat_VIIC` and patrol/path
- **THEN** the text MUST indicate the contact is under way (and MUST NOT claim ASW)
