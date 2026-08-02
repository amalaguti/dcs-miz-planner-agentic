## ADDED Requirements

### Requirement: Briefing dictionary in golden coverage
Golden-fixture (or equivalent contract) coverage for Manston example compiles SHALL
include the mission localisation dictionary member `l10n/DEFAULT/dictionary` (or assert
equivalent non-empty Sortie / Description / player Task content). Empty briefing
dictionary strings MUST fail the suite after this capability ships.

#### Scenario: Dictionary member asserted
- **WHEN** a Manston example Spec is compiled under the golden harness
- **THEN** the comparison or contracts MUST require `l10n/DEFAULT/dictionary` (or
  equivalent briefing content asserts) with non-empty Sortie and player Task text
