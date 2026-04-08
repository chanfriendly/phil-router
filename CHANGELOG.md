# CHANGELOG — Phil-Router Lab Notes

> This file is the agent's portable long-term memory. Every session should begin by reading this file and end by updating it. Document what worked, what didn't, and why. Without failed approaches recorded here, future sessions will repeat the same dead ends.

---

## Current Status

**Phase:** Setup / Pre-experiment  
**Last updated:** 2026-04-08  
**Active focus:** Establishing framework definitions and baseline task categories before first experiment run.

---

## Completed Work

### 2026-04-08
- Initialized repository at `GitHub/phil-router/`
- Wrote `CLAUDE.md` with project overview, framework table, routing architecture, and commit protocol
- Established 6 starting frameworks: Utilitarian, Deontological, Virtue Ethics, Pragmatist, Stoic, Dialectical
- Added **Analytic Philosophy** as 7th framework (best fit for logical/formal reasoning tasks)
- Added **Philosophy of Language** as 8th planned framework (Phase 3 — framing/word-choice effects; Grice, Austin, Wittgenstein)
- Defined project directory structure
- Wrote `eval/rubric.md` — pre-registered rubric for all 3 phases before any experiments run
- Wrote `tasks/categories.md` — 14 Phase 1 prompts (12 fallacy types + 2 valid-argument controls), framework-category fit predictions
- Wrote `frameworks/analytic/constitution.md` and `soul.md`
- Wrote `frameworks/deontological/constitution.md` and `soul.md`
- Selected **Qwen 3.5 9B** (via LM Studio) as primary experiment model
- Pre-registered 5 hypotheses (H1–H5) in `eval/rubric.md` before data collection

---

## Experiment Results

### Phase 1 — Logical Fallacy Identification (2026-04-08)

**Model:** google/gemma-4-e4b  **Prompts:** 14 (12 fallacy types + 2 valid-argument controls)

| Condition | Mean Score (AI, corrected) | Pass Rate | False Positives | Human Score |
|---|---|---|---|---|
| Baseline (no routing) | **100.0** | 100% | 0 | pending |
| Analytic Philosophy (matched) | **92.9** | 93% | P1-13 | pending |
| Virtue Ethics (mismatched) | **94.3** | 93% | P1-14 | pending |

**AI judge note:** Judge (same model as experiment) miscalculated composites — reported 70s/90s where formula gives 100. Corrected composites computed from sub-scores (detection×40 + type×40 + explanation×10). Sub-scores appear reliable; composites were not.

**H1 (Analytic > Virtue):** Not confirmed — Virtue edged Analytic 94.3 vs 92.9  
**H2 (Analytic > Baseline):** Not confirmed — Baseline was perfect; routing lowered performance  
**H3 (Any routing > Baseline):** Not confirmed — mean routed 93.6 vs baseline 100.0  

**Key finding:** Routed models introduced false positives on valid-argument control prompts (P1-13 analytic, P1-14 virtue). Analytic framing appears to bias toward problem-seeking. Analytic also misnamed P1-02 (called Slippery Slope instead of Straw Man). Human scoring required before drawing conclusions.

---

## Failed Approaches

*Document what was tried, what outcome occurred, and why it was abandoned. This section is critical.*

| Date | Approach | What Happened | Why Abandoned |
|---|---|---|---|
| 2026-04-08 | AI-as-judge composite self-calculation | Judge (Gemma 4B) reported composites inconsistent with its own sub-scores — gave 70/90 where formula gives 100 | Not abandoned — sub-scores are reliable; composites now recomputed externally. Lesson: never trust LLM-computed arithmetic; always verify from sub-scores. |
| 2026-04-08 | Qwen 3.5 9B as primary model | LM Studio blocked load — 8.14 GB exceeds memory guardrail | Switched to Gemma 4 4B. Flag as limitation: smaller model may show weaker or different framework effects. |

| Date | Approach | What Happened | Why Abandoned |
|---|---|---|---|
| — | — | — | — |

---

## Known Limitations

*Ongoing constraints and open questions about the experimental design.*

- **Evaluation subjectivity:** Scoring rubric (coherence, fitness, completeness) involves judgment calls. Inter-rater reliability not yet established.
- **Model consistency:** Results may vary across Claude model versions. Pin model ID per experiment run.
- **Framework fidelity:** Constitutions/soul files are approximations of philosophical traditions. A philosophy expert should review them before trusting results.
- **Task category coverage:** Starting task set is not exhaustive. Coverage gaps should be documented here as they're discovered.

---

## Framework Definition Status

