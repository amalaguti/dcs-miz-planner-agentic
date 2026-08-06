## 1. Spec model + expander

- [x] 1.1 Add `DynamicsSpec` / pool models to Mission Spec (`mode`, `pools`, `roll`, `menu`, `exclusive`)
- [x] 1.2 Implement `expand_dynamics_if_needed` (narrative-style); XOR with narrative; reject non-empty triggers
- [x] 1.3 Wire expand into validation and compiler paths
- [x] 1.4 Validate pool indices, late_activation policy, roll min/max, mode-specific required fields

## 2. Emit modes

- [x] 2.1 Expand `live` → set_flag_random + flag branches + activate_group (+ optional message)
- [x] 2.2 Expand `choose` → radio menu + activate pools
- [x] 2.3 Expand `hybrid` → Auto dice item + menu items; `exclusive` default true
- [x] 2.4 Document / implement `fixed` behaviour (no auto dice/menu)

## 3. Example + tests

- [x] 3.1 Add example Spec (intercept or CAP) with live and/or hybrid dynamics
- [x] 3.2 Hermetic tests: expand output, conflict errors, compile smoke / golden contracts as needed
- [x] 3.3 Optional ME smoke note in tasks for acceptance
  - Accepted 2026-08-06: live → one pool after ~5s; hybrid F10 pool sizes Easy=1 / Medium=2 / Hard=4 (Auto rolls same)

## 4. Catalog + agent

- [x] 4.1 Update `dynamics_mode` planning_options support/meta for Spec-backed emit
- [x] 4.2 Schema notes + invent prompt: prefer `dynamics` when locking play-time variation; keep Layer A randomize distinct
- [x] 4.3 Tool description honesty for dynamics_mode

## 5. Docs

- [x] 5.1 BACKLOG `#30f` → building/done as appropriate; LESSONS if expand pitfalls appear
- [x] 5.2 README Status one-liner when dynamics Spec is user-visible
