## ADDED Requirements

### Requirement: Invent land path near strike
The invent path SHALL instruct the agent to build land soft-vehicle `path`
points from channel_place path_point_deltas (or within a few km of strike),
preferring 2–3 points, and MUST NOT place land path waypoints at mid-Channel
distances. Domain-mismatch repair for path MUST include a concrete
Manston-relative path YAML example.

#### Scenario: Prompts mention path deltas and short paths
- **WHEN** invent prompts or GA Spec schema notes are loaded
- **THEN** they MUST mention path_point_deltas or strike-near path points and
  prefer 2–3 points for invent

#### Scenario: Path domain repair includes YAML example
- **WHEN** host_spec_repair_nudge is built for motion_domain_mismatch involving
  path
- **THEN** the nudge MUST include a concrete airfield-relative path bearing/
  distance example suitable for French-coast inland

### Requirement: Host clamps failing land paths once
When invent or chat validate fails with motion_domain_mismatch for a land-domain
target with path motion, the host MAY rewrite that target's path once from the
strike point plus french-coast path_point_deltas (or equivalent), then
re-validate. CLI validate of author Specs MUST NOT auto-clamp. Host MUST NOT
change unit ids or strike geometry in this clamp.

#### Scenario: Clamp rewrites bad land path then validates
- **WHEN** invent validate fails only because land path samples are off-domain
  and strike is on land
- **THEN** the host MAY replace path with strike-relative recipe points and
  accept if re-validation succeeds

### Requirement: Harbour invent prefers sea units
The invent path SHALL instruct harbour/dock asks to call list_strike_targets
with domain=sea, use coastal_harbour geometry, static motion, and
harbour_static — never soft land trucks. Host repair or harbour nudge MUST
mention sea-domain units when harbour cues conflict with land targets.

#### Scenario: Schema or prompts bind harbour to sea
- **WHEN** invent prompts or GA/recon schema notes are loaded
- **THEN** they MUST state harbour/dock → sea units + coastal_harbour + static
  + harbour_static
