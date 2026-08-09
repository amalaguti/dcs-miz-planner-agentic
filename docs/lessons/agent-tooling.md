# Agent, catalog, memory & research

Detailed lessons for this topic. Newest first within this file.
Index: [`../LESSONS_LEARNED.md`](../LESSONS_LEARNED.md).

---

## Theatre expand: Normandy first; Marianas WWII needs PyDCS (R11) (2026-08-08)

- **Date:** 2026-08-08
- **Lesson:** Multi-theatre promote order from install+PyDCS audit: **Normandy**
  next (PyDCS `Normandy`, 38 AF, WWII Units on disk). Syria is PyDCS-ready but
  modern shelves. `MarianaIslandsWWII` / Kola / Iraq may be on disk yet **lack**
  PyDCS 0.15 terrain modules — don’t Spec-bind until upstream or R8 bump.
  Inventory cache can lag new terrain folders — `--refresh` before product work.
  Notes: gitignored `research/theatres/`.
- **Code / notes:** `theatre_terrain.py` (Channel-only bind); harness
  `research/audit_theatres_r11.py`.

## Spitfire campaign unit inventory (R13) (2026-08-08)

- **Date:** 2026-08-08
- **Lesson:** Mine Channel Spitfire campaign `.miz` with zip + regex on
  `["type"]` (PyDCS `Mission.load_file` may KeyError on `zones`). Filter
  waypoint/action strings (`Turning Point`, TakeOff*, …). Helos: **none** in
  Beware/FoD/Epsom/Big Show. Promote from frequency shortlist via `#8e` only —
  never auto-YAML. Notes: gitignored `research/campaign-units.md`.
- **Code / notes:** `research/audit_campaign_units_r13.py` (local).

## Train corridor is curated path deltas, not rail-mesh snap (2026-08-08)

- **Date:** 2026-08-08
- **Lesson:** `#8m` ships `trains` class + `french_coast_rail_corridor` place with
  elongated `path_point_deltas` near the Dunkirk inland band. Invent must copy
  that recipe only — never free-form rail routes. Compiler still places vehicles
  on ordinary waypoints; there is **no** DCS rail-mesh snap. ME Instant Action
  may show trains off the visible track; that is expected for v1.
- **Code / notes:** `planning_options.yaml` (`trains`, `french_coast_rail_corridor`);
  `examples/manston_ground_attack_train.yaml`.

## Promote theatres/targets via checklist, not ME dump (2026-08-08)

- **Date:** 2026-08-08
- **Lesson:** Grow theatres and strike/recon shelves only via curated YAML +
  OpenSpec batches. Follow [`docs/THEATRE_TARGET_PROMOTE.md`](../THEATRE_TARGET_PROMOTE.md)
  (`#8e`). Catalog/`list_strike_targets` is not a full ME unit list; never
  auto-promote install discovery into known sources.
- **Code / notes:** checklist SoT; skill `dcs-dev-agent-tooling` Hard rule 3.

## Invent place recipes fix most domain misses; path points still drift (2026-08-08)

- **Date:** 2026-08-08
- **Lesson:** `#8f` ships Manston-relative `channel_place` recipes
  (`french_coast_strike_belt` ~125°/76 km, `mid_channel_shipping` ~140°/40 km,
  `coastal_harbour` ~120°/68 km — **not** 70 km: 120/70 classifies as land).
  `#8g` invent/chat clamps land paths that fail domain **or** diverge from strike
  (near-Manston path + inland strike was validating). Live invent suite 6/6 after
  those fixes. CLI validate does not auto-clamp.
- **Code / notes:** `planning_options.yaml` place meta; `agent/path_clamp.py`;
  `out/target_invent_eval/`.

## Strike unit catalog is curated YAML, not ME dump (2026-08-08)

