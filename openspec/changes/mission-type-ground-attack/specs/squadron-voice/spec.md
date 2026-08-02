## MODIFIED Requirements

### Requirement: Commander operational brief
After a successful plan that yields an accepted Mission Spec, the planner host SHALL attach
a commander operational brief suitable for CLI display. The brief MUST include, at minimum,
sections covering Situation/sortie, Tactics, Procedures, and Watch-outs appropriate to the
mission type (including CAP when `mission_type` is `cap`, and ground-attack when
`mission_type` is `ground_attack`). When a non-neutral voice is selected, the brief SHOULD
use that commander register. The brief MUST NOT replace validation or Spec content and MUST
NOT be written into `.miz` `l10n` by this capability.

#### Scenario: Successful stub plan exposes a structured brief
- **WHEN** a stub plan succeeds with voice `raf` for a free-flight, intercept, CAP, or
  ground-attack style request
- **THEN** the plan result MUST include a non-empty brief string that contains identifiable
  Situation/Tactics/Procedures/Watch-outs section markers (or equivalent labelled sections)

#### Scenario: Ground-attack brief mentions fuel tank when relevant
- **WHEN** a stub or live plan succeeds for a ground-attack Spec whose payload includes a
  slipper tank (or the brief is built for Channel-crossing ground-attack guidance)
- **THEN** the brief MUST mention external fuel / slipper tank and jettison-before-attack
  procedure in Procedures or Watch-outs (or equivalent labelled sections)

#### Scenario: Brief is not Spec JSON
- **WHEN** a plan succeeds and a brief is attached
- **THEN** the accepted Mission Spec fields MUST remain plain structured values without
  embedding the briefing prose into Spec enums or ids
