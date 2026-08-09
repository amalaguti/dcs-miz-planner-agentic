## 1. Registry and terrain bind

- [x] 1.1 Add `Normandy` to `data/channel/theatres.yaml`
- [x] 1.2 Add `NeedsOarPoint: 28` to `data/channel/airfields.yaml`
- [x] 1.3 Bind `Normandy` → PyDCS `Normandy()` in `theatre_terrain.py`

## 2. Example Spec and fixtures

- [x] 2.1 Add `examples/needs_oar_point_cold_freeflight.yaml`
- [x] 2.2 Extend hermetic inventory helper for Normandy available + planner_supported
- [x] 2.3 Add validate/compile structure regression tests for the Normandy example

## 3. Catalog / docs

- [x] 3.1 Confirm catalog sync exposes Normandy + NeedsOarPoint; adjust catalog tests if needed
- [x] 3.2 Update README status (Normandy smoke) and BACKLOG fleet note if still incomplete
- [x] 3.3 Append LESSONS only if a non-obvious PyDCS/Normandy pitfall appears

## 4. Acceptance

- [x] 4.1 Compile example to `out/needs_oar_point_cold_freeflight.miz`
- [ ] 4.2 ME Instant Action on Normandy 2.0 (BACKLOG do-soon — prefer sooner)
