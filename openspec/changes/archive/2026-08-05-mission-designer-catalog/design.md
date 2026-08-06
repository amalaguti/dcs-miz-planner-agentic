## Context

After v0.3 the pipeline is Spec → deterministic compile, with `mission_behaviour` /
`mission_inspiration` cards and immersion floor. The product goal shifts the agent to
**mission designer co-author**: it must recommend only from declared shelves (dynamics
modes, strike composition, places), joined to what the catalog already knows
(airfields, payloads, ground/sea ids in registry YAML).

Today `planning_options.yaml` has envelope knobs + behaviours/inspirations, but not
designer ontology for “live vs F10 vs fixed”, “truck vs E-boat → which payload/domain”,
or curated Channel place talk-tracks. `#30f` will later expand Spec `dynamics`; this
change only puts the **palette** in the catalog.

## Goals / Non-Goals

**Goals:**

- Packaged, syncable planning-option families the agent can list and reason over.
- Explicit meta linking strike classes → domain + unit/ship ids + payload families.
- Prompt contract: invent/chat consults shelves before recommending.
- Hermetic tests (catalog sync + list + prompt/tool smoke) — no DCS/Windows CI need.

**Non-Goals:**

- Compiling `dynamics` or changing Mission Spec schema (`#30f`).
- Auto-promoting discovered units into YAML.
- Exhaustive Channel POI database.

## Decisions

1. **Reuse `planning_options` + existing catalog sync**
   New families are rows in `planning_options.yaml` (`support` + `meta`), same path as
   behaviours. Avoid new SQLite table types unless sync cannot express the meta (it can
   via `meta_json`).
   *Alt considered:* separate YAML files / `catalog_*` tables — deferred; one sync path
   keeps CLI/`list_mission_options` simple.

2. **Family ids (v1)**
   - `dynamics_mode`: `fixed`, `live`, `choose`, `hybrid` — all `advisory` until `#30f`
     makes them Spec-backed; meta documents intended emit (`set_flag_random`, radio+late,
     none).
   - `strike_target_class`: soft land (trucks/soft), AAA/guns, hard/infrastructure
     (advisory/future if no unit id yet), sea (boats/ships using `ships.yaml` ids). Meta
     MUST include `domain` (`land`|`sea`), `unit_ids` and/or `ship_ids` (verified registry
     keys only), `payload_families`, and `notes` for agent copy.
   - `channel_place`: curated places (e.g. Manston, coastal French AAA belt, mid-Channel
     shipping lane) — `advisory`; meta may reference airfield name or relative geometry
     hints, never invented airdromeIds.

3. **Composition rules live in meta, not code**
   Agent reads meta; validation of land/sea placement stays in existing
   `strike-domain-validate`. Do not duplicate domain math in catalog service.

4. **Prompts (nl-agent)**
   When inventing ground_attack / discussing dynamics / places: MUST call
   `list_mission_options` (or equivalent catalog list) for the new families before
   locking recommendations; speak as co-designer (options + tradeoffs), still no LLM Lua.

5. **Layer A vs B**
   Document in card descriptions: CLI `randomize` = new Spec day (Layer A); dynamics
   modes = play-time variation inside one `.miz` (Layer B, `#30f`). Do not conflate.

## Risks / Trade-offs

- [Risk] Advisory dynamics cards overpromise before `#30f` → Mitigation: `support:
  advisory` + description “palette only; emit deferred”.
- [Risk] Strike classes name units not in YAML → Mitigation: only ids present in
  `ground_units.yaml` / `ships.yaml`; hard targets may be `future` with no unit_ids.
- [Risk] Prompt length / option noise → Mitigation: small v1 card sets (≤8 per family);
  “pick then recommend”.
- [Risk] Agent skips tools → Mitigation: invent prompt MUST list shelf consult; tests on
  prompt/tool surface strings where existing harness allows.

## Migration Plan

- Additive YAML + prompt + tests. Rollback: remove families / revert prompts.
- After accept: archive; `#30f` references `dynamics_mode` meta for emit.

## Open Questions

- Whether `channel_place` should later sync from a dedicated `places.yaml` (lean keep in
  planning_options until volume hurts).
- Exact hybrid card wording vs choose+live — finalize in YAML copy at apply.