- **Date:** 2026-08-08
- **Lesson:** `#8c` syncs `catalog_strike_units` from packaged `ground_units.yaml` +
  `ships.yaml` only (class tags inverted from `strike_target_class` meta). ME shows
  far more land/sea types; there is no epoch auto-filter or install scrape. Grow the
  shelf by promoting verified PyDCS ids into YAML, then `catalog sync`. Invent uses
  `list_strike_targets` (SQLite) — compile/validate stay registry SoT.
- **Code:** `catalog/sync.py`, `tools/surface.list_strike_targets`, schema v5.

## Soft immersion floor for vague invent (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** After `#30c`, live eval still under-emitted on “interesting” FF / marked
  GA / Big Show. Host `host_immersion_repair_nudge` once when prompt cues immersion
  but Spec is bare; `get_mission_spec_schema` prefers immersion examples (gates,
  markers, radio, narrative); invent tools omit `randomize_mission` (CLI randomize
  remains). Soft floor — bare Spec may still accept after one nudge.
- **Code:** `agent/immersion.py`, `planner.py`, `session.py`, `spec_schema.py`,
  `tool_bridge.py`.

## Soft-warn: known aircraft module missing from install (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** Theatre inventory does not prove Spitfire/Mosquito/109 packs are
  installed. Spec type ids ≠ updater ids (`SPITFIRE-MKIX`); check folders under
  `Mods/aircraft/` and `CoreMods/WWII Units/` (FW-190 Spec `A8`/`D9` → folders
  `FW-190A-8` / `FW-190D-9`). Soft-warn only (`aircraft_module_missing`); never
  auto-promote into YAML.
- **Code:** `install/aircraft_modules.py`, `ValidationResult.warnings`.

## Campaign Doc PDF excerpts are cached (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** Opt-in `include_doc_text` on `list_installed_campaigns` extracts short
  Doc PDF text via `pypdf`, capped (size/pages/chars). Cache in inventory SQLite
  (`campaign_doc_cache`) by absolute path + mtime_ns + size so unchanged campaign Docs
  are not re-parsed. Default remains filenames-only for fast listing.
- **Code:** `install/doc_extract.py`, `tools/surface.py`.

## Aircraft module discovery cache (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** Harvest folders on `theatres --refresh` into `aircraft_modules` SQLite
  (schema v2) alongside theatres — installs rarely change. Scan
  `Mods/aircraft` + `CoreMods/aircraft` (require `entry.lua`) and
  `CoreMods/WWII Units` (skip shared dirs like `Weapons`/`l10n`). Catalog
  `list --type aircraft` joins known vs discovered-only; never promote into YAML.
  Catalog list does **not** auto-rescan — refresh theatres first.
- **Code:** `harvest_aircraft_modules`, `InventoryStore`, `join_aircraft_views`.

- **Date:** 2026-08-05
- **Lesson:** First `eval-agent-creativity` live run showed catalog tools are *consulted*
  but immersion often not *emitted*: vague free_flight stayed bare; “keeps me honest”
  skipped altitude/speed gates; “choose difficulty” set `late_activation` + narrative
  without F10/`activate_group` (dormant bandits); “Big Show” never called
  `list_installed_campaigns`. Track as BACKLOG `#30c` — prefer prompt/tool/validation
  hardenings over new Spec predicates. Half-recipes (late-act without activate) are
  worse than narrative-only. **Validation (`#32`):** late_activation without
  `activate_group` (and activate without late_act) now **errors** at validate — empty
  sky Specs are no longer green.
- **Code / process:** `.cursor/skills/eval-agent-creativity/`; `validation.py`
  (`late_activation_no_activate` / `activate_not_late`); `#30c` fixes sticky
  `SPEC_SHAPE_REMINDER` empty-triggers conflict, complete-recipe `infer_creative`, and
  stronger prompt/schema immersion pointers.

## Creative decision memory (`detail.creative`)

