## ADDED Requirements

### Requirement: Chat repair nudge uses derived Spec schema
When interactive chat captures invalid Spec JSON, the host-injected repair nudge MUST
use the same derived Spec example source as the `get_mission_spec_schema` tool (or the
shared helper behind it), scoped to the rejected or draft `mission_type` when known.

#### Scenario: Invalid chat Spec injects derived example
- **WHEN** a chat turn includes Spec JSON that fails to load as Mission Spec
- **THEN** the session history MUST receive a host repair message that includes a
  derived example Spec fragment (not only the Pydantic error text)

#### Scenario: Draft still not written until accept
- **WHEN** chat receives invalid Spec JSON and injects a repair nudge
- **THEN** the host MUST still NOT write Spec YAML until a later successful `/accept`
