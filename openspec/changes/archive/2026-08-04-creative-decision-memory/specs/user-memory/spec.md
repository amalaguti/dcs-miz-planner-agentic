## ADDED Requirements

### Requirement: Generation detail records creative decisions
When a mission generation succeeds (or is accepted) and the planner applied packaged
creative immersion, the generation history `detail` JSON SHOULD include a `creative`
object with `behaviours` (list of `mission_behaviour` ids) and MAY include
`inspirations` (list of `mission_inspiration` ids) and `sources` (e.g. catalog,
campaign_doc, research, user_request). Detail MUST remain valid JSON and MUST NOT
replace unrelated detail keys. Absence of `creative` MUST NOT break history readback.

#### Scenario: Successful generation can store creative detail
- **WHEN** a generation is recorded with detail containing `creative.behaviours`
- **THEN** a subsequent history list MUST return that detail including those behaviour ids

#### Scenario: Missing creative detail is allowed
- **WHEN** a generation is recorded without a `creative` key in detail
- **THEN** history readback MUST still succeed

### Requirement: Feedback informs creative taste
Satisfaction feedback linked to a generation MAY use tags or notes that name behaviour
ids (for example `liked:altitude_speed_gates` or `avoid:narrative_pack`). The system
MUST preserve such tags for later bias computation. Numeric score on the linked
generation remains the primary quality signal when present.

#### Scenario: Feedback tags persist
- **WHEN** feedback is recorded with tags referencing a behaviour id
- **THEN** those tags MUST be retrievable with the feedback row
