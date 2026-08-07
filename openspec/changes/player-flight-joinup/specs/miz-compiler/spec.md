## ADDED Requirements

### Requirement: Wingman join-up Follow and shared route
When `player.flight.role` is `wingman` and `join_up` is enabled, the compiler SHALL
(1) place mission route/tasking (CAP / ground-attack / escort, and a minimal
free-flight outbound leg for free_flight) on the **AI lead** group, and (2) add a
native ME **Follow** task on the **player** group targeting that AI lead group id
(PyDCS `Follow`). The player group MUST remain size-1 with skill `Player`. When
`join_up` is false, behaviour MUST match `#15b` (tasks on player group, no Follow).
`role: lead` multi-unit groups MUST NOT require Follow for cohesion.

#### Scenario: Wingman free-flight Follow
- **WHEN** compiling a free-flight Spec with wingman + join_up
- **THEN** the `.miz` MUST contain a Follow action referencing the AI lead group and
  an outbound waypoint on the AI lead group

#### Scenario: Wingman CAP tasking on lead
- **WHEN** compiling a CAP Spec with wingman + join_up
- **THEN** CAP orbit/route tasking MUST be on the AI lead group and the player group
  MUST Follow that lead

#### Scenario: Join-up opt-out
- **WHEN** compiling wingman with `join_up: false`
- **THEN** the player group MUST NOT have a Follow-to-lead task from this feature
