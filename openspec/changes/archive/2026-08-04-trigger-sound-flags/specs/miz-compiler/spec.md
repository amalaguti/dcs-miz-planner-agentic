## MODIFIED Requirements

### Requirement: Spec vocabulary maps to ME predicates
The compiler SHALL map v1 Spec conditions/actions to native predicates: `time_more` to
time-after, `flag_is` to flag true/false, `flag_equals` / `flag_more` / `flag_less` to
numeric flag compare, `time_since_flag` to time-since-flag, `unit_dead` to group-dead for
the referenced enemy flight, `target_dead` to group-dead for the referenced ground/sea
target group, `coalition_in_zone` to part-of-coalition-in-zone; `message` to delayed
out-text, `set_flag` to set/clear flag, `set_flag_value` / `inc_flag` to set-flag-value /
increase-flag, `mission_end` to end-mission with win/lose for the player coalition,
`sound` to sound-to-all with the resolved registry file embedded in the `.miz`
mapResource, `radio_item_add` / `radio_item_remove` to F10 radio item add/remove (flag on
for add), `activate_group` / `deactivate_group` to activate/deactivate the referenced
placed group. Groups with Spec `late_activation: true` MUST be written with ME late
activation enabled. Unsupported types MUST fail clearly before writing a `.miz`.

#### Scenario: Unknown mapping fails
- **WHEN** a future/unsupported condition type somehow reaches compile
- **THEN** compile MUST fail with a clear error and MUST NOT write a `.miz`

#### Scenario: target_dead maps to group dead
- **WHEN** a ground_attack Spec with a `target_dead` rule is compiled
- **THEN** the `.miz` MUST include a group-dead condition for the corresponding placed
  target group

#### Scenario: Radio and activate emit
- **WHEN** a Spec with `radio_item_add` and `activate_group` actions is compiled
- **THEN** the `.miz` MUST include corresponding radio-item and activate-group predicates

#### Scenario: Late activation on enemy group
- **WHEN** an enemy with `late_activation: true` is compiled
- **THEN** the placed group MUST be marked late-activated in the `.miz`

#### Scenario: Sound embeds and emits
- **WHEN** a Spec with a valid `sound` action is compiled
- **THEN** the `.miz` MUST include a sound-to-all action and MUST embed the resolved
  asset file in mission resources

#### Scenario: Numeric flag emit
- **WHEN** a Spec with `flag_more` and `inc_flag` (or `set_flag_value`) is compiled
- **THEN** the `.miz` MUST include corresponding numeric flag condition and action
  predicates
