## 1. Briefing text builder

- [x] 1.1 Add `build_mission_briefing_texts(spec, voice)` (or equivalent) that splits
      `build_commander_brief` into plain-text Sortie / Description / blue Task / red Task
      per design mapping; strip markdown headers
- [x] 1.2 Unit tests: free flight + one combat type; `raf` vs `usaaf` differ; Sortie ==
      `spec.name`; Spec `description` appears in Description; opposing task empty

## 2. Compiler + CLI/tools

- [x] 2.1 Extend `CompilerInterface.compile` / `PyDCSCompiler.compile` with optional
      `voice`; call PyDCS setters before `mission.save`; default voice `raf`
- [x] 2.2 Wire `dcs-miz compile --voice` and `compile_mission(..., voice=)`; normalize
      voice at call site when provided
- [x] 2.3 Pytest: compile Manston free flight (and at least one combat example); assert
      `l10n/DEFAULT/dictionary` has non-empty Sortie / Description / player Task

## 3. Golden fixtures

- [x] 3.1 Extend `fixtures_support` to require/compare `l10n/DEFAULT/dictionary`; pin
      golden compiles to `voice="raf"`
- [x] 3.2 Refresh all Manston golden fixtures (free flight, intercept, CAP, ground-attack,
      escort)

## 4. Docs and accept

- [x] 4.1 Update README / ARCHITECTURE / BACKLOG (`briefing-generation` building→done when
      accepted); LESSONS if PyDCS dictionary quirks appear
- [x] 4.2 In-game accept: open a compiled example in DCS ME / Instant Action; confirm
      Sortie, Description, and Task text; note result in tasks/LESSONS
  - Accepted 2026-08-02: `out/manston_briefing_check.miz` — Sortie/Description/Task show
    commander brief. ME group task still defaults to CAP for free flight (pre-existing;
    unrelated to briefing l10n).
