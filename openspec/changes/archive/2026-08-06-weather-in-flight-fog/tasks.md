## 1. Spec + templates

- [x] 1.1 Add `FogDynamics` model (`burn_off` / `roll_in` + timings)
- [x] 1.2 Curated Lua template builder (params only; no free script on Spec)
- [x] 1.3 BACKLOG `#17c` → building; README one-liner

## 2. Compiler

- [x] 2.1 Emit ONCE `time_more` → `DoScriptFile` (`fog_dynamics.lua` resource) from fog_dynamics
- [x] 2.2 Wire into compile path after / with native triggers

## 3. Tests + example

- [x] 3.1 Hermetic: compiled `.miz` contains `setFogAnimation`
- [x] 3.2 Example Spec (`sea_fog` + burn_off)
- [x] 3.3 ME smoke (2026-08-06): DictKey DoScript empty → `DoScriptFile`; `sea_fog` ~1 km burn-off visible on Manston ramp

## 4. Docs

- [x] 4.1 LESSONS: DoScript DictKey + setFogAnimation / sea_fog demo pitfalls
