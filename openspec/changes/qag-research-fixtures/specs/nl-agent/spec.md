## ADDED Requirements

### Requirement: QAG research fixtures are colour only
Planning and interactive chat system guidance MUST treat `research_guidance`
notes sourced from local QAG HTML research files as mission-design and historical
colour only. The agent MUST NOT copy QAG UI labels, site template names, or
internal `template.lua` strings into Spec fields (`unit_id`, aircraft ids,
country ids, `mission_type`). The agent MUST NOT invent Spec types from QAG
generator families (Dogfight, Bomber Escort, Bomber Intercept, Anti-Ship SR,
SEAD SR). QAG Cold War 1947–1970 material MUST NOT be treated as a Spec era
package.

#### Scenario: Prompt forbids QAG labels as Spec ids
- **WHEN** the planning or chat system prompt is built
- **THEN** it MUST state that QAG / research fixture labels are not Spec or
  PyDCS identifiers and MUST NOT be copied into Spec fields

#### Scenario: Prompt forbids QAG generator types as Spec types
- **WHEN** the planning or chat system prompt mentions research or mission-design
  focus
- **THEN** it MUST retain that unsupported Spec types (including SEAD and
  anti-ship as first-class types) MUST NOT be invented from research notes
