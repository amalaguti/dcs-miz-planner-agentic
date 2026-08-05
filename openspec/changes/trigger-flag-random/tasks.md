## 1. Implementation

- [x] 1.1 Add `SetFlagRandomAction` to models + TriggerAction union
- [x] 1.2 Validate `min <= max` (and flag name rules)
- [x] 1.3 Emit via PyDCS `SetFlagRandom` in `triggers_emit.py`
- [x] 1.4 Example Spec + unit/compile tests
- [x] 1.5 Update planning_options / schema notes / prompts as needed
- [x] 1.6 BACKLOG `#22a` → done; LESSONS if non-obvious

## 2. Verification

- [x] 2.1 `uv run pytest -q` (triggers/validation at minimum)
