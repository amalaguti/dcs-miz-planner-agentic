## Why

We need a first vertical slice that proves the architecture: a declarative Mission Spec compiles to a valid DCS `.miz` that loads and flies. Without that, later agent tooling and combat mission types have nothing trustworthy to build on. The Manston cold free flight is the smallest acceptance mission already agreed in the backlog.

## What Changes

- Add a Python 3.12 + uv project skeleton for the mission planner.
- Introduce a minimal Mission Spec for free-flight missions (Channel / Spitfire / Manston cold parking / 09:00 / sunny).
- Implement a deterministic compiler path (PyDCS behind a narrow interface) that writes a `.miz`.
- Provide a simple CLI/entry point to compile a checked-in example spec to a `.miz`.
- Document how to open/verify the result in the DCS Mission Editor / Instant Action.

## Non-goals

- Natural-language agent or conversational mission planning.
- Combat mission types (intercept, CAP, escort, ground attack).
- Full reference registry, validation engine, or golden fixture suite beyond what this slice needs.
- VEAF MCP integration or embedded mission Lua frameworks.
- Normandy / other theatres; clipped-wing `SpitfireLFMkIXCW`; multiplayer.

## Capabilities

### New Capabilities

- `mission-spec`: Declarative Mission Spec contract for a Channel Spitfire free-flight mission (player, airfield, start type, time, weather).
- `miz-compiler`: Deterministic compilation of a free-flight Mission Spec into a playable `.miz` via PyDCS.

### Modified Capabilities

- (none — `openspec/specs/` is empty)

## Impact

- New Python package managed with uv; dependency on PyDCS.
- New example Mission Spec artifact and generated `.miz` output path (repo `out/` or documented Saved Games path).
- Acceptance depends on DCS World with The Channel map and Spitfire LF Mk IX installed.
- README / backlog status should reflect that the first compile path exists once this change ships.
