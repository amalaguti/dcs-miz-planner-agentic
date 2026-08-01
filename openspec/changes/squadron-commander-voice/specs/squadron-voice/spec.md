# Squadron Voice

## Purpose

Selectable squadron-commander persona for agent communication with pilots: RAF or USAAF
period register (jargon and slang guidance), or neutral planner tone — plus operational
commander briefs (tactics, procedures, watch-outs) optionally enriched by research.

## ADDED Requirements

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
After a successful plan that writes a validated Spec, the system SHALL attach a commander
brief suitable for CLI display. The brief MUST include, at minimum, sections covering
sortie/situation summary, tactics recommendations for the mission type and plan, procedure
recommendations, and watch-outs / things to observe for successful execution. When a
non-neutral voice is selected, the brief SHOULD use that commander register. The brief
MUST NOT replace validation or Spec content and MUST NOT be written into `.miz` `l10n` by
this capability.

#### Scenario: Successful stub plan exposes a structured brief
- **WHEN** a stub plan succeeds with voice `raf` for a free-flight or intercept style request
- **THEN** the plan result MUST include a non-empty brief string that contains identifiable
  tactics, procedures, and watch-outs content suitable for CLI display

#### Scenario: Brief does not alter Spec machine fields
- **WHEN** a plan succeeds and a brief is attached
- **THEN** the written Mission Spec MUST still use plain canonical field values and MUST
  pass the shared validation engine

### Requirement: Optional guidance research
The system SHALL provide a research capability the planning agent can invoke to gather
short guidance notes on flight procedures, combat manoeuvres, pilot accounts, or
historical context relevant to the mission. Live mode MAY use web-backed retrieval. Stub
or offline mode MUST return fixture notes without network access. Research failures MUST
NOT fail an otherwise successful Spec plan. Research results MUST NOT be treated as a
source of DCS type ids or Spec field authority.

#### Scenario: Stub research returns offline notes
- **WHEN** the research capability is invoked in stub/offline mode for an intercept-oriented
  query
- **THEN** it MUST return non-empty guidance notes without requiring network access

#### Scenario: Research failure soft-fails
- **WHEN** live research fails (timeout or provider error) after a Spec has already validated
- **THEN** the plan MUST still be able to succeed and MUST still be allowed to produce a
  brief without research notes
