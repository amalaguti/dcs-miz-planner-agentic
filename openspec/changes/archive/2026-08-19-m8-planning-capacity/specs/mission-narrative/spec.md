## MODIFIED Requirements

### Requirement: Opt-in narrative expands to typed triggers
When `enabled` is true for `mission_type: recon`, expansion MUST defer the zone
graph to the recon find-beat expander so one AOI zone remains.

#### Scenario: Recon narrative defers to find beat
- **WHEN** a valid recon Spec has `narrative.enabled: true` and empty zones/triggers
- **THEN** recon expand MUST prepend a narrative push message and then inject the AOI
  find beat, and MUST clear `narrative.enabled` after expand
