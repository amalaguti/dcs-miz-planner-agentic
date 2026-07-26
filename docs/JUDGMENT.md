# Project judgment — 2026-07-26

Gate review after M2 close-out. Evidence: concept doc, `docs/BACKLOG.md`,
`docs/ARCHITECTURE.md`, `docs/LESSONS_LEARNED.md`, `ideas-concepts.txt`,
`openspec/specs/`, archived M1–M2 changes. No code shipped in this review.

## 1. Scorecard — what we proved

**Proven**

- End-to-end free-flight: Manston Spitfire cold start compiles, validates, opens in DCS.
- Contract hardening (M2): Spec `schema_version` `"1"`, Channel YAML registry, install
  inventory (SQLite), shared `validate_mission_spec`, Manston golden fixtures.
- Process: OpenSpec change → named branch → apply → in-game/CLI accept → archive → merge.
- Principle held in code: AI does not author Lua; PyDCS stays behind `CompilerInterface`.

**Not proven**

- Natural language → Spec (no agent layer yet).
- Any combat mission (enemies/objectives still reserved and refused).
- Triggers / mission behaviour beyond placement.
- Multi-theatre, multiplayer, campaigns, VO, historical validation.

**Spine check:** Infrastructure matches “AI plans / software compiles,” but relative to the
concept’s *first product story* (dawn Manston intercept vs Bf-109s) we over-invested in
free-flight trust before proving combat compile. That was reasonable for M1–M2; continuing
straight into M3 agent tools for free-flight-only would widen the gap.

## 2. Decision audit

| Decision | Verdict | Why |
|----------|---------|-----|
| PyDCS behind `CompilerInterface` | **Keep** | Still the right seam for M4/M6; no evidence to replace it yet. |
| YAML registry = product SoT; SQLite = install only | **Keep** | Ideas wanted “everything in SQLite”; split is clearer and already shipped. Landmarks/weapons stay later YAML (or tables), not install DB. |
| No LLM Lua | **Keep** | Non-negotiable through M6; snippets only as curated compiler output. |
| Channel-only / Spitfire-first | **Keep** | Narrowing still correct; Normandy waits. |
| M3 agent before first combat (M4) | **Revise** | Reorder: prove intercept compile before agent tools / NL. |
| Native triggers before Mist/MOOSE | **Keep** | R5 stock Channel supports this; revisit only after R1–R2. |
| Defer package versioning/tags | **Keep** | Sole consumer; revisit when someone else needs a pin. |
| One item `building` at a time | **Keep** | Process discipline is working. |

## 3. Sequencing — single next promote

**Next OpenSpec change: `mission-type-intercept`**

Why:

1. Concept’s canonical example is an intercept, not free flight.
2. M3’s own rule (“AI arrives only once compilation is trustworthy”) — combat compile is
   not trustworthy until we ship one.
3. Reserved `enemies` / `objectives` need a real first consumer; agent tools wrapping
   free-flight-only add little product proof.
4. Thin M3 tools can follow quickly once intercept Spec + compile + golden + in-game accept exist.

**Explicitly not next**

- `nl-to-spec-agent`, `squadron-commander-voice`, `mission-option-catalog`
- `agent-tools-surface` (defer until after intercept accept, then thin tools)
- M6 trigger model (need combat Spec shape first; intercept v1 = placement + objective stub,
  not full trigger graph unless trivially required for ME load)
- Research-only burst (R1/R2) as a blocking gate — useful in parallel later, not instead of
  the first combat slice
- Release versioning / tags

**Acceptance bar for `mission-type-intercept`**

- Checked-in example Spec; `dcs-miz validate` + compile succeed.
- Golden (or extended) structural asserts for enemy presence / key contracts.
- Open/fly in DCS Mission Editor / Instant Action (player Spitfire vs Bf-109K-4 intercept
  scenario as specified in the change).

## 4. Scope hygiene — ideas → status

| Raw idea (`ideas-concepts.txt`) | Status |
|---------------------------------|--------|
| Module diagram | Done (M2 `#7`) |
| SQLite asset inventory | Partially done — theatres install DB; full asset dump **park** (YAML registry path) |
| Squadron commander narration | Park → M3 `#11` after tools |
| Planning options catalog | Park → M3 `#9` |
| Lua integration | Park → M6; never LLM Lua |
| Cockpit args | Park → R4 / M6 `#24` |
| User campaigns/missions download | Park → R1–R2 |
| Installed maps | Done (M2 `#4`) |
| Historical sorties from web | Park → R3 |

**Demote for next 2–3 changes:** dynamic campaign, multiplayer, radio VO, historical
engine — stay in concept secondary / Later.

## 5. After this memo

1. BACKLOG “Next promote” → `mission-type-intercept`.
2. `/opsx:propose mission-type-intercept` on matching branch.
3. Micro-judgment after that change archives: confirm whether `agent-tools-surface` or
   intercept polish / triggers is the following step.

## 6. Follow-up note (acceptance 2026-07-26)

Intercept accepted in-game (ThirdReich/red, 6/6/1944 06:00, Average skill). When expanding
agent-facing SQLite beyond install theatres, **mission types** belong in that catalog for
list/ask flows — Spec enums + YAML remain compile SoT (see BACKLOG ideas map).
