## ADDED Requirements

### Requirement: Agent tools aware of recon
Agent-facing tools and derived Spec schema SHALL allow `mission_type` `recon` and document
the nested `recon` block, `recon_area` objective, no-payload rule, and optional observe-only
contacts.

#### Scenario: Schema mentions recon
- **WHEN** `get_mission_spec_schema` (or equivalent) is asked for recon / general shape
- **THEN** the result MUST describe recon fields and forbid payload on recon
