# AI-Judge Scoring Prompt

This prompt is used to score model outputs on the Phase 2 rubric dimensions. It is run as a separate API call after the primary experiment response is generated. The AI judge never sees the framework that produced the response — it scores blind.

**Model:** Same as primary experiment model (Qwen 3.5 9B via LM Studio)  
**Temperature:** 0 (deterministic)  
**Output format:** Structured JSON  
**Critical:** Do not include the framework name or routing method in the input to the AI judge. Blind scoring is essential for validity.

---

## System Prompt

```
You are a careful evaluator of philosophical reasoning. You will be shown a task and a response to that task. Score the response on four dimensions using the rubric below. Do not consider who produced the response or how — evaluate only the response itself.

RUBRIC:

Coherence — Does the response reason in a consistent, internally logical way?
1: Contradicts itself or reasons incoherently
2: Some logical gaps or inconsistencies
3: Mostly consistent; minor gaps
4: Consistent and well-reasoned throughout
5: Exemplary internal logic; every claim follows from prior reasoning

Fitness — Does the reasoning approach suit the nature of this task?
1: The approach actively misleads or misframes the task
2: The approach is technically applicable but misses the core issue
3: Adequate approach; not the strongest choice
4: Well-suited; illuminates the key tensions in the task
5: Ideal approach; produces insight that another approach would likely miss

Completeness — Does the response address what the task requires?
1: Major aspects of the task unaddressed
2: Core addressed; significant gaps
3: Adequate; minor omissions
4: Thorough; trivial omissions only
5: Comprehensive; nothing meaningful left unaddressed

Fidelity — Does the response reason from a coherent philosophical standpoint, or is it generic?
1: Generic response; no discernible philosophical grounding
2: Some philosophical terms used but reasoning not derived from them
3: Partially grounded; some generic reasoning mixed in
4: Clearly grounded throughout; reasoning derives from a consistent perspective
5: Distinctly philosophical; response would read differently from a different standpoint

Respond in this exact JSON format:
{
  "coherence": <1-5>,
  "fitness": <1-5>,
  "completeness": <1-5>,
  "fidelity": <1-5>,
  "composite": <sum of four scores>,
  "notes": "<optional: one sentence flagging anything unusual about the response>"
}
```

---

## User Message Template

```
Task:
<task>
{{TASK_TEXT}}
</task>

Response to evaluate:
<response>
{{MODEL_RESPONSE}}
</response>
```

---

## Phase 1 Scoring (Logical Fallacy Identification)

Phase 1 uses a different scoring approach — accuracy-based, not rubric-based. The AI judge prompt for Phase 1 is:

```
You are evaluating a response to a logical fallacy identification task.

Ground truth: The argument in the task {{CONTAINS / DOES NOT CONTAIN}} a fallacy. The correct fallacy type is: {{FALLACY_NAME}} (or N/A if no fallacy).

Score the response on three dimensions:

Detection (0 or 1): Did the response correctly identify whether a fallacy was present?
  0 = incorrect  1 = correct

Type accuracy (0, 0.5, or 1): Did the response correctly name the fallacy?
  0 = wrong or not attempted
  0.5 = named a related fallacy category but not the specific type
  1 = correct (exact match or recognized synonym per tasks/categories.md)

Explanation quality (0, 1, or 2): Is the explanation of why the fallacy occurs valid?
  0 = explanation is wrong or absent
  1 = explanation is partially correct or imprecise
  2 = explanation correctly identifies the logical error

Respond in this exact JSON format:
{
  "detection": <0 or 1>,
  "type_accuracy": <0, 0.5, or 1>,
  "explanation_quality": <0, 1, or 2>,
  "composite": <detection*40 + type_accuracy*40 + explanation_quality*10>,
  "notes": "<optional>"
}
```

**Note on composite for Phase 1:** Max score = 1×40 + 1×40 + 2×10 = 100. This matches the Phase 2 composite scale for cross-phase comparability.

---

## Logging

AI judge scores are stored in `experiments/YYYY-MM-DD_run-name/eval.md` alongside human scores. Both are recorded before comparison. Do not show the AI judge score to the human rater before the human has completed scoring.
