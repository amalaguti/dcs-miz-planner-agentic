# Lessons Learned

Living agent notes for PyDCS / DCS / compiler / agent pitfalls.
**Do not** treat this as the product contract — durable requirements stay in OpenSpec.

## How to use (agents)

1. **Start of work:** open the matching topic file under [`lessons/`](lessons/)
   (or the `dcs-dev-*` skill) — do not read this whole index end-to-end.
2. **After a non-obvious fix:** append a full entry to the **topic file** (newest
   near the top of that file), add one row to the **Index** below, and update the
   matching `dcs-dev-*` skill if the pitfall changes a procedure.
3. Skill `keep-lessons-learned` owns the write workflow.

## Topic files

| Topic | File | Skill |
|-------|------|-------|
| Player flight | [`lessons/player-flight.md`](lessons/player-flight.md) | `dcs-dev-player-flight` |
| Weather & fog | [`lessons/weather.md`](lessons/weather.md) | `dcs-dev-weather` |
| Triggers / ME / failures | [`lessons/triggers-me.md`](lessons/triggers-me.md) | `dcs-dev-triggers-me` |
| Channel identity ids | [`lessons/channel-ids.md`](lessons/channel-ids.md) | `dcs-dev-channel-ids` |
| PyDCS compile | [`lessons/pydcs-compile.md`](lessons/pydcs-compile.md) | `dcs-dev-pydcs-compile` |
| Agent / catalog / research | [`lessons/agent-tooling.md`](lessons/agent-tooling.md) | `dcs-dev-agent-tooling` |
| CI / install / process | [`lessons/ci-process.md`](lessons/ci-process.md) | `dcs-dev-ci-process` |

## Index (newest first)

