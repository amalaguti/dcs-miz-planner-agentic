## ADDED Requirements

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
