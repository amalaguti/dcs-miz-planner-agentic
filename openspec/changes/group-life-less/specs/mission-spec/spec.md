## ADDED Requirements

### Requirement: Triggers may use group life less thresholds
When a Mission Spec includes a trigger condition `group_life_less`, it MUST identify the
affected group by Spec `enemy_index` or `target_index` and a remaining-life `percent`
threshold. The Spec MUST NOT carry raw DCS group ids for this condition.

#### Scenario: Index and percent fields
- **WHEN** a Spec declares `type: group_life_less` with exactly one index field and
  `percent` in 1–100
- **THEN** loading MUST succeed when the rest of the Spec is valid
