## MODIFIED Requirements

### Requirement: Spec vocabulary maps to ME predicates
The compiler SHALL map v1 Spec conditions/actions to native predicates: `time_more` to
time-after, `flag_is` to flag true/false, `unit_dead` to group-dead for the referenced
enemy flight, `target_dead` to group-dead for the referenced ground/sea target group,
`coalition_in_zone` to part-of-coalition-in-zone; `message` to delayed out-text,
`set_flag` to set/clear flag, `mission_end` to end-mission with win/lose for the player
coalition, `radio_item_add` / `radio_item_remove` to F10 radio item add/remove (flag on
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
