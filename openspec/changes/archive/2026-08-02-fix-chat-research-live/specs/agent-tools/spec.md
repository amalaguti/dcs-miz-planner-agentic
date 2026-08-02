## MODIFIED Requirements

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
