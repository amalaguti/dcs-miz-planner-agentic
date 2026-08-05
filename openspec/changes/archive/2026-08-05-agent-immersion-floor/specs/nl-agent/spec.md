## ADDED Requirements

### Requirement: Immersion floor repair for vague invent
When one-shot planning (and chat draft capture when applicable) produces a Spec that
validates structurally but the user prompt cues immersion/challenge and the Spec lacks
matching packaged behaviours (e.g. empty triggers on an “interesting” free_flight, or
ground_attack without mark/smoke when the ask is about finding the target), the host
MUST inject at most one immersion repair nudge naming the expected behaviour recipe and
example Spec path before accepting the bare Spec. If the model still returns a bare Spec
after that nudge, the host MAY accept it (soft floor).

#### Scenario: Interesting free_flight bare Spec nudges once
- **WHEN** the user prompt suggests unspecified immersion (e.g. “interesting”) and the
  model returns a free_flight Spec with empty triggers
- **THEN** the host MUST inject an immersion repair message once before writing the Spec

#### Scenario: After nudge bare Spec may still accept
- **WHEN** the model returns another bare free_flight after the immersion nudge
- **THEN** the host MAY write the Spec (soft floor — not a hard validation failure)