| Date | Lesson | Topic |
|------|--------|-------|
| 2026-08-08 | [Target motion: ship/vehicle waypoints + SwitchWaypoint loop](lessons/pydcs-compile.md#target-motion-shipvehicle-waypoints--switchwaypoint-loop-2026-08-08) | `pydcs-compile` |
| 2026-08-07 | [Recon AOI land/sea domain for contacts](lessons/triggers-me.md#recon-aoi-landsea-domain-for-contacts-2026-08-07) | `triggers-me` |
| 2026-08-07 | [Recon AOI find pack (`mission_type: recon`)](lessons/triggers-me.md#recon-aoi-find-pack-mission_type-recon-2026-08-07) | `triggers-me` |
| 2026-08-07 | [Fail-to-follow discipline (`player.flight.discipline`)](lessons/player-flight.md#fail-to-follow-discipline-playerflightdiscipline-2026-08-07) | `player-flight` |
| 2026-08-07 | [Synthetic METAR + rainy light gallery beyond PyDCS](lessons/weather.md#synthetic-metar--rainy-light-gallery-beyond-pydcs-2026-08-07) | `weather` |
| 2026-08-07 | [OpenSpec CLI invoke: use `npx`, not `uv`](lessons/ci-process.md#openspec-cli-invoke-use-npx-not-uv-2026-08-07) | `ci-process` |
| 2026-08-07 | [F10 section orders (`player.flight.orders`)](lessons/player-flight.md#f10-section-orders-playerflightorders-2026-08-07) | `player-flight` |
| 2026-08-07 | [Aircraft failures via ME Failures table](lessons/triggers-me.md#aircraft-failures-via-me-failures-table-2026-08-07) | `triggers-me` |
| 2026-08-07 | [Aircraft failures via ME SetFailure triggers](lessons/triggers-me.md#aircraft-failures-via-me-setfailure-triggers-2026-08-07) | `triggers-me` |
| 2026-08-07 | [Player flight wingman Follow / join-up](lessons/player-flight.md#player-flight-wingman-follow-join-up-2026-08-07) | `player-flight` |
| 2026-08-07 | [Player flight: SP Player must be group unit #1](lessons/player-flight.md#player-flight-sp-player-must-be-group-unit-1-2026-08-07) | `player-flight` |
| 2026-08-06 | [In-flight weather: fog yes, clouds/rain no](lessons/weather.md#in-flight-weather-fog-yes-cloudsrain-no-2026-08-06) | `weather` |
| 2026-08-06 | [Weather invent seed vs golden stability](lessons/weather.md#weather-invent-seed-vs-golden-stability-2026-08-06) | `weather` |
| 2026-08-06 | [PyDCS cloud presets vs legacy density weather](lessons/weather.md#pydcs-cloud-presets-vs-legacy-density-weather-2026-08-06) | `weather` |
| 2026-08-05 | [Spec dynamics expand XOR with narrative](lessons/triggers-me.md#spec-dynamics-expand-xor-with-narrative-2026-08-05) | `triggers-me` |
| 2026-08-05 | [GitHub CLI + hermetic CI (no Windows/DCS on runners)](lessons/ci-process.md#github-cli-hermetic-ci-no-windowsdcs-on-runners-2026-08-05) | `ci-process` |
| 2026-08-05 | [CI needs hermetic inventory; strip install-local liveries](lessons/ci-process.md#ci-needs-hermetic-inventory-strip-install-local-liveries-2026-08-05) | `ci-process` |
| 2026-08-05 | [R2 ED Spitfire campaigns: immersion without triggers](lessons/triggers-me.md#r2-ed-spitfire-campaigns-immersion-without-triggers-2026-08-05) | `triggers-me` |
| 2026-08-05 | [R1 Channel User Files: native dynamic > Mist](lessons/triggers-me.md#r1-channel-user-files-native-dynamic-mist-2026-08-05) | `triggers-me` |
| 2026-08-05 | [Weather SoT parity](lessons/weather.md#weather-sot-parity-2026-08-05) | `weather` |
| 2026-08-05 | [Campaign Doc PDF excerpts are cached](lessons/agent-tooling.md#campaign-doc-pdf-excerpts-are-cached-2026-08-05) | `agent-tooling` |
| 2026-08-05 | [Spec theatre → PyDCS terrain binding](lessons/pydcs-compile.md#spec-theatre-pydcs-terrain-binding-2026-08-05) | `pydcs-compile` |
| 2026-08-05 | [Soft immersion floor for vague invent](lessons/agent-tooling.md#soft-immersion-floor-for-vague-invent-2026-08-05) | `agent-tooling` |
| 2026-08-05 | [Soft-warn: known aircraft module missing from install](lessons/agent-tooling.md#soft-warn-known-aircraft-module-missing-from-install-2026-08-05) | `agent-tooling` |
| 2026-08-05 | [Aircraft module discovery cache](lessons/agent-tooling.md#aircraft-module-discovery-cache-2026-08-05) | `agent-tooling` |
| — | [Creative decision memory (`detail.creative`)](lessons/agent-tooling.md#creative-decision-memory-detailcreative) | `agent-tooling` |
| — | [Local campaign inspiration (`.cmp` vs `Doc/`)](lessons/agent-tooling.md#local-campaign-inspiration-cmp-vs-doc) | `agent-tooling` |
| — | [Player altitude / speed gates](lessons/triggers-me.md#player-altitude-speed-gates) | `triggers-me` |
| — | [Mark + smoke zone markers](lessons/triggers-me.md#mark-smoke-zone-markers) | `triggers-me` |
| — | [Group life less (partial damage)](lessons/triggers-me.md#group-life-less-partial-damage) | `triggers-me` |
| — | [F10 radio items + late activation emit](lessons/triggers-me.md#f10-radio-items-late-activation-emit) | `triggers-me` |
| — | [Sound assets + numeric flags](lessons/triggers-me.md#sound-assets-numeric-flags) | `triggers-me` |
| — | [R9 ME enrichment candidates (radio / late-act first)](lessons/triggers-me.md#r9-me-enrichment-candidates-radio-late-act-first) | `triggers-me` |
| 2026-08-04 | [R7 PyDCS open-issue triage](lessons/pydcs-compile.md#r7-pydcs-open-issue-triage-2026-08-04) | `pydcs-compile` |
| — | [Opt-in CAP narrative expands before validate/compile](lessons/triggers-me.md#opt-in-cap-narrative-expands-before-validatecompile) | `triggers-me` |
| — | [Trigger Spec compiles to native ME tables](lessons/triggers-me.md#trigger-spec-compiles-to-native-me-tables) | `triggers-me` |
| — | [Trigger Spec is typed; .miz emit is a separate change](lessons/triggers-me.md#trigger-spec-is-typed-miz-emit-is-a-separate-change) | `triggers-me` |
| — | [Mission randomization: seed is build-scoped, not forever-stable](lessons/weather.md#mission-randomization-seed-is-build-scoped-not-forever-stable) | `weather` |
| — | [Weather presets: dawn_clear / marginal_vfr mappings](lessons/weather.md#weather-presets-dawn_clear-marginal_vfr-mappings) | `weather` |
| — | [Briefing l10n: PyDCS setters + lazy import (no compiler↔agent cycle)](lessons/pydcs-compile.md#briefing-l10n-pydcs-setters-lazy-import-no-compileragent-cycle) | `pydcs-compile` |
| — | [Escort: package first, then EscortTaskAction + ROE](lessons/pydcs-compile.md#escort-package-first-then-escorttaskaction-roe) | `pydcs-compile` |
| — | [Ground-attack: always verify strike position (land vs water, enemy vs practice)](lessons/pydcs-compile.md#ground-attack-always-verify-strike-position-land-vs-water-enemy-vs-practice) | `pydcs-compile` |
| — | [Ground-attack: registry CLSID loadout + Bombing (not install payload scan)](lessons/pydcs-compile.md#ground-attack-registry-clsid-loadout-bombing-not-install-payload-scan) | `pydcs-compile` |
| — | [Live research: Instant Answer alone is not enough](lessons/agent-tooling.md#live-research-instant-answer-alone-is-not-enough) | `agent-tooling` |
| — | [Agent Spec JSON needs a derived example (not hand skeletons)](lessons/agent-tooling.md#agent-spec-json-needs-a-derived-example-not-hand-skeletons) | `agent-tooling` |
| — | [CAP station is airfield-relative; ROE is Spec-backed](lessons/pydcs-compile.md#cap-station-is-airfield-relative-roe-is-spec-backed) | `pydcs-compile` |
| — | [Squadron voice is USAAF (not USAF); CLI brief vs `.miz` l10n](lessons/agent-tooling.md#squadron-voice-is-usaaf-not-usaf-cli-brief-vs-miz-l10n) | `agent-tooling` |
| — | [User memory tables are not catalog_*](lessons/agent-tooling.md#user-memory-tables-are-not-catalog_) | `agent-tooling` |
| — | [Catalog schema bump must clear synced_at](lessons/agent-tooling.md#catalog-schema-bump-must-clear-synced_at) | `agent-tooling` |
| — | [NL planner: stub offline, live via env key only](lessons/agent-tooling.md#nl-planner-stub-offline-live-via-env-key-only) | `agent-tooling` |
| — | [Agent tools: structured dicts, no dedicated CLI](lessons/agent-tooling.md#agent-tools-structured-dicts-no-dedicated-cli) | `agent-tooling` |
| — | [Agent catalog shares `inventory.sqlite` (query layer, not SoT)](lessons/agent-tooling.md#agent-catalog-shares-inventorysqlite-query-layer-not-sot) | `agent-tooling` |
| — | [Channel WWII Axis: use `ThirdReich`, not `Germany`](lessons/channel-ids.md#channel-wwii-axis-use-thirdreich-not-germany) | `channel-ids` |
| — | [Intercept spawn: Hawkinge anchor + Dover-approach offset](lessons/channel-ids.md#intercept-spawn-hawkinge-anchor-dover-approach-offset) | `channel-ids` |
| — | [Golden fixtures: normalize random `onboard_num`](lessons/pydcs-compile.md#golden-fixtures-normalize-random-onboard_num) | `pydcs-compile` |
| — | [Install inventory: SQLite cache, never execute DCS Lua](lessons/ci-process.md#install-inventory-sqlite-cache-never-execute-dcs-lua) | `ci-process` |
| — | [Stock Channel Spitfire: native triggers, almost no Lua](lessons/triggers-me.md#stock-channel-spitfire-native-triggers-almost-no-lua) | `triggers-me` |
| — | [Mission Scripting API defs ≠ ME trigger predicates](lessons/pydcs-compile.md#mission-scripting-api-defs-me-trigger-predicates) | `pydcs-compile` |
| — | [Spitfire / WWII: group frequency must be in VHF band](lessons/channel-ids.md#spitfire-wwii-group-frequency-must-be-in-vhf-band) | `channel-ids` |
| — | [Spitfire cockpit arguments: triggers only, not compile input](lessons/triggers-me.md#spitfire-cockpit-arguments-triggers-only-not-compile-input) | `triggers-me` |
| — | [PyDCS: payload loader KeyError when DCS install is present](lessons/pydcs-compile.md#pydcs-payload-loader-keyerror-when-dcs-install-is-present) | `pydcs-compile` |
| — | [PyDCS: no standalone `theatre` zip member](lessons/pydcs-compile.md#pydcs-no-standalone-theatre-zip-member) | `pydcs-compile` |
| — | [PyDCS weather: `clouds_iprecptns` is an enum](lessons/pydcs-compile.md#pydcs-weather-clouds_iprecptns-is-an-enum) | `pydcs-compile` |
| — | [DCS identity strings: never invent](lessons/channel-ids.md#dcs-identity-strings-never-invent) | `channel-ids` |
| — | [Mission Spec vs PyDCS boundary](lessons/pydcs-compile.md#mission-spec-vs-pydcs-boundary) | `pydcs-compile` |
| — | [OpenSpec / git process](lessons/ci-process.md#openspec-git-process) | `ci-process` |

## Entry format (topic files)

```markdown
## Short title (YYYY-MM-DD)

- **Date:** YYYY-MM-DD
- **Symptom:** …
- **Cause:** …
- **Fix:** …
- **Code / notes:** …
```

Or a short **Lesson:** bullet when there is no bug narrative.
