## 1. Packaged cards

- [x] 1.1 Add `mission_behaviour` family cards to `planning_options.yaml` (altitude/speed gates, mark/smoke, narrative, radio+late-act, sound, group_life_less) with intent/recipe/example `meta`
- [x] 1.2 Add `mission_inspiration` advisory pattern cards (stock/R5-style ideas) with `meta.behaviours` linking to behaviour ids and optional `source` labels
- [x] 1.3 Confirm registry parse + `dcs-miz catalog sync` / CLI `--family mission_behaviour|mission_inspiration` lists them

## 2. Live mission-design research

- [x] 2.1 Extend `research_guidance` with mission-design focus and/or query enrichment biased toward DCS User Files, public mission repos, and ME/mission-design terms (keep soft-fail + injectable fetch)
- [x] 2.2 Wire tool bridge / surface parameter or documented convention; unit-test enrichment with fake fetch

## 3. Local campaign index

- [x] 3.1 Implement read-only scan of `Mods/campaigns` via discovered DCS root (`.cmp` playlist + `.miz` names + `Doc/` PDF filenames; no full `.miz` import)
- [x] 3.2 Expose agent tool (e.g. `list_installed_campaigns`); hermetic fixture includes sample `Doc/`; optional Doc text extract only if cheap
- [x] 3.3 Prompts: prefer Doc briefing titles/themes over raw `.cmp` stages when inventing from local campaigns

## 4. Agent surface

- [x] 4.1 Update tool descriptions + schema notes for behaviour, inspiration, live research, and local campaigns
- [x] 4.2 Update planning/chat prompts: inspiration → behaviour; research + local campaigns when inventing; no `.miz`→Spec; respect hand-trigger conflicts

## 5. Docs and tests

- [x] 5.1 Tests: option families; research enrichment; local campaign fixture; prompt/schema creative path
- [x] 5.2 BACKLOG / README: status; R1/R2 deep audit vs live snippets vs local index listing
