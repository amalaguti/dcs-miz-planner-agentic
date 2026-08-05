# Adversarial review notes — 2026-08-05

Expert “prove it wrong” pass over agent, compiler/validation, process, tests, and
security. **Not a backlog** — raw notes for later triage into OpenSpec / BACKLOG /
LESSONS. Findings are ordered by severity within each theme.

**Claim scorecard**

| Claim | Verdict |
|-------|---------|
| AI plans; software compiles safely | **Partially true** — schema/registry gate is real; playability and recipe completeness are not enforced |
| Agent is creative & assertive via catalog/memory | **False as an invariant** — soft prompts + conflicting reminders + no emission checks; live eval already showed bare Specs |
| `validate` ≈ ready to fly in DCS | **False** — many green→broken / green→ME-fail modes |

---

## A. Agent / prompts / memory (creativity story)

### A1 — Critical — `SPEC_SHAPE_REMINDER` says `triggers (must be [])`
- **Where:** `agent/spec_schema.py` (`SPEC_SHAPE_REMINDER`); always injected via `compose_system_prompt`
- **Conflict:** Same stack tells the model to use `mission_behaviour`, zones/triggers, late_activation
- **Failure:** Model copies empty triggers from sticky reminder → bare Specs that still validate
- **Later:** Fix reminder wording; align schema examples with immersion variants

### A2 — High — Catalog + creative bias are prompt theater, not policy
- **Where:** `memory/creative.py` (`format_creative_bias_fragment` = “soft bias”); planner/session inject text only; no post-check that behaviours were emitted; `creativity_level` only truncates list length
- **Failure:** Success generations with zero immersion while product claims assertive catalog use
- **Later:** Soft→hard ladder (require N behaviours when immersion unspecified; reject/repair if prefer-list ignored). Overlaps `#30c`

### A3 — High — `infer_creative_from_spec` rewards half-recipes
- **Where:** `memory/creative.py` — any `late_activation` → `radio_late_activation` even without radio/`activate_group`
- **Failure:** Memory “prefers” a behaviour that was never fully applied; feedback loop teaches the wrong lesson
- **Later:** Infer only on complete graphs; or tag `partial:*` and exclude from prefer

### A4 — High — Schema tool examples steer to bare Specs
- **Where:** `get_mission_spec_schema` uses packaged examples without narrative/late-act/triggers; creative examples exist separately (`*_radio.yaml`, gates, etc.) but are not the schema SoT
- **Failure:** “Match that example’s structure” beats assertive prompt rules
- **Later:** Immersion variant in schema view, or point at behaviour example paths first-class

### A5 — Medium — Draft capture ≠ validated Spec
- **Where:** `session.py` — draft = Pydantic shape only; full `validate_mission_spec` on `/accept`
- **Failure:** Host banner implies Spec is good; `/accept` then fails on registry/inventory
- **Later:** Validate on capture or clarify UX (“shape OK / validation pending”)

### A6 — Medium — Stub LLM falsifies creativity demos
- **Where:** `agent/llm.py` `StubLLM` → always Manston free flight JSON; ignores tools/user
- **Failure:** CI/offline “planner works” proves nothing about assertive behaviour
- **Later:** Label stub as fixture only; creativity claims need live or scripted multi-tool fixtures

### A7 — Medium — Research soft-fail / agent vs `/research` diverge
- **Where:** Agent `research_guidance` often fixture path with weak warning; chat `/research` forces live
- **Failure:** Model treats fixtures as research; skips mission_design live sources
- **Later:** Always label `source=fixture`; align live defaults

---

## B. Validation / compiler (false green)

### B1 — Critical — Late-activation half-recipes validate + compile
- **Where:** `validation.py` (index/emptiness only); compiler sets `late_activation`; LESSONS 2026-08-05 live eval (dormant bandits)
- **Failure:** Empty sky, green CLI. `activate_group` without late_act also useless but green
- **Later:** Graph check — every late-act group reachable from activate; every activate targets late-act (error or hard warn). Core of `#30c`

