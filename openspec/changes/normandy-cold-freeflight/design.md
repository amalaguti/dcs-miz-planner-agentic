## Context

Channel-only planner: `theatre_terrain.py` binds `TheChannel`; packaged
`data/channel/` lists one theatre and Channel airfields. Normandy 2.0 is on the
definitive owned fleet (`Normandy` inventory id), PyDCS has `dcs.terrain.Normandy`
with Needs Oar Point = airdromeId **28**. Promote checklist A wants a Manston-
class smoke before broader Normandy content.

## Goals / Non-Goals

**Goals:**

- First planner-supported WWII map besides Channel: cold freeflight Spitfire at
  Needs Oar Point.
- Fail-closed binding + registry + validate/compile + hermetic tests.
- Record definitive fleet in BACKLOG (already noted).

**Non-Goals:**

- Full Normandy airfield YAML, GA/strike shelves, Normandy places, invent cues.
- Multi-theatre invent prompts rewrite beyond accepting Normandy Specs that
  authors write by hand.
- Other fleet maps.

## Decisions

1. **Keep one packaged registry (`data/channel/`)**
   Add `Normandy` to `theatres.yaml` and `NeedsOarPoint: 28` to `airfields.yaml`.
   *Alt:* split `data/normandy/` — deferred until more Normandy content justifies it.

2. **Curated Spec key `NeedsOarPoint`** (Channel style: no spaces) → id 28.
   Display name in PyDCS is `Needs Oar Point`; compiler uses airdromeId.

3. **Reuse Spitfire + `sunny_clear` + UK blue cold parking** — same freeflight
   path as Manston; only theatre/airfield change.

4. **Hermetic inventory helper** extends to Channel+Normandy (or Normandy-only
   helper used by Normandy tests). Live DCS not required for CI.

5. **Golden:** structure asserts on compiled Normandy `.miz` (theatre member /
   player placement) rather than a full golden zip refresh unless cheap to add.

6. **Catalog:** after YAML sync, `Normandy` becomes known; offerable when install
   inventory marks it available (existing join).

## Risks / Trade-offs

- [Shared airfield map] Channel+Normandy keys in one dict → Mitigation: no
  overlapping names today; future collisions need prefixed keys or split packages.
- [Invent still Channel-centric] NL invent may not propose Normandy → Mitigation:
  documented; hand Specs + validate/compile work; invent multi-theatre later.
- [ME parking at Needs Oar Point] Spitfire cold slots may differ → Mitigation: ME
  Instant Action acceptance after compile.

## Migration Plan

Ship on branch `normandy-cold-freeflight`; sync main specs on archive. No DB
migration beyond `catalog sync` picking up new theatre/airfield.

## Open Questions

- None blocking smoke. Next slice: more Normandy AFs / places after ME accept.
