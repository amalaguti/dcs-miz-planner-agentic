## ADDED Requirements

### Requirement: Escort in agent planning allow-list
Natural-language planning rules SHALL allow `mission_type: escort` and describe the
required `escort` block, friendly `package`, optional `enemies`, and `escort_package`
objective. The agent MUST NOT invent WGS84 coordinates or unregistered aircraft ids; package
destination MUST use airfield-relative bearing/distance.

#### Scenario: Escort mentioned in planning rules
- **WHEN** the planning system prompt / rules are built
- **THEN** they MUST include `escort` among supported mission types with package/destination
  guidance
