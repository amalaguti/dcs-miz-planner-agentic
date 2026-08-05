## MODIFIED Requirements

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