### B2 — Critical — Strike land/water / domain not validated
- **Where:** `_validate_ground_attack` = unit id + coalition; placement at compile; `randomize` can jitter into water
- **Failure:** Validate green; trucks in Channel / ships inland
- **Later:** Terrain/domain probe at validate; constrain randomize envelopes

### B3 — Critical — `message.delay_s` accepted, silently ignored
- **Where:** `models.py` field; `triggers_emit.py` comment “approximated by time conditions”; OpenSpec may overclaim delayed out-text
- **Failure:** Authors/agents believe delayed ME text; message fires when `when` is true
- **Later:** Reject non-zero `delay_s` until implemented, or implement; align OpenSpec

### B4 — High — Country / skill not in validation (validate ≠ compile)
- **Where:** Compiler `_ensure_country` / `_skill_from_name`; LESSONS Germany≠ThirdReich; catalog knows countries; validation ignores
- **Failure:** Validate OK → compile `ValueError` or Axis on blue
- **Later:** Shared allowlists in validation

### B5 — High — Enemy coalition only enforced for escort (+ GA targets)
- **Where:** `_validate_escort`; intercept/CAP enemy coalition unchecked
- **Failure:** Blue “bandits” validate and compile
- **Later:** Opposing-coalition rule for intercept/CAP enemies

### B6 — High — Channel terrain hardcoded; theatre field is aspirational
- **Where:** `pydcs_compiler.py` `Mission(terrain=TheChannel())` always
- **Failure:** Adding theatre to YAML/inventory without compiler map → false confidence
- **Later:** Explicit theatre→terrain map; fail if Spec theatre ≠ bound terrain

### B7 — High — Altitude/speed gates: continuous spam + int truncation
- **Where:** Examples use `once: false`; `int(altitude_m)` in emit; LESSONS note parking spam
- **Failure:** Message flood after threshold; fractional altitudes silently truncated
- **Later:** Latch/debounce guidance or validation; document integer metres

### B8 — High — Install inventory checks theatre, not aircraft modules
- **Where:** Theatre probe only; `catalog-discover-modules` still `idea`
- **Failure:** Compile OK without Spitfire/Mosquito/109 → DCS load fail
- **Later:** Soft-warn known modules; never auto-promote into YAML

### B9 — Medium — `unit_dead` → GroupDead; late-act win conditions can stall
- **Where:** `triggers_emit.py`; narrative win on dead enemies
- **Failure:** Name implies unit; multi-ship needs full wipe; never-activated enemies → no win
- **Later:** Docs + validate “dead on late-act requires activate path”

### B10 — Medium — Intercept multi-flight stacks at one Hawkinge offset
- **Where:** `_place_enemies` fixed corridor point
- **Failure:** Radio difficulty Specs with 3 groups stacked; ME/AI glitches
- **Later:** Per-index offsets

### B11 — Medium — Dual semantic SoT (Pydantic mission rules vs `validation.py`)
- **Failure:** Drift (already different shapes for coalition rules)
- **Later:** Single semantic engine; models keep structural/`extra=forbid`

### B12 — Medium — Weather triple SoT (enum + YAML + hardcoded physics)
- **Failure:** Add preset in one place, miss another → parse fail or silent incompleteness
- **Later:** Parity test enum ⊆ YAML ⊆ planning_options ⊆ compiler cases

### B13 — Low — Flag ids are emit-order; smoke zone name vs mark zone id API oddity
- Fragile across PyDCS bumps; ME-smoke after bump

---

## C. Tool trust / security

### C1 — High — LLM tools can compile, set prefs, record history
- **Where:** `tool_bridge.py` — `compile_mission`, `set_user_prefs`, `record_generation`, `record_feedback` with no path sandbox / host confirm
- **Failure:** “Host accepts Spec” is social, not a capability boundary; confused/injected model writes disk + poisons memory
- **Later:** Read-only planning tools in chat; mutate/compile only via slash/host; path allowlist under `out/`

