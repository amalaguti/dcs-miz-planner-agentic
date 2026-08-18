## 1. Registry and example

- [x] 1.1 Extend `data/theatres/Falklands/airfields.yaml` to the eight
      curated keys (comments: PyDCS names/classes; do not dump 27; ids 4
      and 28 absent)
- [x] 1.2 Add `Argentina` to `data/era/modern/countries.yaml` only (not WWII)
- [x] 1.3 Add `examples/rio_gallegos_cold_freeflight.yaml` (RioGallegos,
      Argentina red, Su-25T, 2024-06-06 09:00 sunny_clear). Leave
      `mount_pleasant_cold_freeflight.yaml` UK blue.

## 2. Infer and tools

- [x] 2.1 Extend `infer_theatre` to the eight Falklands Spec keys; keep
      `Mount_Pleasant`; do not add other underscore aliases
- [x] 2.2 Confirm `find_airfield` is theatre-scoped (RioGallegos 5 ≠
      Manston 5; PortStanley lookup-only; underscore keys unknown)

## 3. Tests and docs

- [x] 3.1 Registry tests: eight AFs exact set; RioGallegos 5 vs Manston;
      MountPleasant 2 vs GroomLake/Merville; `Rio_Gallegos` /
      `Port_Stanley` unknown; Argentina modern; Channel+Argentina unknown;
      Chile still unknown; ids 4 and 28 not in curated set
- [x] 3.2 Validate+compile Rio Gallegos N1 contracts
      (`airdromeId=5`, Argentina, Falklands theatre, 251.0, cold, 32400);
      invent still FF-only at MountPleasant; schema blob must not cite
      rio_gallegos example as home
- [x] 3.3 Update BACKLOG F5b, README extra-AF list, LESSONS (`channel-ids`),
      matching skills; next promote `falklands-places`
- [x] 3.4 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
