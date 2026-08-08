## 1. Spec model and validation

- [x] 1.1 Extend `GroundTarget` with optional `ai_preset`, `ai` (allowlisted keys),
      and land `move_formation`; pydantic unknown-key reject; preset expand +
      explicit override rules
- [x] 1.2 Validation: class/domain allowlists (soft vs AAA vs sea) per R12;
      reject soft interception_range, sea move_formation, unknown presets
- [x] 1.3 Unit tests for omit, convoy fields, flak interception, sea reject paths

## 2. Compiler emit

- [x] 2.1 Implement Opt* emit (`OptROE`, `OptAlarmState`, `OptEngageAirWeapons`,
      `OptRestrictTargets`, `OptInterceptionRange` when allowed) on target WP0
- [x] 2.2 Apply `PointAction` for `move_formation` on land route points (motion +
      static single point); keep `#15g` disperse rules
- [x] 2.3 Compile tests: convoy Action/options evidence; U-boat ROE/Alarm;
      omit unchanged

## 3. Examples, agent, docs, accept

- [x] 3.1 Update convoy example with transit preset / Alarm / move_formation;
      add or update AAA alert example; U-boat ai roe/alarm
- [x] 3.2 Planning options cards + prompts/schema/voice notes for presets and
      class heuristics
- [x] 3.3 README / ARCHITECTURE / BACKLOG `#15h` building→done on accept; LESSONS
      if Opt*/PointAction pitfall is non-obvious
- [x] 3.4 Ruff + full pytest green
- [x] 3.5 In-game accept: ME — convoy options/Action; Flak alert options; U-boat
      ROE/Alarm; static/omit Specs unchanged
      (deferred 2026-08-08 per user: backlog do-soon ME smoke on convoy /
      flak_alert / uboat_hunt; compile+pytest green; finalize without ME fly)
