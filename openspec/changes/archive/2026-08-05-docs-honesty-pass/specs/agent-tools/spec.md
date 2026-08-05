## MODIFIED Requirements

### Requirement: List installed campaign missions for inspiration
The system SHALL expose an agent-callable tool (e.g. `list_installed_campaigns`) that
discovers the local DCS World install root (reuse existing install discovery) and lists
campaigns under `Mods/campaigns`, including campaign display name when available, mission
`.miz` filenames, short description text when obtainable from lightweight `.cmp`
metadata, and **filenames only** under each campaign’s `Doc/` folder when present
(typically briefing PDFs, intro, maps). The tool MUST NOT extract or return PDF body
text. Tool descriptions and host guidance MUST describe Doc entries as filenames/titles,
not as readable briefing themes or extracted content. The tool MUST be read-only, MUST NOT
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

#### Scenario: Doc entries are filenames only
- **WHEN** a campaign folder contains `Doc/*.pdf` files
- **THEN** the tool result MUST expose those PDF filenames and MUST NOT claim or return
  extracted PDF text or briefing-body themes
