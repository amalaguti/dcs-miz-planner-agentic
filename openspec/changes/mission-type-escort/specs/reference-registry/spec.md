## ADDED Requirements

### Requirement: Package aircraft in Channel registry
The Channel reference registry SHALL expose exact DCS aircraft type ids usable as escort
package aircraft, including at least `MosquitoFBMkVI` with a documented Allied VHF group
radio default. Keys MUST match PyDCS plane ids; the registry MUST NOT invent spellings.

#### Scenario: Mosquito lookup
- **WHEN** a caller requests aircraft `MosquitoFBMkVI` from the Channel registry
- **THEN** the registry MUST return the aircraft reference including a radio frequency in
  the Allied VHF band
