## ADDED Requirements

### Requirement: Modern ground units and Su-25T payload in era package
The packaged registry SHALL load ground units and named payloads from each
`data/era/<era>/` package when those YAML files exist (`wwii` and `modern`).
Era `modern` SHALL include PyDCS vehicle ids `Ural-375`, `GAZ-66`, and
`ZIL-135` (domain land) and payload preset `su25t_2x_fab250` (aircraft
`Su-25T`, FAB-250 CLSID `{3C612111-C7AD-476E-8A8E-2485812F4E5C}` on inner
pylons 5 and 7). Duplicate ids across eras with differing refs MUST fail
load. WWII ground units and Spitfire payloads MUST remain in the WWII era
package. The registry MUST NOT invent vehicle ids or CLSIDs.

#### Scenario: Modern trucks registered
- **WHEN** the registry lists ground units
- **THEN** it MUST include `Ural-375`, `GAZ-66`, and `ZIL-135` and MUST still
  include WWII `Blitz_36-6700A`

#### Scenario: Su-25T FAB-250 preset resolves
- **WHEN** the registry is queried for `su25t_2x_fab250`
- **THEN** it MUST return aircraft `Su-25T` and FAB-250 CLSID on pylons 5 and 7
