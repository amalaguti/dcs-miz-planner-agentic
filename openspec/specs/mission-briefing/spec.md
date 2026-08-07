# Mission Briefing

## Purpose

Compile-time population of DCS `.miz` localisation dictionary briefing fields (Sortie,
Description, coalition Tasks) from Spec-driven squadron-commander brief content.

## Requirements

### Requirement: Compile writes DCS briefing dictionary text
The compiler SHALL, on every successful Mission Spec compile, populate the mission
localisation dictionary with non-empty Sortie and Description strings derived from the
Spec and the squadron-commander briefing builder. The player coalition Task string MUST
also be non-empty. The opposing coalition Task MAY be empty. Briefing text MUST be plain
text suitable for the DCS Mission Editor briefing panel (no markdown heading markers).
The compiler MUST use PyDCS briefing setters (or equivalent) and MUST NOT invent DCS
identifiers or emit LLM-authored Lua.

#### Scenario: Free-flight compile fills dictionary
- **WHEN** the checked-in Manston cold free-flight Spec is compiled with default voice
- **THEN** the output `.miz` MUST contain `l10n/DEFAULT/dictionary` (or equivalent) whose
  Sortie equals the Spec `name`, Description is non-empty, and the player-coalition Task
  is non-empty

#### Scenario: Combat types fill player task
- **WHEN** a checked-in intercept, CAP, ground-attack, or escort example Spec is compiled
- **THEN** the player-coalition Task text MUST be non-empty and MUST reflect that mission
  type’s commander brief content (tactics/procedures material), and Sortie MUST equal the
  Spec `name`

### Requirement: Briefing text reuses commander brief and voice
Mission briefing dictionary text SHALL be produced by splitting the same Spec-driven
commander operational brief used for CLI/`PlanResult` display (Situation, Tactics,
Procedures, Watch-outs), under a resolved squadron voice (`raf`, `usaaf`, or `neutral`).
Compile MUST accept an optional voice override; when omitted, the compiler MUST use the
default squadron voice `raf` (callers MAY resolve prefs before invoking compile). Spec
fields MUST remain free of briefing prose requirements beyond existing `name` /
`description`.

#### Scenario: Voice override changes register
- **WHEN** the same Spec is compiled once with voice `raf` and once with voice `usaaf`
- **THEN** the Description or Task strings MUST differ in register/wording consistent with
  those voice packs, while Sortie remains the Spec `name`

#### Scenario: Spec description feeds Description field
- **WHEN** a Spec with a non-empty `description` is compiled
- **THEN** the Description dictionary string MUST include that Spec description content
  (in addition to situation/watch-out material as designed)

### Requirement: Briefing covered by regression tests
The test suite SHALL assert that compiled example `.miz` files include non-empty briefing
dictionary content. Golden-fixture refresh for Manston examples MUST capture the
dictionary member (or equivalent contracted briefing asserts) so silent empty briefings
fail CI.

#### Scenario: Golden or contract fails on empty briefing
- **WHEN** a compile under the golden/briefing harness produces empty Sortie or empty
  player Task
- **THEN** the test MUST fail

### Requirement: Brief mentions player flight when present
When `player.flight` is present, generated briefing / squadron-voice text SHALL mention
the section size and whether the human flies as lead or wingman, in voice-appropriate
language. Solo Specs (no `player.flight`) MUST keep existing brief behaviour.

#### Scenario: Four-ship lead brief
- **WHEN** briefing a Spec with `player.flight.size: 4` and `role: lead`
- **THEN** Sortie/Description or Task text MUST indicate a four-ship section led by the
  player (wording may vary by voice)

### Requirement: Brief mentions join-up for wingman
When wingman + join_up, briefing/voice SHALL mention joining / following the AI
section lead after takeoff (wording may vary by voice).

#### Scenario: Wingman join brief
- **WHEN** briefing a wingman Spec with join-up enabled
- **THEN** Situation or Procedures MUST indicate join-up / follow the lead

### Requirement: Brief honesty when failures armed
When `failures` is non-empty, generated briefing/voice text SHALL mention that
system failures may occur (training / keep-honest wording). Solo Specs without
failures MUST keep prior brief behaviour.

#### Scenario: Failures brief note
- **WHEN** briefing a Spec with at least one failure entry
- **THEN** Situation or Watch-outs MUST indicate possible aircraft system failures

### Requirement: Brief mentions section orders when armed
When `player.flight.orders` is non-empty, generated briefing/voice text SHALL
mention that F10 (or section) orders are available. Specs without orders MUST
keep prior brief behaviour for this topic.

#### Scenario: Orders brief note
- **WHEN** briefing a Spec with at least one section order
- **THEN** Procedures or Watch-outs MUST indicate available section orders

### Requirement: Briefing includes synthetic METAR from weather snapshot
When building mission briefing dictionary text, the shared commander-brief path
SHALL include one synthetic ICAO-style METAR line derived from the invent
`WeatherSnapshot` for the Spec (winds, visibility, cloud groups from packaged
gallery decode, temperature, altimeter) plus Spec date/time. The line MUST use a
fixed Channel station id suitable for Manston-centred sorties (e.g. `EGMH`), MUST
be deterministic for the same Spec + seed, MUST NOT call any network meteo API,
and MUST be marked as simulated (e.g. `NOSIG` and a `RMK SIM` or equivalent remark)
so it is not mistaken for a live observation. Legacy density patterns without a
gallery id MUST still produce a valid METAR-looking line (e.g. `CLR` clouds).

#### Scenario: Gallery pattern brief contains METAR
- **WHEN** a Spec with a gallery weather pattern and pinned `weather_opts.seed` is
  briefed for compile
- **THEN** Description or Task text MUST contain a single-line METAR including the
  fixed station id, a `Z` timestamp group, and `NOSIG`

#### Scenario: Same seed same METAR
- **WHEN** the commander brief / METAR builder runs twice for the same Spec and seed
- **THEN** the synthetic METAR line MUST be identical

#### Scenario: No network for METAR
- **WHEN** synthetic METAR is generated during brief or compile
- **THEN** the implementation MUST NOT fetch aviationweather, CheckWX, Open-Meteo,
  or any other live meteo endpoint
