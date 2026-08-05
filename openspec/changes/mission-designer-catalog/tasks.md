## 1. Packaged designer shelves

- [ ] 1.1 Add `dynamics_mode` options (`fixed`, `live`, `choose`, `hybrid`) to `planning_options.yaml` as `advisory` with meta describing intended play-time emit (none / dice / F10 / hybrid) and Layer-A vs Layer-B note
- [ ] 1.2 Add `strike_target_class` options covering at least soft land, AAA/guns, and sea craft; meta MUST include `domain` plus verified `unit_ids` / `ship_ids` from Channel YAML and `payload_families` guidance (hard/infrastructure may be `future` without inventing ids)
- [ ] 1.3 Add `channel_place` options (Manston + ≥2 Channel geometry/place cues); meta MUST NOT invent airdromeIds

## 2. Catalog / tools verification

- [ ] 2.1 Confirm catalog sync loads the new families without schema changes (or add minimal sync/tests if anything fails)
- [ ] 2.2 Extend hermetic tests so after sync, listing/`list_mission_options` returns `dynamics_mode`, `strike_target_class`, and `channel_place` with expected ids/meta shape
- [ ] 2.3 Update `list_mission_options` tool description to mention designer shelves

## 3. Agent co-author prompts

- [ ] 3.1 Update invent/chat system guidance to require consulting the three designer families when discussing dynamics, strike composition, or Channel places
- [ ] 3.2 Document distinction: `randomize` (new Spec day) vs `dynamics_mode` (play-time palette); advisory modes are not yet Spec-emitted
- [ ] 3.3 Add/adjust prompt or tool-surface tests covering the new guidance strings

## 4. Docs closeout

- [ ] 4.1 Keep BACKLOG `#30e` as `building` until acceptance; note `#30f` consumes these shelves
- [ ] 4.2 Append LESSONS only if apply reveals a non-obvious pitfall; skim README Status if designer shelves become user-visible
