## 1. Validation engine

- [x] 1.1 Add shared country/skill allowlists (or helpers) usable from `validation.py`; wire unknown country/skill errors on player, enemies, targets, package
- [x] 1.2 Enforce opposing-coalition for intercept and CAP enemies (reuse escort helper pattern)
- [x] 1.3 Implement late_activation ↔ `activate_group` / `deactivate_group` bidirectional graph checks with stable error codes
- [x] 1.4 Reject `message.delay_s > 0` in validation (and pydantic/`models` if needed for load paths)
- [x] 1.5 Confirm dead-on-late-act is covered by the activate graph; add a dedicated error message if clearer UX is needed

## 2. Tests & fixtures

- [x] 2.1 Negative unit tests: late without activate; activate without late; delay_s; bad country/skill; friendly intercept/CAP enemy
- [x] 2.2 Assert `examples/manston_dawn_intercept_radio.yaml` (and other shipped examples) still validate
- [x] 2.3 Mark `docs/BACKLOG.md` `#32` as `building`

## 3. Docs

- [x] 3.1 Update LESSONS (dormant bandits → validation rule; Germany≠ThirdReich hint at validate)
- [x] 3.2 Refresh README Next / BACKLOG promote line when applying
- [x] 3.3 Run `uv run pytest -q`
