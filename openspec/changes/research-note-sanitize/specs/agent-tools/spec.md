## ADDED Requirements

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
