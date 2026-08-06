## ADDED Requirements

### Requirement: Dynamics expand uses existing trigger actions only
Expanded dynamics graphs MUST use only already-supported Spec trigger conditions/actions
(`set_flag_random`, radio items, `activate_group`, `message`, flags, time). They MUST NOT
introduce new ME predicates in this change.

#### Scenario: Expanded graph validates as native triggers
- **WHEN** dynamics expand produces triggers
- **THEN** those triggers MUST pass the same trigger validation rules as hand-authored
  graphs
