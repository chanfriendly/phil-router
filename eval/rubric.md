# Evaluation Rubric — Phil-Router

> **Pre-registration note:** This rubric was written before any experiment runs. Criteria and weights must not be modified after data collection begins for a given phase. Add new phases freely; do not retroactively alter completed ones.

---

## Experimental Phases

| Phase | Task Type | Primary Metric | Ground Truth Source |
|---|---|---|---|
| 1 | Logical fallacy identification | Accuracy (% correct) | Standard fallacy taxonomy |
| 2 | Normative / ethical reasoning | Rubric score (human + AI-judge) | Pre-registered rubric below |
| 3 | Language framing effects | Semantic divergence score | Pairwise comparison protocol |

---

## Phase 1: Logical Fallacy Identification

### Task Format
Each prompt presents an argument. The model must:
1. Identify whether a fallacy is present (yes/no)
2. Name the fallacy type from the canonical list in `tasks/categories.md`
3. Explain why the argument commits that fallacy

### Scoring

| Metric | Description | Weight |
|---|---|---|
| **Detection accuracy** | Correct yes/no on fallacy presence | 40% |
| **Type accuracy** | Correct fallacy name from canonical list | 40% |
| **Explanation quality** | Is the stated reasoning valid? (0–2: wrong / partial / correct) | 20% |

**Composite score per response:** 0–100

**Scoring rules:**
- Type accuracy requires an exact match to canonical name OR a recognized synonym (listed in `tasks/categories.md`)
- Partial credit (1/2) for type accuracy if the model names a related fallacy category but not the specific type
- Explanation quality scored by human rater; AI-as-judge score recorded separately for comparison

### Controls Required Per Task
- **Baseline:** Same prompt, no framework routing, no system prompt modification
- **Matched:** Prompt routed through the framework deemed best-fit for logical tasks (Analytic Philosophy)
- **Mismatched:** Same prompt routed through the least-fit framework (Stoic or Virtue Ethics — pre-registered as predicted worst performers for logical tasks)

---

## Phase 2: Normative / Ethical Reasoning

### Task Format
Each prompt presents an ethical dilemma, policy question, or interpersonal scenario. The model responds under a given framework.

### Rubric (Human Rater + AI-Judge, scored independently)

Rate each dimension 1–5 using the anchors below.

#### Coherence — Does the response follow from the framework's stated principles?
- **1:** Response ignores or contradicts the framework entirely
- **2:** Framework referenced superficially; reasoning doesn't follow from it
- **3:** Framework applied inconsistently or partially
- **4:** Framework applied consistently; minor gaps
- **5:** Response is a clear, principled derivation from the framework

#### Fitness — Does this framework suit this task class?
- **1:** Framework is actively unhelpful or misleading for this task
- **2:** Framework provides marginal structure but misses core considerations
- **3:** Framework is applicable but not the strongest choice
- **4:** Framework is well-suited; illuminates the key tensions
- **5:** Framework is the natural lens for this task; provides unique insight

#### Completeness — Does the response address what the task requires?
- **1:** Major aspects of the task unaddressed
- **2:** Core addressed; significant gaps
- **3:** Adequate; minor omissions
- **4:** Thorough; trivial omissions only
- **5:** Comprehensive; nothing meaningful left unaddressed

#### Framework Fidelity — Is the response actually applying the stated framework, not just naming it?
- **1:** Framework named but not applied; generic response
- **2:** Some framework-specific terms used; reasoning not framework-derived
- **3:** Framework partially applied; some generic reasoning mixed in
- **4:** Framework clearly applied throughout; minimal drift
- **5:** Response is recognizably distinct because of the framework; would read differently under a different lens

### Composite Score
`(Coherence + Fitness + Completeness + Fidelity) / 20 × 100`

### Inter-Rater Reliability
- Human and AI-judge score independently, without seeing each other's scores
- Record both scores; calculate Cohen's kappa per dimension after first 20 responses
- If kappa < 0.6 on any dimension, the rubric anchor for that dimension must be clarified before continuing (document revision in CHANGELOG.md)

---

## Phase 3: Language Framing Effects

### Task Format
Pairs of prompts that are semantically similar but use different terminology (e.g., "be candid" vs. "be honest"). Same base task, same framework routing, only the framing word changes.

### Scoring (Pairwise Comparison)

| Metric | Description |
|---|---|
| **Lexical divergence** | Token-level difference in outputs (automated) |
| **Semantic divergence** | Embedding cosine distance between responses (automated) |
| **Tonal shift** | Human rater: does the response feel meaningfully different in register or stance? (0/1) |
| **Content delta** | Human rater: does the response cover different ground or reach different conclusions? (0/1) |

### Key Comparisons (Pre-registered)
These word pairs are selected for philosophical interest (see `frameworks/language/` for grounding):

| Pair | Philosophical distinction |
|---|---|
| candid / honest | Candor implies completeness; honesty implies truthfulness — not the same obligation |
| analyze / critique | Critique implies evaluative judgment; analyze is more neutral |
| fair / just | Justice implies a framework; fairness implies relational balance |
| persuade / convince | Persuasion can use non-rational means; conviction implies rational assent |
| explain / justify | Justification implies normative defense; explanation is descriptive |

---

## Scoring Logistics

- All raw scores stored in `experiments/YYYY-MM-DD_run-name/eval.md`
- Human rater scores entered by hand after reading outputs (not during generation)
- AI-judge scores generated via a separate API call with a structured scoring prompt (stored in `router/ai_judge_prompt.md`)
- Never run AI-judge and human scoring in the same sitting — rest period minimizes anchoring bias

---

## Pre-Registered Predictions (written 2026-04-08, before any experiment runs)

These are directional predictions, not thresholds. A result counts as confirmatory if the direction matches, regardless of effect size.

| Hypothesis | Prediction |
|---|---|
| H1 (Match wins) | Analytic Philosophy routing > Virtue Ethics routing on Phase 1 logical fallacy tasks |
| H2 (Match beats baseline) | Analytic Philosophy routing > unrouted baseline on Phase 1 |
| H3 (Any routing helps) | Mean of all framework-routed conditions > unrouted baseline on Phase 1 |
| H4 (Framing matters) | Semantically similar but lexically distinct prompts produce measurably different outputs in Phase 3 |
| H5 (Framework fit) | Matched framework routing > mismatched on Phase 2 normative tasks (Utilitarian on tradeoff tasks, Deontological on rights tasks) |
