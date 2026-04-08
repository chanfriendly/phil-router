# Results — Phase 1

**Date:** 2026-04-08  **Model:** google/gemma-4-e4b

> AI composite scores are **corrected** from sub-scores (detection×40 + type×40 + explanation×10).
> The AI judge miscalculated its own composites — reported 90s/70s where sub-scores compute to 100.
> Human column to be filled in independently before comparing.

| Prompt | Fallacy | Condition | Det | Type | Exp | Score (AI corrected) | Score (Human) |
|---|---|---|---|---|---|---|---|
| P1-01 | Ad Hominem | Baseline (no routing) | 1 | 1 | 2 | 100 | ___ |
| P1-01 | Ad Hominem | Analytic Philosophy (matched) | 1 | 1 | 2 | 100 | ___ |
| P1-01 | Ad Hominem | Virtue Ethics (mismatched) | 1 | 1 | 2 | 100 | ___ |
| P1-02 | Straw Man | Baseline (no routing) | 1 | 1 | 2 | 100 | ___ |
| P1-02 | Straw Man | Analytic Philosophy (matched) | 1 | 0.5 | 2 | 80.0 | ___ |
| P1-02 | Straw Man | Virtue Ethics (mismatched) | 1 | 1 | 2 | 100 | ___ |
| P1-03 | False Dilemma | Baseline (no routing) | 1 | 1 | 2 | 100 | ___ |
| P1-03 | False Dilemma | Analytic Philosophy (matched) | 1 | 1 | 2 | 100 | ___ |
| P1-03 | False Dilemma | Virtue Ethics (mismatched) | 1 | 1 | 2 | 100 | ___ |
| P1-04 | Slippery Slope | Baseline (no routing) | 1 | 1 | 2 | 100 | ___ |
| P1-04 | Slippery Slope | Analytic Philosophy (matched) | 1 | 1 | 2 | 100 | ___ |
| P1-04 | Slippery Slope | Virtue Ethics (mismatched) | 1 | 1 | 2 | 100 | ___ |
| P1-05 | Appeal to Authority | Baseline (no routing) | 1 | 1 | 2 | 100 | ___ |
| P1-05 | Appeal to Authority | Analytic Philosophy (matched) | 1 | 1 | 2 | 100 | ___ |
| P1-05 | Appeal to Authority | Virtue Ethics (mismatched) | 1 | 1 | 2 | 100 | ___ |
| P1-06 | Circular Reasoning | Baseline (no routing) | 1 | 1 | 2 | 100 | ___ |
| P1-06 | Circular Reasoning | Analytic Philosophy (matched) | 1 | 1 | 2 | 100 | ___ |
| P1-06 | Circular Reasoning | Virtue Ethics (mismatched) | 1 | 1 | 2 | 100 | ___ |
| P1-07 | Hasty Generalization | Baseline (no routing) | 1 | 1 | 2 | 100 | ___ |
| P1-07 | Hasty Generalization | Analytic Philosophy (matched) | 1 | 1 | 2 | 100 | ___ |
| P1-07 | Hasty Generalization | Virtue Ethics (mismatched) | 1 | 1 | 2 | 100 | ___ |
| P1-08 | Post Hoc | Baseline (no routing) | 1 | 1 | 2 | 100 | ___ |
| P1-08 | Post Hoc | Analytic Philosophy (matched) | 1 | 1 | 2 | 100 | ___ |
| P1-08 | Post Hoc | Virtue Ethics (mismatched) | 1 | 1 | 2 | 100 | ___ |
| P1-09 | Appeal to Emotion | Baseline (no routing) | 1 | 1 | 2 | 100 | ___ |
| P1-09 | Appeal to Emotion | Analytic Philosophy (matched) | 1 | 1 | 2 | 100 | ___ |
| P1-09 | Appeal to Emotion | Virtue Ethics (mismatched) | 1 | 1 | 2 | 100 | ___ |
| P1-10 | Red Herring | Baseline (no routing) | 1 | 1 | 2 | 100 | ___ |
| P1-10 | Red Herring | Analytic Philosophy (matched) | 1 | 1 | 2 | 100 | ___ |
| P1-10 | Red Herring | Virtue Ethics (mismatched) | 1 | 1 | 2 | 100 | ___ |
| P1-11 | Tu Quoque | Baseline (no routing) | 1 | 1 | 2 | 100 | ___ |
| P1-11 | Tu Quoque | Analytic Philosophy (matched) | 1 | 1 | 2 | 100 | ___ |
| P1-11 | Tu Quoque | Virtue Ethics (mismatched) | 1 | 1 | 2 | 100 | ___ |
| P1-12 | Bandwagon | Baseline (no routing) | 1 | 1 | 2 | 100 | ___ |
| P1-12 | Bandwagon | Analytic Philosophy (matched) | 1 | 1 | 2 | 100 | ___ |
| P1-12 | Bandwagon | Virtue Ethics (mismatched) | 1 | 1 | 2 | 100 | ___ |
| P1-13 | (valid) | Baseline (no routing) | 1 | 1 | 2 | 100 | ___ |
| P1-13 | (valid) | Analytic Philosophy (matched) | 0 | 0.5 | 2 | 40.0 | ___ |
| P1-13 | (valid) | Virtue Ethics (mismatched) | 1 | 1 | 2 | 100 | ___ |
| P1-14 | (valid) | Baseline (no routing) | 1 | 1 | 2 | 100 | ___ |
| P1-14 | (valid) | Analytic Philosophy (matched) | 1 | 0.5 | 2 | 80.0 | ___ |
| P1-14 | (valid) | Virtue Ethics (mismatched) | 0 | 0 | 2 | 20 | ___ |

## Aggregate by Condition (AI judge, corrected composites)

| Condition | Mean Score | Pass Rate (≥60) | False Positives |
|---|---|---|---|
| Baseline (no routing) | 100.0 | 100% | none |
| Analytic Philosophy (matched) | 92.9 | 93% | P1-13 |
| Virtue Ethics (mismatched) | 94.3 | 93% | P1-14 |

## Hypothesis Outcomes (pending human scoring)

| Hypothesis | Prediction | AI result | Confirmed? | Notes |
|---|---|---|---|---|
| H1 | Analytic > Virtue | 92.9 vs 94.3 | **No** | Virtue edged analytic by 1.4 points |
| H2 | Analytic > Baseline | 92.9 vs 100.0 | **No** | Baseline perfect; analytic lower |
| H3 | Any routing > Baseline | 93.6 avg vs 100.0 | **No** | Routing hurt performance |

## Key Observations

- **Baseline was perfect (100.0):** No false positives; correct detection, type, and explanation on all 14 prompts.
- **Routed models introduced false positives on valid arguments:** P1-13 (analytic) and P1-14 (virtue) both detected fallacies where none exist.
- **Failure mode hypothesis:** Analytic framing ('find ambiguity', 'resist taking claims at face value') and virtue framing may bias the model toward problem-seeking even when arguments are sound.
- **Type error (analytic, P1-02):** Analytic routing named Slippery Slope for a Straw Man argument — possible over-application of the 'slippery slope' heuristic from the constitution.
- **Methodological flag:** AI judge is same model as experiment (Gemma 4B). Same-model judging may introduce bias. Human scores are the authoritative measure.
- **AI judge composite error:** Judge miscalculated its own composite scores (reported 70s/90s where formula gives 100). Sub-scores were used for corrected composites above.