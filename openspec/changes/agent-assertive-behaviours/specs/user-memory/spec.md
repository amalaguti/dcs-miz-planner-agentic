## MODIFIED Requirements

### Requirement: Generation detail may record creative choices
Generation history detail JSON MAY include a ``creative`` object with optional lists
``inspirations``, ``behaviours``, and ``sources`` (vocabulary:
catalog|campaign_doc|research|user_request|spec_infer). When hosts infer creative detail
from a Spec, ``radio_late_activation`` MUST be recorded only when the Spec has both
``late_activation`` on a referenced group and at least one ``activate_group`` action
(complete recipe). Late activation alone MUST NOT credit that behaviour id.

#### Scenario: Creative detail round-trips in generation history
- **WHEN** a generation is recorded with detail containing a creative object
- **THEN** listing that generation MUST return the creative fields intact in detail

#### Scenario: Infer requires complete late-act recipe
- **WHEN** ``infer_creative_from_spec`` sees ``late_activation`` without ``activate_group``
- **THEN** it MUST NOT include ``radio_late_activation`` in inferred behaviours
