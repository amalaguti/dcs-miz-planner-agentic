# Golden fixtures

Structural expectations for compiled `.miz` output. Compared by pytest; not rewritten
during ordinary test runs.

## Manston cold free-flight

Directory: `tests/fixtures/manston_cold_freeflight/`

| File | Role |
|------|------|
| `theatre` | Exact `theatre` zip member |
| `mission` | Normalized `mission` zip member (`onboard_num` redacted — random per process) |
| `meta.json` | Required zip members + contracted mission substrings |

## Manston dawn intercept

Directory: `tests/fixtures/manston_dawn_intercept/`

Same layout; contracts include `Bf-109K-4` and German VHF `40.0` MHz.

## Manston CAP

Directory: `tests/fixtures/manston_cap/`

Contracts include CAP task, Orbit/Circle, ControlledTask duration, OptROE value, and
optional Bf-109 opposition.

## Refresh after an intentional compiler change

```bash
uv run python tests/refresh_manston_golden.py
uv run python tests/refresh_intercept_golden.py
uv run python tests/refresh_cap_golden.py
uv run pytest -q
```

Review the diff under `tests/fixtures/`, then commit with the compiler change. If mission
semantics changed, also open the compiled `.miz` in DCS.
