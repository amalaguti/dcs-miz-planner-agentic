## ADDED Requirements

### Requirement: Schema example follows extra-home airfield
`build_spec_schema` / invent schema SHALL accept an optional player airfield.
When theatre is TheChannel and airfield is omitted or Manston, the derived
example MUST remain the Manston immersion-first envelope. When airfield is
Hawkinge and mission type is free_flight or cap, the example MUST use packaged
Hawkinge YAML (`player.airfield` Hawkinge; CAP station MUST NOT be Manston
135/25). When airfield is another Channel extra home (Detling, BigginHill) or
a Normandy extra home (Chailey, Tangmere, FordAF), the example MUST set that
airfield and copy `cap_*` / `strike_*` / `escort_*` from the matching
`channel_place` `*_home` meta rather than Manston 135/25, 125/76, 120/55 or
NeedsOarPoint 180/63, 180/133. Place-card meta is the geometry source of truth.

#### Scenario: Hawkinge CAP schema is not Manston 135/25
- **WHEN** a caller requests the cap Spec schema with theatre TheChannel and
  airfield Hawkinge
- **THEN** the example MUST use `player.airfield` Hawkinge and CAP bearing/
  distance MUST be the hawkinge_home values (76/32), not 135/25

#### Scenario: Detling CAP schema rewrites from place card
- **WHEN** a caller requests the cap Spec schema with theatre TheChannel and
  airfield Detling
- **THEN** the example MUST use `player.airfield` Detling and CAP geometry
  from detling_home meta, not Manston 135/25

#### Scenario: Chailey CAP schema is not NeedsOarPoint 180/63
- **WHEN** a caller requests the cap Spec schema with theatre Normandy and
  airfield Chailey
- **THEN** the example MUST use `player.airfield` Chailey and CAP geometry
  from chailey_home meta, not 180/63

#### Scenario: Manston default schema unchanged
- **WHEN** a caller requests the cap Spec schema with theatre TheChannel and
  no airfield (or airfield Manston)
- **THEN** the example MUST remain the Manston envelope (CAP 135/25)

### Requirement: Host repair infers extra-home airfield
When the host rejects assistant Spec JSON, repair MUST infer `player.airfield`
from the rejected payload when present and MUST pass that airfield into
`build_spec_schema` so an extra-home draft is not repaired with the default
home example.

#### Scenario: Hawkinge parse failure is not repaired with Manston JSON
- **WHEN** host_spec_repair_nudge is built for rejected JSON whose
  `player.airfield` is Hawkinge
- **THEN** the derived example fragment MUST use Hawkinge, not Manston

### Requirement: Host clamps extra-home cloned default stations
When invent or chat produces a Spec whose `player.airfield` is a Channel or
Normandy extra home and CAP, escort destination, strike, or recon AOI matches
the theatre default-home station (TheChannel Manston 135/25, 125/76, 120/55;
Normandy NeedsOarPoint 180/63, 180/133), the host SHALL rewrite those fields
from the matching `*_home` place-card meta, then re-validate. CLI validate of
author Specs MUST NOT auto-clamp. The host MUST NOT rewrite when the ask names
a place (French coast, harbour, mid-Channel) rather than a home CAP, and MUST
NOT change land-path clamp behaviour. Intercept Specs have no station fields;
this clamp MUST NOT invent intercept spawn geometry.

#### Scenario: Hawkinge CAP cloned 135/25 is rewritten to 76/32
- **WHEN** invent/chat validates a TheChannel CAP with airfield Hawkinge and
  cap 135/25
- **THEN** the host MUST rewrite cap to hawkinge_home 76/32 and accept if
  re-validation succeeds

#### Scenario: Chailey CAP cloned 180/63 is rewritten
- **WHEN** invent/chat validates a Normandy CAP with airfield Chailey and
  cap 180/63
- **THEN** the host MUST rewrite cap from chailey_home meta

#### Scenario: Manston 135/25 is not clamped
- **WHEN** invent/chat validates a TheChannel CAP with airfield Manston and
  cap 135/25
- **THEN** the host MUST NOT rewrite cap geometry

#### Scenario: Named French-coast strike from Hawkinge is not clamped
- **WHEN** the user ask names a French-coast or harbour place and the Spec
  strike uses that place recipe from Hawkinge
- **THEN** the host MUST NOT rewrite strike onto hawkinge_home strike_*

### Requirement: Host nudges M8 knobs when the ask implies them
Invent/chat SHALL apply a one-shot host nudge (not a compiler rebuild) when
the ask implies an M8 card and the draft omits it: Mustang/P-51 → `P-51D`
country USA (GA payload `p51d_2x_anm64`); artillery/howitzer/leFH/Wespe →
artillery class via `list_strike_targets`; hangars/dispersal/scenery →
`scenery[]` / `airfield_scenery`; magneto/failures/cockpit honesty →
`aircraft_failures`; F10/section orders/rejoin-engage → curated
`player.flight.orders`; wingman fail-to-follow → `player.flight.discipline`
(wingman+join_up only). When the ask is a pair/section and `player.flight` is
omitted, the host SHALL nudge once for size 2 role lead. A bare pair/Hawkinge
hop MUST NOT stack scenery, failures, orders, or discipline. Soft immersion
floor remains TheChannel-only.

#### Scenario: Mustang ask nudges P-51D
- **WHEN** invent is asked for a Channel Mustang or P-51 sortie and the draft
  still uses SpitfireLFMkIX
- **THEN** the host MUST nudge once to emit `P-51D` with country USA

#### Scenario: Pair ask nudges size 2 when flight is omitted
- **WHEN** invent is asked for a pair from Hawkinge and the draft has no
  `player.flight`
- **THEN** the host MUST nudge once to emit size 2 role lead

#### Scenario: Bare Hawkinge pair is not stacked
- **WHEN** invent is asked only for a pair from Hawkinge and the draft already
  has `player.flight` size 2
- **THEN** the host MUST NOT require scenery, failures, orders, or discipline
  on that draft
