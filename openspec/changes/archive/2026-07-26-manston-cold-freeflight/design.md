## Context

Greenfield repo with OpenSpec and backlog; no Python package yet. Local research established `.miz` zip/Lua shape, Manston `airdromeId = 5`, cold start as `TakeOffParking` / `From Parking Area`, and `start_time = 32400` for 09:00. This change delivers the first compile path only.

## Goals / Non-Goals

**Goals:**

- uv-managed Python package with a minimal free-flight Mission Spec model.
- Deterministic compile of a checked-in Manston cold free-flight example into a `.miz`.
- Acceptance: open the `.miz` in DCS Mission Editor / Instant Action and sit cold at Manston.

**Non-Goals:**

- Agent / NL interface; combat missions; full registry/validation platforms; VEAF; multi-theatre.

## Decisions

1. **PyDCS as compiler backend (v1)**
   - Rationale: handles IDs, packaging, Channel/WWII types; fastest path to a loadable `.miz`.
   - Alternative: hand-rolled Lua serializer — deferred; higher risk for little gain.
   - Boundary: public API is Mission Spec + `CompilerInterface`; PyDCS stays an implementation detail.

2. **Authoring path for v1: YAML Mission Spec → CLI compile**
   - Rationale: forces the contract early; matches architecture (AI later fills the same spec).
   - Alternative: one-off PyDCS script without a spec — rejected (skips the product boundary).

3. **Minimal free-flight schema only**
   - Fields: theatre, date, start_time, weather preset, player (aircraft, country/coalition, airfield name → id mapping, cold parking start).
   - No enemies, triggers, objectives, or briefing VO beyond a short text description.

4. **Hardcoded Manston mapping for this slice**
   - `Manston` → `airdromeId 5` in a small constant/map table inside the compiler (or tiny YAML table).
   - Full Channel registry is backlog M2 (`reference-registry-channel`).

5. **Weather preset `sunny_clear`**
   - Compiler maps named preset → PyDCS/DCS clear-sky weather. Exact table tuned until in-game looks clear; not a full weather system.

6. **Output to `out/` in the repo**
   - Default write path: `out/manston_cold_freeflight.miz` (gitignored).
   - README documents optional copy into `Saved Games\DCS\Missions\` for Instant Action convenience.
   - Alternative: write straight to Saved Games — rejected for repo reproducibility.

7. **Mission date**
   - Use a fixed Channel-valid date in the example spec (e.g. 1944-06-06) unless PyDCS/Channel rejects it; adjust only if load fails.

8. **Package layout**
   - `src/` (or `src/dcs_miz_planner/`) with `models`, `compiler`, `cli`; `examples/manston_cold_freeflight.yaml`; `pyproject.toml` via uv; `requires-python = ">=3.12,<3.14"`.

## Risks / Trade-offs

- [PyDCS Channel parking quirks] → Use cold parking APIs / TakeOffParking; verify against known Channel cold-start sample behavior; fallback to default parking if slot pick fails.
- [“Sunny” looks wrong in-game] → Iterate weather table once; keep preset name stable.
- [PyDCS version lag vs DCS] → Pin a known PyDCS version; document DCS modules required (Channel + Spitfire).
- [Spec too ambitious] → Keep free-flight fields minimal; expand in later changes.

## Migration Plan

N/A (new code). Rollback = delete branch / revert change. Generated `.miz` files under `out/` are not source of truth.

## Open Questions

- Exact PyDCS API calls for Channel parking cold start (spike during apply).
- Whether briefings go into `l10n` dictionary keys in this slice or only mission description fields — prefer minimal description in mission table if PyDCS supports it easily.
