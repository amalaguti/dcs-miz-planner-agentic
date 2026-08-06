## 1. Spec + templates

- [x] 1.1 Add `FogDynamics` model (`burn_off` / `roll_in` + timings)
- [x] 1.2 Curated Lua template builder (params only; no free script on Spec)
- [x] 1.3 BACKLOG `#17c` → building; README one-liner

## 2. Compiler

- [x] 2.1 Emit ONCE `time_more` → `DoScript` from fog_dynamics
- [x] 2.2 Wire into compile path after / with native triggers

## 3. Tests + example

- [x] 3.1 Hermetic: compiled `.miz` contains `setFogAnimation`
- [x] 3.2 Example Spec (dawn + burn_off)
- [ ] 3.3 Optional ME / Instant Action smoke (fog changes over time)

## 4. Docs

- [x] 4.1 LESSONS: DoScript + setFogAnimation pitfalls if found
