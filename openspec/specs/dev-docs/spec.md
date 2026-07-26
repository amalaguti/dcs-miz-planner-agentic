# Dev Docs

## Purpose

Developer-facing orientation for the mission planner package: where modules live,
how they relate on the Spec → `.miz` path, and how to keep that map current.

## Requirements

### Requirement: Architecture module map document
The repository SHALL include a checked-in architecture document that describes the mission planner’s development modules and their relationships for contributors and agents.

#### Scenario: Document present
- **WHEN** a developer clones the repository
- **THEN** `docs/ARCHITECTURE.md` (or an equivalent path linked from README Docs) MUST be present

### Requirement: Runtime relationship diagram
The architecture document SHALL include a diagram (Mermaid or ASCII) of the free-flight compile path showing how CLI, Mission Spec loading/models, reference data, compiler interface, and PyDCS-backed compiler relate, ending at a `.miz` output.

#### Scenario: Spec-to-miz path is visible
- **WHEN** a reader opens the architecture document
- **THEN** they MUST be able to follow Mission Spec YAML → validated Spec → compiler → `.miz` without reading the full concept essay

### Requirement: Repo layout orientation
The architecture document SHALL briefly locate supporting areas (`openspec/`, `.cursor/`, `examples/`, `tests/`, and that `research/` is local/gitignored) so developers know where planning vs product code live.

#### Scenario: OpenSpec vs product code
- **WHEN** a reader opens the architecture document
- **THEN** it MUST distinguish product code under `src/` from OpenSpec change/specs workflow and Cursor agent tooling

### Requirement: Refresh guidance
The project SHALL document how and when to update the architecture map (at minimum: when public package layout or the Spec→`.miz` flow changes), and SHALL provide a lightweight reminder on `git push` when `src/dcs_miz_planner/` changes are being pushed.

#### Scenario: Push reminder when package changes
- **WHEN** an agent is about to `git push` commits that touch `src/dcs_miz_planner/`
- **THEN** a Cursor hook MUST remind them to verify `docs/ARCHITECTURE.md` still matches reality (non-blocking allow, same pattern as README reminder)