| Framework | Constitution | Soul | Status |
|---|---|---|---|
| Analytic Philosophy | constitution.md | soul.md | Complete |
| Deontological | constitution.md | soul.md | Complete |
| Utilitarian | constitution.md | soul.md | Complete |
| Virtue Ethics | constitution.md | soul.md | Complete |
| Pragmatist | constitution.md | soul.md | Complete |
| Stoic | constitution.md | soul.md | Complete |
| Dialectical | constitution.md | soul.md | Complete |
| Philosophy of Language | — | — | Planned (Phase 3) |

---

## Task Category Status

| Category | Description | Baseline Run | Notes |
|---|---|---|---|
| — | — | — | — |

---

## Next Steps

1. **In progress:** Phase 1 experiment run
2. **After run:** open `experiments/YYYY-MM-DD_phase1/eval_human.md` and score independently
3. **Score:** open `experiments/YYYY-MM-DD_phase1/eval_human.md` and score responses independently (before looking at AI scores)
4. Fill in human column in `results.md`; calculate inter-rater kappa; document in CHANGELOG
5. Record aggregate results in experiment results table above
6. Assess H1–H3 outcomes; write them into results.md
7. After Phase 1 complete: run Phase 2

---

## Design Decisions

| Date | Decision | Rationale |
|---|---|---|
| 2026-04-08 | Add Analytic Philosophy as 7th framework | Logical/formal tasks need a framework explicitly built around argument structure; existing 6 were too ethics-focused |
| 2026-04-08 | Plan Philosophy of Language as 8th framework (Phase 3) | Owner's core interest: how word choice ("candid" vs "honest") affects model outputs — grounded in Grice, Austin, Wittgenstein |
| 2026-04-08 | Start with logical fallacy identification (Phase 1) | Objective ground truth available; no rubric subjectivity; builds credibility before moving to normative tasks |
| 2026-04-08 | Switch primary model to Gemma 4 4B (google/gemma-4-e4b) | Qwen 3.5 9B requires 8.14 GB and is blocked by LM Studio's memory guardrail on this machine; Gemma 4B loads successfully and passed 14/14 classifier calibration at high confidence |
| 2026-04-08 | Pre-register H1–H5 before any data collection | Distinguishes confirmatory from exploratory findings; required for publishability |
| 2026-04-08 | Both human + AI-as-judge scoring; human is ground truth | AI judge is fast but biased; human is authoritative; comparison between them is itself a data point |

---

## Session Log

### Session 001 — 2026-04-08
**Goal:** Repository initialization and project scaffold  
**Outcome:** Completed. `CLAUDE.md` and `CHANGELOG.md` created. Directory structure planned.

### Session 002 — 2026-04-08
**Goal:** Pre-registration, rubric, task prompts, first two framework definitions  
**Outcome:** Completed. `eval/rubric.md` written with 5 pre-registered hypotheses. 14 Phase 1 prompts written. Analytic and Deontological frameworks complete.

### Session 003 — 2026-04-08
**Goal:** Remaining framework files, meta-router, AI-judge scoring prompt  
**Outcome:** Completed. All 7 frameworks now have constitution.md and soul.md. `router/classifier.md` and `router/ai_judge_prompt.md` written. Phase 2 prompts P2-01 through P2-04 added; P2-05 is a placeholder pending owner scenario.

### Session 004 — 2026-04-08
**Goal:** Classifier calibration script and first calibration run  
**Outcome:** Completed. `scripts/calibrate_classifier.py` written; `tasks/phase1_prompts.json` structured data file created. Qwen 3.5 9B blocked (8.14 GB, exceeds system memory guardrail) — switched to Gemma 4 4B. Calibration: **14/14 PASS**, all high confidence. Results saved to `experiments/calibration/2026-04-08_classifier_calibration.json`.

### Session 005 — 2026-04-08
**Goal:** Phase 1 experiment runner script  
**Outcome:** Completed. `scripts/run_phase1.py` written — 42 experiment calls (14 prompts × 3 conditions) + 42 AI judge calls, with randomized prompt order (seed=42). Generates config.md, raw outputs/, eval_ai.json, eval_human.md (human scoring template), and results.md. Dry run passed. `tasks/phase2_prompts.json` created with P2-05 as placeholder.

### Session 006 — 2026-04-08
**Goal:** Finalize P2-05 and launch Phase 1  
**Outcome:** P2-05 finalized. Phase 1 run complete — 42/42 API calls succeeded. Baseline=100.0, Analytic=92.9, Virtue=94.3 (corrected from AI judge sub-scores). H1/H2/H3 tentatively not confirmed. Key finding: routed models produced false positives on valid-argument controls. AI judge composite arithmetic unreliable — recomputed externally.  
**Next session should start with:** Human scoring — open `experiments/2026-04-08_phase1/eval_human.md` and score all 42 responses independently before looking at `eval_ai.json`. Then fill human column in `results.md` and calculate inter-rater kappa.
