## ADDED Requirements

### Requirement: Geometry randomization preserves ground-attack strike domain
When the geometry axis jitters a ground-attack `strike` block, randomization MUST NOT
leave the Spec with a strike point domain that mismatches the Spec’s target unit domains.
Implementations MAY redraw jitter until compatible or retain the pre-jitter strike.

#### Scenario: GA geometry randomize keeps domain
- **WHEN** a valid ground-attack Spec is randomized with the geometry axis
- **THEN** the result MUST still pass strike-domain validation
