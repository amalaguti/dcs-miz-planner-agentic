## Why

Validation only checks theatre availability in the install inventory. A Spec can compile
cleanly without Spitfire / Mosquito / Bf-109 modules present, then fail when opened in
DCS (adversarial B8). Full module harvest (`#8a.1`) is still deferred; we need a thin
soft-warn for known Channel aircraft.

## What Changes

- Static map of known Channel Spec aircraft ids → expected install folders (and aliases
  such as `FW-190A8` → `FW-190A-8`).
- Probe DCS roots from inventory: present if any mapped folder exists under
  `Mods/aircraft` or `CoreMods/WWII Units` (and similar known locations).
- Soft-warn (does not fail validation) when a Spec references a known aircraft whose
  module folder is missing on all usable roots.
- Surface warnings on `ValidationResult`, CLI `validate`, and the validate tool.
- Do **not** auto-promote discovered modules into YAML/catalog (`#8a.1` stays separate).

## Non-goals

- Full aircraft module harvest / catalog listing (`#8a.1`).
- Hard-fail validate/compile on missing modules.
- Scanning every `Mods/aircraft` entry into the registry.
- Ground-unit / ship module presence checks.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `mission-validation`: Soft-warn when known Spec aircraft modules are missing from the
  local install (theatre inventory roots).

## Impact

- New `install/aircraft_modules.py` (or similar); `validation.py` / CLI / tools; tests
  with hermetic fake roots; docs/BACKLOG `#38`.
