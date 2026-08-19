## ADDED Requirements

### Requirement: Invent player is Spitfire on bound modern theatres
When invent/chat emits a Mission Spec for theatre `Caucasus`, `Syria`, `Nevada`,
`Falklands`, or `Kola`, `player.aircraft` MUST be `SpitfireLFMkIX` unless the
user names Su-25T/Frogfoot or P-51. Airfield and station geometry MUST remain
the theatre home (Batumi, Incirlik, Nellis, MountPleasant, Bodo). Su-25T MAY
remain on enemies or escort package when the ask is Cold War or unspecified
modern. Kola MUST remain free_flight only.

#### Scenario: Caucasus invent player is Spitfire
- **WHEN** invent is asked for a Caucasus free-flight or combat type without naming Frogfoot
- **THEN** the emitted Spec MUST use `player.aircraft` SpitfireLFMkIX at Batumi
  (MUST NOT copy Su-25T into the player slot from theatre YAML)

#### Scenario: Named Frogfoot keeps Su-25T player
- **WHEN** the user names Su-25T or Frogfoot as the aircraft they will fly
- **THEN** invent MUST NOT rewrite `player.aircraft` to SpitfireLFMkIX

### Requirement: WWII colour opposition on modern theatres
When the bound theatre is Caucasus, Syria, Nevada, or Falklands and the ask
cues WWII / Luftwaffe / 1944, invent MUST emit enemies `Bf-109K-4` or
`FW-190A8` with country `ThirdReich` rather than defaulting Su-25T Russia/Syria
red. It MUST NOT invent MiG-15 or F-86 ids. Kola combat remains refused.

#### Scenario: Luftwaffe cue on Caucasus does not keep Su-25T enemies
- **WHEN** invent is asked for a 1944 Luftwaffe bounce over Batumi
- **THEN** enemies MUST be Bf-109K-4 or FW-190A8 country ThirdReich
  (MUST NOT be Su-25T Russia as the default opposition)

### Requirement: Invent asserts dynamics and moving targets from cues
When a validated invent/chat draft omits play-time variation that the ask
implied, the host MUST one-shot nudge a combined repair (player, opposition,
dynamics, and/or motion) rather than accepting a static Spec. Vague
unpredictable / dice / different-each-load asks MUST emit `dynamics.mode` `live`;
F10 / I-choose asks MUST emit `choose`; both MUST emit `hybrid`. Ground-attack
or recon asks for moving convoy / under way / patrol MUST set `targets[].motion`
to `patrol` or `path` (presets `convoy_transit` / `ship_under_way` as
appropriate). The host MUST NOT enable `narrative` together with `dynamics`.
The host MUST NOT treat CLI `dcs-miz randomize` as invent authoring.

#### Scenario: Different-each-load intercept gets live dynamics
- **WHEN** the user asks for an intercept that is different each load and the
  draft omits `dynamics` (or uses mode `fixed`)
- **THEN** the host MUST nudge `dynamics.mode` `live` with exclusive late-activation
  pools (MUST NOT enable narrative)

#### Scenario: F10 choose cue gets choose mode
- **WHEN** the user asks to pick difficulty from the F10 menu and the draft omits dynamics
- **THEN** the host MUST nudge `dynamics.mode` `choose`

#### Scenario: Moving convoy cue sets target motion
- **WHEN** the user asks for a moving convoy ground attack and all targets are static
- **THEN** the host MUST nudge `targets[].motion` `patrol` or `path`

#### Scenario: Narrative xor skips dynamics nudge
- **WHEN** the draft has `narrative.enabled` true
- **THEN** the host MUST NOT nudge `dynamics`

## MODIFIED Requirements

### Requirement: Kola invent is free_flight only
Invent/chat SHALL allow `free_flight` when the bound theatre is `Kola`
(home `Bodo`, player `SpitfireLFMkIX`, `sunny_clear`, Norway blue). It SHALL refuse
`intercept`, `cap`, `ground_attack`, `escort`, and `recon` on Kola every
turn (never capture or write a refused Spec). Repair MUST nudge toward Bodo
free_flight or switching theatre to TheChannel — not MountPleasant, Nellis,
Incirlik, Batumi, NeedsOarPoint, or Manston.

#### Scenario: Kola free_flight invent allowed
- **WHEN** invent is asked for a Kola free-flight
- **THEN** the planner MUST be allowed to emit `theatre: Kola` with
  `airfield: Bodo` and player SpitfireLFMkIX

#### Scenario: Kola CAP invent refused every turn
- **WHEN** invent is asked for a CAP on Kola
- **THEN** it MUST NOT emit a combat Mission Spec and MUST surface a repair
  toward Bodo free_flight (or TheChannel combat)
