## ADDED Requirements

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
