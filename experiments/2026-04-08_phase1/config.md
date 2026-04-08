# Experiment Config — Phase 1

**Date:** 2026-04-08
**Model:** google/gemma-4-e4b
**Experiment temperature:** 0.3
**Judge temperature:** 0
**Prompts:** 14 (12 fallacy types + 2 valid-argument controls)

## Conditions

| ID | Label | Framework |
|---|---|---|
| baseline | Baseline (no routing) | none |
| analytic | Analytic Philosophy (matched) | analytic |
| virtue | Virtue Ethics (mismatched control) | virtue |

## Pre-registered Hypotheses Under Test

- **H1:** Analytic routing > Virtue Ethics routing on fallacy identification accuracy
- **H2:** Analytic routing > unrouted baseline
- **H3:** Mean of all routed conditions > unrouted baseline

## Notes

Mismatched control is Virtue Ethics (pre-registered as worst-fit for logical tasks).
Results recorded in eval_ai.json (AI judge) and eval_human.md (human rater).
Do not compare scores until both raters have completed independently.
