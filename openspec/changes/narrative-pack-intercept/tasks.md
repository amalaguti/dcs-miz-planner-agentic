## 1. Intercept pack

- [x] 1.1 Refactor `narrative.py` for multi-pack dispatch; add intercept pack (scramble + unit_dead→win); keep CAP behaviour
- [x] 1.2 Update unsupported-type errors to allow intercept; require enemies for intercept

## 2. Example, agent, docs

- [x] 2.1 Add `examples/manston_dawn_intercept_narrative.yaml`
- [x] 2.2 Agent schema/prompt notes for intercept narrative; BACKLOG/README pointer

## 3. Tests and acceptance

- [x] 3.1 Tests: expand/validate/compile intercept narrative; CAP regression; unsupported types
- [x] 3.2 In-game: ME Triggers shows intercept narrative rules on compiled example
  - Accepted 2026-08-04: ME shows `narrative_scramble` + `narrative_bandits_down` (MESSAGE TO ALL + END MISSION) on `out/manston_dawn_intercept_narrative.miz`.
