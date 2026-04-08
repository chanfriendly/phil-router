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

*Accuracy/quality tables will be recorded here after each experiment batch.*

| Date | Task Category | Framework | Routing Method | Coherence | Fitness | Completeness | vs. Baseline |
|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — |

---

## Failed Approaches

*Document what was tried, what outcome occurred, and why it was abandoned. This section is critical.*

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

1. Run classifier calibration: send all 14 Phase 1 prompts through `router/classifier.md`; confirm expected outputs; log results in classifier calibration table
2. Run first experiment: Phase 1 logical fallacy batch — baseline + Analytic (matched) + Virtue Ethics (mismatched control)
3. Score results with AI judge; then human rater scores independently
4. Calculate inter-rater reliability (human vs. AI-judge); document kappa in CHANGELOG
5. Record results in experiment results table
6. Owner to supply concrete scenario for P2-05 (Reparative Justice prompt)
7. After Phase 1 complete: write Phase 2 prompts and run Phase 2

---

## Design Decisions

| Date | Decision | Rationale |
|---|---|---|
| 2026-04-08 | Add Analytic Philosophy as 7th framework | Logical/formal tasks need a framework explicitly built around argument structure; existing 6 were too ethics-focused |
| 2026-04-08 | Plan Philosophy of Language as 8th framework (Phase 3) | Owner's core interest: how word choice ("candid" vs "honest") affects model outputs — grounded in Grice, Austin, Wittgenstein |
| 2026-04-08 | Start with logical fallacy identification (Phase 1) | Objective ground truth available; no rubric subjectivity; builds credibility before moving to normative tasks |
| 2026-04-08 | Use Qwen 3.5 9B via LM Studio as primary model | Best available local model; capable enough for nuanced philosophical reasoning |
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
**Next session should start with:** Classifier calibration run (Step 1 of Next Steps), then first experiment batch.