- **Date:** 2026-08-04
- **Lesson:** Persist creative picks under `generation_history.detail_json` as
  `{"creative": {"behaviours": [...], "inspirations": [...], "sources": [...]}}`.
  Hosts merge light Spec infer when `creative` is absent (`infer_creative_from_spec`).
  Bias via `creative_bias_from_history` + optional prefs
  (`preferred_behaviours` / `avoid_behaviours` / `creativity_level`); inject
  `format_creative_bias_fragment` into the system prompt. Feedback tags
  `liked:…` / `avoid:…` strengthen taste. Do not auto-rewrite packaged cards.
- **Code:** `memory/creative.py`, `agent/planner.py`, `agent/session.py`, `prompts.py`.

## Local campaign inspiration (`.cmp` vs `Doc/`)

- **Date:** 2026-08-04 (honesty update 2026-08-05)
- **Lesson:** `Mods/campaigns/*.cmp` is the campaign **playlist** (stages → `.miz`
  filenames, optional description) — not mission narrative. Real per-sortie colour
  often lives in each pack’s `Doc/*.pdf`, but the agent tool only indexes **PDF
  filenames** (no body extract until backlog `#40`). Prefer Doc filenames/titles over
  raw `.cmp` stage lists when inventing; map onto packaged behaviours; never import
  `.miz` as Spec. Hermetic tests use a fake campaigns tree (`campaigns_dir=`), not
  `S:\DCS World`.
- **Code:** `install/campaigns.py`, `tools/surface.py` (`list_installed_campaigns`).

## Live research: Instant Answer alone is not enough

- **Date:** 2026-08-02
- **Symptom:** `/research Manston spitfire` printed only `fixture:…` notes that looked
  like a successful live lookup; Instant Answer JSON was often empty for multi-word
  aviation queries.
- **Cause:** DuckDuckGo Instant Answer is entity/definition oriented, not a full search
  API; it also sometimes returns an empty HTTP body (JSON decode fails). Soft-fail used
  to abort before any HTML fallback and returned fixtures with a warning chat did not
  label clearly. DDG HTML also serves an anomaly/challenge page for non-browser
  User-Agents (empty `result__a` parse).
- **Fix:** Cascade Instant Answer → `html.duckduckgo.com` result parse (stdlib); treat
  empty/invalid Instant Answer as continue-to-HTML; use a browser User-Agent for HTML;
  detect anomaly pages; enrich query with mission_type/theatre/aircraft; on empty/error
  always warn and label `/research` as offline fixture fallback. Research remains
  non-authoritative for Spec ids.
- **Code:** `tools/research.py`, `agent/session.py` (`/research`).

## Agent Spec JSON needs a derived example (not hand skeletons)

- **Date:** 2026-08-01
- **Symptom:** Live chat emitted flat Spec JSON (`airfield`/`aircraft` top-level, ISO
  `date` string, wrong `enemies`, `cap.objectives`) that Pydantic rejected; `/accept`
  had nothing to write.
- **Cause:** System prompt described rules in prose; models invent plausible shapes.
  Hand-maintained CAP skeletons in the prompt drift as mission types grow.
- **Fix:** `get_mission_spec_schema(mission_type)` + `agent/spec_schema.py` load
  validating examples from `examples/*.yaml`. Thin always-on anti-pattern reminder in
  the prompt; host repair nudge injects the derived example (infer `mission_type` from
  rejected JSON). Commander brief must use enum `.value` (weather → `sunny_clear`).
  `gpt-5.6-luna` rejects function tools on Chat Completions unless `reasoning_effort=none`
  or Responses API — stay on `gpt-4o-mini` until the live client is upgraded.
- **Code:** `agent/spec_schema.py`, `tools/surface.py` (`get_mission_spec_schema`),
  `agent/prompts.py`, `agent/session.py`, `agent/voice.py`.

## Squadron voice is USAAF (not USAF); CLI brief vs `.miz` l10n

