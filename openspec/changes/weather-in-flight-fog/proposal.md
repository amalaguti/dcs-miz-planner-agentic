## Why

Static invent weather (`#17a`/`#17e`) sets the sortie look at load, but Channel
sorties often want **fog that burns off or rolls in during the flight**. DCS
exposes only fog animation mid-mission (`world.weather.setFogAnimation`); clouds
and rain cannot change. Productize that as a small Spec + curated Lua inject —
no full `#22` library yet, no LLM Lua.

## What Changes

- Optional Spec `fog_dynamics` (mode `burn_off` | `roll_in`, timing params)
- Compiler injects a native ONCE `time_more` → `DoScript` using a **human-authored**
  Lua template filled with declared params only
- Example Spec (e.g. dawn + burn-off); hermetic asserts on emitted script text
- BACKLOG `#17c` → building; documents fog-only scope (not sunny→rain)

## Non-goals

- Mid-flight cloud/rain/wind/gallery changes (no DCS API)
- Full `#22` snippet catalog / Mist / MOOSE
- ME Dynamic cyclones
- LLM-authored Lua

## Capabilities

### New Capabilities

- `weather-fog-dynamics`: Spec fog evolution + curated DoScript emit

### Modified Capabilities

- `mission-spec`: optional `fog_dynamics`
- `miz-compiler` / `mission-triggers`: DoScript emit for fog templates
- `mission-validation`: fog_dynamics param checks

## Impact

- `models.py`, compiler trigger emit, small `fog_dynamics.py` template module
- Acceptance: compile example, Instant Action / ME — fog visibly changes over time

## Goal / Why (apply)

**Goal:** Spec-driven mid-sortie fog burn-off / roll-in via curated `setFogAnimation`.
**Why:** Only honest in-flight weather story DCS allows today.
