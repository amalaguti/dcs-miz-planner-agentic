## Context

`tests/test_compile_manston.py` already compiles the Manston example and asserts zip
members plus selected mission strings (theatre, Spitfire, airdromeId 5, start_time,
TakeOffParking, Player, frequency 124.0). That is useful but ad-hoc: there is no checked-in
expected artifact, no refresh ritual, and no shared helper for the next mission types.

Validation and the Channel registry are done; before M3 agents start emitting Specs, pin
the Manston compile surface as a golden structural regression.

## Goals / Non-Goals

**Goals:**

- Checked-in structural goldens for Manston free-flight compile output.
- Pytest compares a fresh compile (injected available Channel inventory) to those goldens.
- Clear, intentional fixture refresh when compiler output changes on purpose.
- Single primary regression surface (thin or fold overlapping Manston asserts).

**Non-Goals:**

- Byte-identical full `.miz` zip comparison.
- Combat / trigger / multi-theatre goldens.
- Changing production compiler logic unless a bug is found.
- CI release tagging or packaging.

## Decisions

1. **Store extracted text members, not a binary `.miz` as the sole golden**
   - Check in at least `theatre` (exact string) and a **normalized** `mission` excerpt or
     full `mission` member with documented ignore rules if needed.
   - Prefer: `tests/fixtures/manston_cold_freeflight/` containing `theatre` plus
     `mission.expected` (full or trimmed) and a small `meta.json` listing required zip
     members and key substring contracts that must still hold.
   - Alternative rejected: whole `.miz` binary golden — zip timestamps / compression differ.

2. **Compare structure, not PyDCS round-trip as the golden**
   - Keep optional PyDCS load_file smoke if useful, but goldens are zip-member text/asserts.
   - Alternative rejected: only round-trip through PyDCS — does not catch radio/theatre
     member regressions we already care about.

3. **Inject synthetic Channel inventory in golden tests**
   - Same pattern as validation/compile tests so CI/local runs without depending on a live
     SQLite inventory. Production CLI still uses real inventory.

4. **Refresh path: compile once, write fixture files, review diff, commit**
   - Document a one-liner or tiny script under `tests/` (e.g. `pytest --update-goldens` **or**
     a `uv run python -m tests.refresh_manston_golden` helper). Prefer an explicit refresh
     module over a magic pytest flag if simpler to maintain.
   - Never auto-update goldens in normal `pytest`.

5. **Scope v1 = Manston example only**
   - One Spec → one fixture directory. Expand when new mission types land.

## Risks / Trade-offs

- [PyDCS output churn on library upgrade] → Goldens fail loudly; refresh after intentional
  upgrade, with DCS open-check if mission semantics changed.
- [Over-asserting volatile Lua ordering] → Assert required members + stable key fields /
  substrings first; only store full `mission` if diffs stay readable.
- [Duplicating asserts with old compile tests] → Migrate Manston structural checks into the
  golden test; leave thin “compiles + round-trip” if still valuable.

## Migration Plan

1. Generate fixtures from current accepted compiler output.
2. Add golden tests; delete or thin redundant asserts in `test_compile_manston.py`.
3. Document refresh in README or `tests/fixtures/README.md`.
4. No runtime migration; tests-only change.

## Open Questions

None blocking — full vs substring `mission` golden can be chosen during apply based on
diff readability of the first generated fixture.