### C2 — High — Live research → prompt injection
- **Where:** DDG HTML snippets injected into session as synthetic user content; weak sanitization
- **Failure:** Poisoned SERP corrupts briefings/prefs; Spec gate limits `.miz` damage only
- **Later:** Delimiters + strip controls + length caps; stronger “not instructions”; prefer Instant Answer / licensed API

### C3 — Medium — Verbose default on (`#10b` still idea)
- Tool/LLM JSON to stderr; screenshot/log leakage of prompts
- **Later:** Quiet default; redact env-like strings in vlog

### C4 — Low/OK — `.env` handling
- Gitignored, shell wins, keys not in SQLite — good residual: cwd-relative `.env` only

---

## D. Process / docs / tests

### D1 — High — README Status lead is stale
- Still says “combat/trigger keys reserved for later” while M4–M6 triggers are done
- **Later:** Rewrite Status; keep-readme / finish-change missed this

### D2 — High — “Doc briefings / themes” overclaim
- **Where:** `install/campaigns.py` only lists `Doc/*.pdf` filenames — **no PDF text extract**; prompts/README say themes/briefings
- **Failure:** Agent cannot actually prefer Doc themes; `#30c` campaign/Docs ask is half-impossible
- **Later:** Downgrade claims to filenames, or propose opt-in PDF extract

### D3 — Medium — No CI; test pyramid stops before acceptance
- Goldens = zip/string contracts; PyDCS reload partial; agent = stub; no DCS ME automation; no `.github` workflows
- **Later:** Minimal CI (pytest + ruff); optional `@live_llm` / `@needs_dcs` markers

### D4 — Medium — Golden gaps for trigger-rich paths
- Radio+late-act, gates, mark/smoke, numeric flags = smoke string tests, not structural goldens
- **Later:** One golden each

### D5 — Medium — Loose `pydcs>=0.15.0` vs lock `==0.15.0` (2023 wheel) + permanent payload-scan workaround
- R8 still idea; accidental bump risk without lock discipline
- **Later:** Exact pin in pyproject until R8; bump ritual with golden refresh + ME smoke

### D6 — Medium — OpenSpec ceremony vs doc lag
- Zero active changes; `#30c` still idea; `openspec/config.yaml` may still read MVP-era
- **Later:** Thin artifacts for prompt/eval fixes; sync config context

### D7 — Low — Memory schema bump wipes prefs/history
- Looks like “creative memory doesn’t work” after upgrades
- **Later:** Migrate or warn loudly

---

## E. Intentional scope (do not “fix” — label honestly)

- Channel-only theatre / Spitfire MVP path
- No LLM-authored Lua (`#22` curated snippets only if needed)
- Campaign `.miz` not imported (index/inspiration only)
- Stub planner + offline research default for hermetic tests
- Aircraft module harvest deferred (`#8a.1`) — OK as backlog; bad if UI pretends modules are present

---

## F. Suggested triage order (for later, not committing now)

**Promoted into backlog** (2026-08-05): see `docs/BACKLOG.md` → **Adversarial review track**
`#31`–`#42` (plus expanded `#30c`). Challenge before proposing; order is a suggestion only.

1. **Honesty cheap wins:** `#31` docs-honesty-pass (+ `SPEC_SHAPE_REMINDER` with `#30c`)
2. **False-green killers:** `#32` validation-false-green
3. **`#30c` agent-assertive-behaviours**
4. **Tool boundary:** `#33` agent-tool-trust-boundary
5. **Strike domain:** `#34` strike-domain-validate
6. **Goldens + CI:** `#35` / `#36`
7. **Rest:** `#37`–`#42`, `#10b`, R8, `#8a.1`

---

## G. Cross-links

- Live creativity gaps already logged: `docs/LESSONS_LEARNED.md` (2026-08-05), BACKLOG `#30c`
- Eval harness: `.cursor/skills/eval-agent-creativity/`
- Interactive finding board: Cursor canvas `adversarial-review-2026-08-05.canvas.tsx` (project canvases folder)
