## ADDED Requirements

### Requirement: Compile populates briefing l10n
On successful compile of any supported Mission Spec (free flight, intercept, CAP,
ground-attack, escort), the compiler SHALL write Sortie, Description, and player-coalition
Task text into the `.miz` localisation dictionary per the `mission-briefing` capability.
Compile MUST accept an optional squadron voice parameter for briefing register; when
omitted, briefing text MUST use default voice `raf`. Placement, weather, radio, and
mission-type tasking behaviour MUST otherwise remain unchanged.

#### Scenario: Manston free flight includes briefing text
- **WHEN** the checked-in Manston cold free-flight Spec is compiled
- **THEN** the `.miz` MUST include non-empty Sortie and Description dictionary entries and
  a non-empty player-coalition Task, and MUST still place the player cold at Manston with
  prior acceptance behaviour

#### Scenario: Optional voice reaches briefing
- **WHEN** compile is invoked with voice `usaaf` for a valid Channel Spec
- **THEN** the written briefing Task or Description MUST use USAAF commander register
  wording from the shared brief builder
