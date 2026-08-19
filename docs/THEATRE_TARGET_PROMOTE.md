# Theatre & target promote checklist

Durable steps for **humans and agents** when adding a map/theatre slice or
expanding strike/recon target shelves. Do **not** dump Mission Editor unit trees
into YAML. Auto-scrape and auto-promote from install discovery stay out of scope.

Product contracts stay in OpenSpec. This file is the process checklist (`#8e`).

---

## A. New theatre / map slice

1. **Research** — R11-style audit: era, airfields, campaigns, free vs Assets Pack,
   what we will *not* support yet. Notes in gitignored `research/theatres/`.
2. **Install probe** — theatre id appears in inventory join; mark
   `planner_supported` only when a registry binding ships.
3. **Registry slice** — theatre YAML (airdromeIds, aircraft, weather as needed) +
   PyDCS terrain binding; countries/coalitions if new.
4. **Validate / compile** — shared engine accepts the theatre; one smoke Spec
   equivalent to the first Manston free-flight slice.
5. **Catalog** — `dcs-miz catalog sync`; offerable theatre appears. If invent is
   still Channel-only, update prompts/allow-lists when multi-theatre ships.
6. **Accept** — ME Instant Action on that map for the smoke Spec.
7. **Docs** — README / ARCHITECTURE / BACKLOG; LESSONS if ids or bindings were
   surprising.

Open an OpenSpec change for the batch; do not edit registry on `master` without
a change branch.

---

## B. New strike / recon target units (same or new theatre)

1. **Verify PyDCS id** — exact `vehicle_map` / `ship_map` key; domain `land`|`sea`;
   era-plausible for the theatre (Channel Spitfire ≠ every WWII id).
2. **YAML** — `ground_units.yaml` or `ships.yaml` (label + domain); never invent
   ids.
3. **Class shelf** — `strike_target_class` `unit_ids` / `ship_ids` in
   `planning_options.yaml`; set `preferred_motion` / `preferred_ai_preset` (or
   add a class row + `#15h` allowlist).
4. **Motion / AI** — speed band in `target_motion.yaml` if moving; preset/class
   rules if new domain behaviour (R12b if ME options differ).
5. **Places** — update `channel_place` (or future `theatre_place`)
   `related_classes` / cues when the unit belongs to a geography cue. Verify
   place geometry bands are correct domain (land vs sea) before invent relies on
   them.
6. **Example Spec** — at least one GA or recon example using the unit; compile +
   golden/assert as needed.
7. **Catalog** — `dcs-miz catalog sync`; `list_strike_targets` returns the id +
   class tags.
8. **Invent** — cue table / invent meta still coherent (`#8d`); extend cues if a
   new class. Path/harbour geometry lessons from `#8f`/`#8g` still apply.
9. **Accept** — ME smoke when motion/AI is non-trivial; CLI/API + hermetic tests
   enough for catalog-only adds.
10. **Docs / LESSONS** — BACKLOG class spine; pitfalls (domain mismatch, Assets
    Pack, wrong place bands).

One OpenSpec change per coherent batch (e.g. “Channel soft + AAA expand” or
“Channel sea harbour set”).

---

## Explicit non-goals

- Scraping full ME unit trees into the catalog.
- Auto-promoting discovered install folders into known YAML.
- Invent inventing Opt* names or unit strings outside allowlists.
- Treating `list_strike_targets` / catalog as a complete ME unit list.
- Auto-promoting gitignored `research/` QAG HTML (or its thin `data/qag_fixtures`
  index) into unit YAML — those pages are local research colour only until a
  `#8e` verify-then-shelf batch. Do not copy the HTML into the package.

---

## Channel class spine (candidates — not a ship list)

Expand registry over time; invent plans around these classes. **Shipped Channel
ids** live in `ground_units.yaml` / `ships.yaml` (`#8h` soft/AAA/sea; `#8i`
halftracks; `#8j` armor; `#8k` troops; `#8l` radar; `#8m` trains + rail corridor).

| Class id | Domain | Motion default | Notes |
|----------|--------|----------------|-------|
| `soft_vehicles` | land | path / patrol | Trucks / light cars as `#8h` |
| `halftracks_apc` | land | path / patrol | Sd_Kfz_251, Sd_Kfz_7, M2A1 as `#8i` |
| `armor` | land | path / patrol (static if dug-in) | Pz_IV_H, Stug_III, Cromwell, Sherman as `#8j` |
| `troops` | land | path / patrol (static if dug-in) | soldier_mauser98, wwii_br/us as `#8k` |
| `aaa_guns` | land | **static** | Flak / AT / searchlight as `#8h` |
| `artillery` | land | static (rare relocate) | LeFH_18-40-105, Wespe124, M2A1-105 (`channel-shelf-artillery`) |
| `radar_c3` | land | **static** | FuMG-401, FuSe-65 as `#8l` |
| `trains` | land | **path** on curated rail | Loco + wagons as `#8m`; `french_coast_rail_corridor` (no mesh snap) |
| `sea_craft` | sea | patrol / path; harbour → static | Ships / U-boat / cargo / tug as `#8h` |
| `hard_infrastructure` | land | **static** | Often `#17b` statics — not vehicle groups |

Era caution: prefer BoB / Channel-front plausible Axis/Allied sets when promoting.

---

## Related

- Catalog sync + `list_strike_targets`: `#8c`
- Invent cues / presets: `#8d`; geometry: `#8f`/`#8g`
- Lessons: [`LESSONS_LEARNED.md`](LESSONS_LEARNED.md) → `lessons/agent-tooling.md`
- Skill: `.cursor/skills/dcs-dev-agent-tooling`
- Multi-theatre campaign: [`BACKLOG.md`](BACKLOG.md) M7 (modern maps parked in M8);
  WWII density: M8. Orchestrator
  `.cursor/skills/full-catalog-orchestrator/SKILL.md`
