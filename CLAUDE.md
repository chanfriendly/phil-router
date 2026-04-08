# CLAUDE.md — Phil-Router Development Guide

## Project Overview

**Phil-Router** is a scientific experiment testing whether routing AI tasks through different philosophical frameworks produces meaningfully different—and situationally better—outputs. The core hypothesis: philosophical frameworks function like programming languages. Each has strengths suited to particular problem classes; none is universally optimal.

The experiment maps task categories to candidate frameworks, runs them through framework-specific routing (via constitutions, soul files, skills, or system prompts), and evaluates output quality. Findings are tracked in `CHANGELOG.md`.

---

## Core Hypothesis & Research Questions

1. **Primary:** Does routing tasks through a matched philosophical framework produce measurably better outputs than unrouted or mismatched routing?
2. **Secondary:** Can a meta-router reliably classify tasks and select the appropriate framework?
3. **Exploratory:** Are some frameworks robustly better across task types, or is the advantage always situational?

---

## Philosophical Frameworks

Each framework is treated as a distinct "language" with a domain of fitness:

| Framework | Best-fit Task Categories | Routing Mechanism |
|---|---|---|
| **Utilitarianism** | Resource allocation, tradeoff analysis, policy evaluation | `frameworks/utilitarian/` |
| **Deontology (Kantian)** | Rights, duties, ethical red lines, rule-following | `frameworks/deontological/` |
| **Virtue Ethics (Aristotelian)** | Character judgment, advice, interpersonal reasoning | `frameworks/virtue/` |
| **Pragmatism (Dewey/James)** | Open-ended problem solving, experimental design, creative work | `frameworks/pragmatist/` |
| **Stoicism** | Resilience reasoning, emotional regulation, acceptance vs. action | `frameworks/stoic/` |
| **Dialectical (Hegelian)** | Synthesis tasks, debate, resolving contradictions | `frameworks/dialectical/` |

Add or remove frameworks as the experiment evolves. Document all additions and the reasoning behind them in `CHANGELOG.md`.

---

## Routing Architecture

Routing can be implemented via any of the following mechanisms (each is a valid experimental condition):

- **Constitution files** (`constitution.md` per framework): Top-level values and constraints injected at system-prompt level.
- **Soul files** (`soul.md` per framework): Character and disposition priming.
- **Claude Code Skills** (`.claude/skills/` entries): Triggerable per-framework reasoning styles.
- **System prompt injection**: Inline framework text prepended to the task.
- **Meta-router agent**: A classifier agent that reads the task and selects the best framework before routing.

The routing mechanism used in each experiment run must be recorded in `CHANGELOG.md` alongside results.

---

## Project Structure

```
phil-router/
├── CLAUDE.md               # This file — development guide and design decisions
├── CHANGELOG.md            # Lab notes, progress, failures, accuracy tables
├── frameworks/             # One subdirectory per philosophical framework
│   ├── utilitarian/
│   │   ├── constitution.md
│   │   └── soul.md
│   ├── deontological/
│   ├── virtue/
│   ├── pragmatist/
│   ├── stoic/
│   └── dialectical/
├── tasks/                  # Task category definitions and test cases
│   └── categories.md
├── experiments/            # Experiment runs — one folder per run
│   └── YYYY-MM-DD_run-name/
│       ├── config.md       # Framework, routing method, task type, model
│       ├── inputs/
│       ├── outputs/
│       └── eval.md         # Scoring and notes
├── router/                 # Meta-router logic (classification prompts, etc.)
│   └── classifier.md
└── eval/                   # Evaluation rubrics and scoring templates
    └── rubric.md
```

---

## Development Workflow

### Before Starting Any Session
1. Read `CHANGELOG.md` — current status, what's been tried, what failed.
2. Read this file — confirm you understand the active design decisions.
3. Identify the next experiment or implementation task from the changelog's `## Next Steps` section.

### During Work
- One experiment run = one meaningful unit. Don't mix framework definitions, routing logic changes, and evaluation in the same commit.
- If an approach fails, **stop and document it in `CHANGELOG.md` before pivoting.** Future sessions depend on this.
- If a design decision is made (e.g., changing how constitutions are structured), update this file.

### Commit & Push Protocol

After every meaningful unit of work that passes any applicable tests or produces interpretable results:

```bash
git add -p                          # Stage changes selectively
git commit -m "<type>: <short description>"
git push origin main
```

Commit types: `experiment`, `framework`, `router`, `eval`, `docs`, `fix`

Examples:
- `experiment: run utilitarian routing on tradeoff task batch`
- `framework: add stoic constitution and soul files`
- `eval: add pairwise rubric for ethical task category`

**Never commit an experiment run without a completed `eval.md`** — raw outputs without evaluation are not meaningful data points.

---

## Evaluation & Scoring

Outputs should be scored using the rubrics in `eval/rubric.md`. At minimum, track:

- **Coherence** (1–5): Does the response follow from the framework's logic?
- **Fitness** (1–5): Does the framework suit this task class?
- **Completeness** (1–5): Is the response thorough given the task?
- **Comparison score**: How does it rank against the unrouted baseline and mismatched-framework control?

Record accuracy/quality tables in `CHANGELOG.md` at key checkpoints.

---

## What Not To Do

- Do not conflate frameworks — each experiment run uses exactly one framework unless explicitly testing blending.
- Do not skip baseline (unrouted) runs — every task category needs a no-framework control.
- Do not mark an experiment complete without recording the results in `CHANGELOG.md`, including negative results.
- Do not change the routing mechanism mid-experiment — finish the run under the original method, then change and re-run.

---

## Design Decisions Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-04-08 | Start with 6 frameworks | Covers major Western traditions; enough diversity to find meaningful differences |
| 2026-04-08 | Track routing mechanism as an experimental variable | The *how* of routing may matter as much as the framework itself |
| 2026-04-08 | Require unrouted baseline for every task category | Without a control, no comparison is meaningful |
