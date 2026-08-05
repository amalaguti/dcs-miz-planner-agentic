## ADDED Requirements

### Requirement: Spec theatre binds to PyDCS terrain
The compiler MUST construct the PyDCS mission terrain from an explicit binding of Spec
theatre id → terrain factory (not a silent Channel hardcode that ignores `spec.theatre`).
When the Spec theatre has no binding, compile MUST fail with a clear unbound-theatre
error and MUST NOT emit a `.miz` that uses a different terrain silently.

#### Scenario: Channel Spec uses Channel terrain
- **WHEN** a Mission Spec with theatre `TheChannel` is compiled
- **THEN** the compiler MUST construct a PyDCS Channel terrain for the mission

#### Scenario: Unbound theatre fails compile
- **WHEN** compile is asked to use a theatre id with no terrain binding
- **THEN** compile MUST fail without writing a successful mismatched-terrain `.miz`
