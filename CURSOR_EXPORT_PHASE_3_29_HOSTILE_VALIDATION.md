# Phase 3.29 Hostile Solver Validation

Overall verdict: **FAIL**
Emergent claim supported: **False**

Solver module: `validation.solver.phase3_28_true_discovery_sim`
Solver available: `False`

## Test Verdicts

| Test | Verdict | Mode |
|---|---|---|
| solver_availability | FAIL | blocker |
| abandonment_virga_test | FAIL | retrospective_single_run |
| time_dependence_audit | FAIL | retrospective_single_run |
| metric_correlation_audit | FAIL | retrospective_single_run |
| drift_vs_convergence_test | FAIL | retrospective_single_run |
| geometry_variation_test | UNPROVEN | retrospective_unavailable |
| randomized_initial_distribution_test | UNPROVEN | retrospective_unavailable |
| frontier_authenticity_test | UNPROVEN | retrospective_unavailable |
| hidden_target_audit | UNPROVEN | retrospective_unavailable |

## Strongest Evidence Against Emergence

- Phase 3.28 solver module `validation.solver.phase3_28_true_discovery_sim` not importable. Live multi-geometry hostile tests could not run.
- Abandonment count cliff at step 11 (0.115 normalized): global synchronization.
- Particle sample shows single abandonment step for all particles: 11
- Early global abandonment cliff suggests screenplay timing, not local decay.
- Froth metric monotonic in 0.968 of steps — engineered curve shape.
- Compression metric plateau run length 19 — staircase behavior.
- Compression metric highly correlated with normalized time (0.9038).
- maxFrontierPressure saturates early and flatlines — metric ceiling theater.
- End-state particle velocities near zero after large displacement — moved then frozen, not converging.
- Solver never reached convergence in archived run despite high acceptance metrics.
- Live solver module unavailable — cannot execute multi-geometry or trajectory audit.
- Live solver module unavailable — cannot execute multi-geometry or trajectory audit.
- Live solver module unavailable — cannot execute multi-geometry or trajectory audit.
- Live solver module unavailable — cannot execute multi-geometry or trajectory audit.
- abandonment_virga_test: synchronized cliff transitions
- time_dependence_audit: monotonic/time-shaped metrics
- time_dependence_audit: synchronized cliff transitions

## Strongest Evidence For Emergence


## Suspicious Behaviors

- Archived baseline shows global abandonment cliff at step 11
- Froth metric monotonic growth with late plateau in archived run
- Compression metric staircase plateaus in archived run
- maxFrontierPressure saturates to 1.0 early in archived run
- convergenceReached=false in archived acceptance run
- End-state particle velocities near zero after large displacement (sample)

## Likely Fake-Emergence Mechanisms

- Time-shaped metric curves independent of geometry (if reproduced across shapes)
- Global abandonment synchronization
- Metric saturation ceilings (frontier pressure -> 1.0)
- Acceptance-pass despite non-convergence
- Movement then freeze pattern (high displacement, ~0 terminal velocity)
