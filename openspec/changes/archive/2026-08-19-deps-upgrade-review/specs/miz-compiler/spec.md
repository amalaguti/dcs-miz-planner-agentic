## ADDED Requirements

### Requirement: Git-pinned PyDCS does not bind new theatres
Pinning pydcs to a git revision that contains additional terrain classes (including `Kola` and Cold War Germany) MUST NOT add Spec theatre bindings. Compile and validation MUST still fail closed for unbound theatre ids. The compiler MUST NOT construct `Kola()` (or other unbound terrains) from a Spec.

#### Scenario: Kola Spec still fails compile
- **WHEN** compile is asked to use theatre id `Kola` after pydcs is git-pinned
- **THEN** compile MUST fail with an unbound-theatre error and MUST NOT write a Kola `.miz`

### Requirement: Payload-directory scan stays disabled until proven
The compiler MUST keep the install payload-directory scan disabled (`_disable_payload_scan` or equivalent) after the git pin, unless a recorded compile with a real DCS World install present succeeds with scanning enabled. Ground-attack loadouts MUST continue to use registry CLSIDs. Free-flight, intercept, and CAP compile MUST remain independent of install payload lua.

#### Scenario: Default compile still disables payload scan
- **WHEN** a Mission Spec is compiled with a DCS install detectable by PyDCS
- **THEN** the compiler MUST NOT rely on scanning the install `UnitPayloads` directory unless LESSONS records that scan-on was proven green for that pin

## MODIFIED Requirements

### Requirement: Compile intercept at Mount Pleasant
The compiler SHALL compile a Falklands intercept Mission Spec that
cold-starts the player Su-25T at Mount Pleasant and places opposition on the
packaged South Atlantic corridor (Mount Pleasant + 150° / 40 km). Channel
Hawkinge/Dover literals MUST stay bit-identical.

#### Scenario: Mount Pleasant intercept contracts
- **WHEN** `examples/mount_pleasant_dawn_intercept.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Falklands`, player type `Su-25T`,
  `airdromeId` 2, start_time 21600, player radio 251.0 MHz, country
  `Argentina` when enemies are present, and enemy map position
  38677.30416162246 / 67168.748047 (MUST NOT contain Channel 30989.935547)

### Requirement: Compile ground_attack at Mount Pleasant
The compiler SHALL compile a Falklands ground_attack Mission Spec that
cold-starts the player Su-25T at Mount Pleasant with payload
`su25t_2x_fab250` and places Argentina Ural-375 (and companions) at 269° /
21 km / 2000 m. It MUST bind PyDCS `Falklands` terrain. It MUST NOT write
Channel 125/76, Syria 121/200, Caucasus 43/110, Nevada 303/85, or CAP 150/40
station 38677.30416162246 / 67168.748047 as the required destination.

#### Scenario: Mount Pleasant ground_attack contracts
- **WHEN** `examples/mount_pleasant_east_falkland_ground_attack.yaml` is
  compiled
- **THEN** the `.miz` MUST contain theatre `Falklands`, player type `Su-25T`,
  `airdromeId` 2, start_time 32400, player radio 251.0 MHz, Ground Attack
  tasking, FAB-250, country `UK` on the player, and country `Argentina` on
  the trucks (MUST NOT contain Channel 30989.935547 or CAP station
  38677.30416162246)

### Requirement: Compile recon at Mount Pleasant
The compiler SHALL compile a Falklands recon Mission Spec that cold-starts
the player Su-25T at Mount Pleasant and places an observe AOI at the packaged
East Falkland inland station (269° / 21 km / 2000 m) with Ural-375 contacts
country Argentina. It MUST bind PyDCS `Falklands` terrain. It MUST NOT write
Channel Manston french-coast 125/76, Syria Aleppo 121/200, Caucasus Kutaisi
43/110, Nevada Creech 303/85, or the Falklands CAP 150/40 station
38677.30416162246 / 67168.748047 as the required AOI.

#### Scenario: Mount Pleasant East Falkland recon contracts
- **WHEN** `examples/mount_pleasant_east_falkland_recon.yaml` is compiled
- **THEN** the `.miz` MUST contain theatre `Falklands`, player type `Su-25T`,
  `airdromeId` 2, cold parking, start_time 32400, player radio 251.0 MHz,
  Reconnaissance tasking, `recon_aoi`, country `UK` on the player, and
  country `Argentina` on land contacts (MUST NOT contain Channel 30989.935547
  or CAP station 38677.30416162246)
