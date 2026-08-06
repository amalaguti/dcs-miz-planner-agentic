## ADDED Requirements

### Requirement: Dynamics mode options reflect Spec-backed expand
After dynamics expand ships, packaged `dynamics_mode` planning options MUST be marked so
agents do not treat them as emit-deferred-only: prefer `supported` (or `advisory` with
`meta` pointing at Spec `dynamics.mode`) consistently with other Spec-backed knobs.

#### Scenario: Catalog lists dynamics modes after sync
- **WHEN** catalog sync runs after this change
- **THEN** `dynamics_mode` rows MUST remain listable and describe Spec `dynamics.mode`
  values `fixed`, `live`, `choose`, `hybrid`
