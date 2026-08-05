## 1. Detail convention + recording

- [x] 1.1 Document `detail.creative` shape (inspirations, behaviours, sources) in code/docs comments or small helper constants
- [x] 1.2 Ensure planner/chat success `record_generation` can accept/pass creative detail (host and/or agent tool path)
- [x] 1.3 Tests: detail round-trip via memory/tools

## 2. Bias helper

- [x] 2.1 Implement `creative_bias_from_history` (or equivalent) from generations + feedback → prefer/avoid
- [x] 2.2 Unit tests: high score prefers; empty history empty; mission_type filter

## 3. Agent surface

- [x] 3.1 Update prompts: vague invent → list options → consult history/bias → 1–2 behaviours
- [x] 3.2 Update `record_generation` / related tool descriptions for creative detail
- [x] 3.3 Optional: prefs keys `preferred_behaviours` / `avoid_behaviours` / `creativity_level` if cheap

## 4. Docs

- [x] 4.1 BACKLOG `#30a` → building/done as appropriate; README one-liner if status changes
- [x] 4.2 Prompt/schema tests mention history bias