- **Date:** 2026-08-01 (updated 2026-08-02)
- **Lesson:** WWII Channel persona id is `usaaf` (Army Air Forces). `usaf` is post-1947 —
  do not rename the voice id. Default voice is `raf`. Commander briefs (tactics /
  procedures / watch-outs) are CLI/`PlanResult.brief` **and**, since `briefing-generation`,
  the same builder feeds compile-time `.miz` `l10n` — Spec fields still stay plain.
  `research_guidance` soft-fails to fixtures with a
  clear warning; chat `/research` labels offline fallback. Live uses Instant Answer then
  HTML results (`DCS_MIZ_RESEARCH_LIVE=1` or chat). Research is not DCS-id authority.
- **Code:** `agent/voice.py`, `agent/prompts.py`, `tools/research.py`, `agent/planner.py`,
  `briefing.py`, `compiler/pydcs_compiler.py`.

## User memory tables are not catalog_*

- **Date:** 2026-08-01
- **Lesson:** Prefs, generation history, and feedback live in the same
  `inventory.sqlite` as install + catalog, but under `user_meta` / `user_prefs` /
  `generation_history` / `satisfaction_feedback`. Never name them `catalog_*` —
  catalog sync and catalog schema bumps wipe those tables. User schema bumps may
  clear only user-memory tables; they must leave install + catalog intact.
  Host `plan_mission` records history; do not rely on the LLM calling
  `record_generation`. Never store API keys in SQLite.
- **Code:** `memory/store.py`, `agent/planner.py`, `tools/surface.py`.

## Catalog schema bump must clear synced_at

- **Date:** 2026-08-01
- **Symptom:** After bumping `CATALOG_SCHEMA_VERSION`, agent tools return empty catalog
  (`find_airfield` not_found) even though packaged YAML is fine.
- **Cause:** Version mismatch wiped `catalog_*` tables but left `catalog_meta.synced_at`,
  so `ensure_synced()` treated the empty DB as already synced.
- **Fix:** On schema mismatch, also delete `synced_at` / `source` so the next ensure/sync
  rebuilds from packaged YAML. Users with a stuck empty catalog can run
  `dcs-miz catalog sync`.
- **Code:** `catalog/store.py` (`CatalogStore._connect`).

## NL planner: stub offline, live via env key only

- **Date:** 2026-08-01
- **Lesson:** `dcs-miz plan` uses `agent/` with tool calling. `--stub` needs no network (canned
  Manston free flight). Live mode reads `OPENAI_API_KEY` (optional `DCS_MIZ_LLM_MODEL`,
  `OPENAI_BASE_URL`) — never store the key in SQLite or the repo. Always validate before
  writing YAML; one repair turn on failure. LLM must not write `.miz`/Lua.
- **Date / era:** Prefer a date that fits the mission’s historical backdrop (WWII for
  current Channel Spitfire/Axis content; later eras or modern day when the user wants).
  Channel years outside ~1939–1945 still succeed but warn (`agent/realism.py` / CLI stderr).
- **Code:** `agent/planner.py`, `agent/llm.py`, `agent/realism.py`; CLI `plan`.

## Agent tools: structured dicts, no dedicated CLI

- **Date:** 2026-08-01
- **Lesson:** Agent callables live in `dcs_miz_planner.tools` and return JSON-friendly
  `{ok: …}` dicts. Lookups use catalog; validate/compile wrap existing engines (inject
  `inventory=` in tests). Browse known data with `dcs-miz catalog list`; there is no
  `dcs-miz tools` CLI in v1 — pytest / Python REPL is the acceptance path.
- **Code:** `tools/surface.py`; `tests/test_tools.py`.

## Agent catalog shares `inventory.sqlite` (query layer, not SoT)

- **Date:** 2026-07-26
- **Lesson:** Known agent rows live in `catalog_*` tables in the same
  `%LOCALAPPDATA%\dcs-miz-planner\inventory.sqlite` as install inventory. YAML under
  `data/channel/` + Spec enums remain the product SoT; `dcs-miz catalog sync` replaces
  `catalog_*` from that package. Theatre **offerable** = known ∧ available ∧
  planner_supported. Never auto-promote discovered install theatres into known YAML.
- **Code:** `catalog/`; CLI `dcs-miz catalog sync|list`.
