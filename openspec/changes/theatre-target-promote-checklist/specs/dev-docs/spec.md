## ADDED Requirements

### Requirement: Theatre and target promote checklist
The repository SHALL include a checked-in promote checklist document that covers
adding a new theatre/map slice and expanding strike/recon target shelves via
curated registry YAML (not ME scrape). The document MUST state explicit
non-goals: no full ME unit-tree scrape and no auto-promotion from install
discovery into known YAML.

#### Scenario: Checklist document present
- **WHEN** a developer or agent opens the Docs set
- **THEN** `docs/THEATRE_TARGET_PROMOTE.md` (or an equivalent path linked from
  README Docs) MUST be present

#### Scenario: Theatre and unit sections exist
- **WHEN** a reader opens the promote checklist
- **THEN** it MUST include a new-theatre section and a new-target-units section
  with ordered steps through research, registry/YAML, catalog sync, invent
  coherence, accept, and docs
