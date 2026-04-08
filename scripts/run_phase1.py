"""
run_phase1.py

Runs the Phase 1 experiment: all 14 logical fallacy prompts × 3 conditions
(baseline, analytic-matched, virtue-mismatched), then scores each response
with the AI judge and generates a human-scoring template.

Usage:
    python scripts/run_phase1.py [--dry-run]

    --dry-run   Print what would run without making API calls (for sanity check)

Output (in experiments/YYYY-MM-DD_phase1/):
    config.md         Experiment configuration and conditions
    outputs/          Raw model responses, one JSON file per prompt × condition
    eval_ai.json      AI judge scores for all responses
    eval_human.md     Blank scoring sheet for human rater (fill in after AI scores)
    results.md        Summary table — populated after both raters complete

Requirements:
    pip install openai
    LM Studio running on localhost:1234 with google/gemma-4-e4b loaded
"""

import json
import sys
import re
import random
import argparse
from datetime import date, datetime
from pathlib import Path
from openai import OpenAI

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BASE_URL  = "http://localhost:1234/v1"
MODEL     = "google/gemma-4-e4b"
TEMP_EXPERIMENT = 0.3   # slight variation for responses (not deterministic)
TEMP_JUDGE      = 0     # deterministic scoring

REPO_ROOT    = Path(__file__).parent.parent
PROMPTS_FILE = REPO_ROOT / "tasks" / "phase1_prompts.json"
FRAMEWORKS   = REPO_ROOT / "frameworks"
EXP_DIR      = REPO_ROOT / "experiments" / f"{date.today()}_phase1"

TASK_INSTRUCTION = (
    "Read the following argument. State whether it contains a logical fallacy. "
    "If yes, name the fallacy and explain why the argument commits it. "
    "If no fallacy is present, explain why the argument is valid."
)

CONDITIONS = [
    {
        "id":          "baseline",
        "label":       "Baseline (no routing)",
        "framework":   None,
        "description": "No system prompt; model reasons without philosophical framing.",
    },
    {
        "id":          "analytic",
        "label":       "Analytic Philosophy (matched)",
        "framework":   "analytic",
        "description": "Routed through Analytic Philosophy — pre-registered as best-fit for logical tasks.",
    },
    {
        "id":          "virtue",
        "label":       "Virtue Ethics (mismatched control)",
        "framework":   "virtue",
        "description": "Routed through Virtue Ethics — pre-registered as worst-fit for logical tasks.",
    },
]

# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def ok(t):   return f"{GREEN}{t}{RESET}"
def fail(t): return f"{RED}{t}{RESET}"
def warn(t): return f"{YELLOW}{t}{RESET}"
def info(t): return f"{CYAN}{t}{RESET}"
def bold(t): return f"{BOLD}{t}{RESET}"

# ---------------------------------------------------------------------------
# Framework loader
# ---------------------------------------------------------------------------

def load_framework_system_prompt(framework_id):
    """Combine constitution.md and soul.md into a single system prompt."""
    framework_dir = FRAMEWORKS / framework_id
    constitution  = (framework_dir / "constitution.md").read_text().strip()
    soul          = (framework_dir / "soul.md").read_text().strip()
    return f"{constitution}\n\n---\n\n{soul}"

# ---------------------------------------------------------------------------
# API calls
# ---------------------------------------------------------------------------

def run_experiment_call(client, system_prompt, task_text, dry_run=False):
    """Run one experiment call. Returns response text or None."""
    if dry_run:
        return "[DRY RUN — no API call made]"
    messages = [{"role": "user", "content": task_text}]
    if system_prompt:
        messages.insert(0, {"role": "system", "content": system_prompt})
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            temperature=TEMP_EXPERIMENT,
            messages=messages,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(fail(f"    API error: {e}"))
        return None


AI_JUDGE_SYSTEM = """You are evaluating a response to a logical fallacy identification task.

Score the response on three dimensions:

Detection (0 or 1): Did the response correctly identify whether a fallacy was present?
  0 = incorrect   1 = correct

Type accuracy (0, 0.5, or 1): Did the response correctly name the fallacy?
  0   = wrong or not attempted
  0.5 = named a related fallacy category but not the specific type
  1   = correct (exact match or recognized synonym)

Explanation quality (0, 1, or 2): Is the explanation of why the fallacy occurs valid?
  0 = explanation is wrong or absent
  1 = explanation is partially correct or imprecise
  2 = explanation correctly identifies the logical error

Respond ONLY in this exact JSON format — no other text:
{
  "detection": <0 or 1>,
  "type_accuracy": <0, 0.5, or 1>,
  "explanation_quality": <0, 1, or 2>,
  "composite": <detection*40 + type_accuracy*40 + explanation_quality*10>,
  "notes": "<one sentence or empty string>"
}"""

def run_judge_call(client, task_text, response_text, ground_truth, dry_run=False):
    """Run AI judge on one response. Returns parsed score dict or None."""
    if dry_run:
        return {"detection": 0, "type_accuracy": 0, "explanation_quality": 0,
                "composite": 0, "notes": "DRY RUN"}

    has_fallacy  = ground_truth["has_fallacy"]
    fallacy_name = ground_truth["fallacy"] or "N/A"

    user_msg = (
        f"Ground truth: The argument {'CONTAINS' if has_fallacy else 'DOES NOT CONTAIN'} a fallacy. "
        f"Correct fallacy type: {fallacy_name}\n\n"
        f"Task shown to model:\n{task_text}\n\n"
        f"Response to evaluate:\n{response_text}"
    )
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            temperature=TEMP_JUDGE,
            messages=[
                {"role": "system", "content": AI_JUDGE_SYSTEM},
                {"role": "user",   "content": user_msg},
            ],
        )
        raw = resp.choices[0].message.content.strip()
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            print(warn(f"      Judge: no JSON in response"))
            return None
        return json.loads(match.group())
    except Exception as e:
        print(fail(f"      Judge error: {e}"))
        return None

# ---------------------------------------------------------------------------
# File writers
# ---------------------------------------------------------------------------

def write_config(exp_dir, conditions):
    config = f"""# Experiment Config — Phase 1

**Date:** {date.today()}
**Model:** {MODEL}
**Experiment temperature:** {TEMP_EXPERIMENT}
**Judge temperature:** {TEMP_JUDGE}
**Prompts:** 14 (12 fallacy types + 2 valid-argument controls)

## Conditions

| ID | Label | Framework |
|---|---|---|
"""
    for c in conditions:
        config += f"| {c['id']} | {c['label']} | {c['framework'] or 'none'} |\n"

    config += """
## Pre-registered Hypotheses Under Test

- **H1:** Analytic routing > Virtue Ethics routing on fallacy identification accuracy
- **H2:** Analytic routing > unrouted baseline
- **H3:** Mean of all routed conditions > unrouted baseline

## Notes

Mismatched control is Virtue Ethics (pre-registered as worst-fit for logical tasks).
Results recorded in eval_ai.json (AI judge) and eval_human.md (human rater).
Do not compare scores until both raters have completed independently.
"""
    (exp_dir / "config.md").write_text(config)


def write_human_scoring_template(exp_dir, prompts, all_outputs):
    """Generate a markdown file the human rater fills in."""
    lines = [
        "# Human Scoring — Phase 1\n",
        f"**Rater:** _______________  **Date scored:** _______________\n",
        "> Score each response independently. Do not look at AI judge scores first.",
        "> Detection: 0=wrong, 1=correct | Type: 0/0.5/1 | Explanation: 0/1/2\n",
        "---\n",
    ]

    for prompt in prompts:
        pid = prompt["id"]
        gt_fallacy = prompt["fallacy"] or "(none — valid argument)"
        lines.append(f"## {pid} — Ground truth: {gt_fallacy}\n")
        lines.append(f"**Argument:** {prompt['text']}\n")

        for condition in CONDITIONS:
            cid = condition["id"]
            key = f"{pid}_{cid}"
            response = all_outputs.get(key, "[no response]")
            lines.append(f"### Condition: {condition['label']}\n")
            lines.append(f"**Response:**\n\n{response}\n")
            lines.append(
                "**Human scores:**  \n"
                "Detection (0/1): ___  \n"
                "Type accuracy (0 / 0.5 / 1): ___  \n"
                "Explanation quality (0/1/2): ___  \n"
                "Composite (auto): ___  \n"
                "Notes: ___\n"
            )
        lines.append("---\n")

    (exp_dir / "eval_human.md").write_text("\n".join(lines))


def write_results_template(exp_dir, prompts, ai_scores):
    """Write results.md with AI scores pre-filled; human column blank."""
    lines = [
        "# Results — Phase 1\n",
        f"**Date:** {date.today()}  **Model:** {MODEL}\n",
        "AI scores filled in automatically. Human scores to be added after independent rating.\n",
        "| Prompt | Fallacy | Condition | Det (AI) | Type (AI) | Exp (AI) | Score (AI) | Score (Human) |",
        "|---|---|---|---|---|---|---|---|",
    ]

    for prompt in prompts:
        pid = prompt["id"]
        fallacy = prompt["fallacy"] or "(valid)"
        for condition in CONDITIONS:
            cid = condition["id"]
            key = f"{pid}_{cid}"
            s = ai_scores.get(key)
            if s:
                det  = s.get("detection", "—")
                typ  = s.get("type_accuracy", "—")
                exp  = s.get("explanation_quality", "—")
                comp = s.get("composite", "—")
            else:
                det = typ = exp = comp = "ERROR"
            lines.append(
                f"| {pid} | {fallacy} | {condition['label']} | "
                f"{det} | {typ} | {exp} | {comp} | ___ |"
            )

    lines.append("\n## Aggregate by Condition\n")
    lines.append("*(Fill in after both raters complete)*\n")
    lines.append("| Condition | Mean Score (AI) | Mean Score (Human) | Pass Rate |")
    lines.append("|---|---|---|---|")
    for condition in CONDITIONS:
        lines.append(f"| {condition['label']} | ___ | ___ | ___ |")

    lines.append("\n## Hypothesis Outcomes\n")
    lines.append("*(Complete after scoring)*\n")
    lines.append("| Hypothesis | Direction | Confirmed? | Notes |")
    lines.append("|---|---|---|---|")
    lines.append("| H1 | Analytic > Virtue | ___ | ___ |")
    lines.append("| H2 | Analytic > Baseline | ___ | ___ |")
    lines.append("| H3 | Any routing > Baseline | ___ | ___ |")

    (exp_dir / "results.md").write_text("\n".join(lines))

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would run without making API calls")
    args = parser.parse_args()
    dry_run = args.dry_run

    print(bold(f"\n=== Phil-Router: Phase 1 Experiment {'(DRY RUN) ' if dry_run else ''}==="))
    print(f"Model      : {MODEL}")
    print(f"Conditions : {len(CONDITIONS)} (baseline, analytic, virtue)")
    print(f"Prompts    : 14")
    print(f"Total calls: {14 * len(CONDITIONS)} experiment + up to {14 * len(CONDITIONS)} judge")
    print(f"Output     : {EXP_DIR.relative_to(REPO_ROOT)}\n")

    # Setup
    prompts = json.loads(PROMPTS_FILE.read_text())
    client  = OpenAI(base_url=BASE_URL, api_key="lm-studio")

    EXP_DIR.mkdir(parents=True, exist_ok=True)
    (EXP_DIR / "outputs").mkdir(exist_ok=True)
    write_config(EXP_DIR, CONDITIONS)

    # Pre-load framework system prompts
    framework_prompts = {}
    for condition in CONDITIONS:
        if condition["framework"]:
            framework_prompts[condition["id"]] = load_framework_system_prompt(
                condition["framework"]
            )

    all_outputs = {}   # key: "P1-01_baseline" → response text
    ai_scores   = {}   # key: "P1-01_baseline" → score dict

    # Shuffle prompt order within each condition to reduce order effects
    shuffled = prompts[:]
    random.seed(42)  # fixed seed for reproducibility
    random.shuffle(shuffled)

    # ---------------------------------------------------------------------------
    # Experiment loop
    # ---------------------------------------------------------------------------
    for condition in CONDITIONS:
        cid    = condition["id"]
        label  = condition["label"]
        sysprompt = framework_prompts.get(cid)   # None for baseline

        print(bold(f"\n── Condition: {label} ──"))

        for prompt in shuffled:
            pid       = prompt["id"]
            task_text = f"{TASK_INSTRUCTION}\n\n\"{prompt['text']}\""
            fallacy   = prompt["fallacy"] or "(valid)"

            print(f"  {pid}  {fallacy:<22}", end=" ", flush=True)

            response = run_experiment_call(client, sysprompt, task_text, dry_run)

            if response:
                print(ok("✓"))
                key = f"{pid}_{cid}"
                all_outputs[key] = response

                # Save raw output
                output_file = EXP_DIR / "outputs" / f"{key}.json"
                output_file.write_text(json.dumps({
                    "prompt_id":   pid,
                    "condition":   cid,
                    "fallacy":     prompt["fallacy"],
                    "has_fallacy": prompt["has_fallacy"],
                    "task_text":   task_text,
                    "response":    response,
                    "timestamp":   datetime.now().isoformat(),
                }, indent=2))
            else:
                print(fail("✗"))

    # ---------------------------------------------------------------------------
    # AI Judge loop
    # ---------------------------------------------------------------------------
    print(bold("\n── AI Judge Scoring ──"))

    for condition in CONDITIONS:
        cid = condition["id"]
        for prompt in prompts:
            pid = prompt["id"]
            key = f"{pid}_{cid}"

            if key not in all_outputs:
                continue

            print(f"  Judging {key:<25}", end=" ", flush=True)
            score = run_judge_call(
                client,
                task_text=f"{TASK_INSTRUCTION}\n\n\"{prompt['text']}\"",
                response_text=all_outputs[key],
                ground_truth=prompt,
                dry_run=dry_run,
            )

            if score:
                ai_scores[key] = score
                composite = score.get("composite", "?")
                print(ok(f"score={composite}"))
            else:
                print(fail("error"))

    # ---------------------------------------------------------------------------
    # Write output files
    # ---------------------------------------------------------------------------
    (EXP_DIR / "eval_ai.json").write_text(json.dumps(ai_scores, indent=2))
    write_human_scoring_template(EXP_DIR, prompts, all_outputs)
    write_results_template(EXP_DIR, prompts, ai_scores)

    # ---------------------------------------------------------------------------
    # Console summary
    # ---------------------------------------------------------------------------
    print(bold("\n── Summary ──\n"))
    print(f"{'Condition':<35} {'Mean Score':>10}  {'Pass Rate (≥60)':>15}")
    print("-" * 65)

    for condition in CONDITIONS:
        cid    = condition["id"]
        scores = [
            ai_scores[f"{p['id']}_{cid}"]["composite"]
            for p in prompts
            if f"{p['id']}_{cid}" in ai_scores
        ]
        if scores:
            mean_score = sum(scores) / len(scores)
            pass_rate  = sum(1 for s in scores if s >= 60) / len(scores) * 100
            print(f"{condition['label']:<35} {mean_score:>10.1f}  {pass_rate:>14.0f}%")
        else:
            print(f"{condition['label']:<35} {'—':>10}  {'—':>15}")

    print(f"\nFiles written to: {EXP_DIR.relative_to(REPO_ROOT)}/")
    print(f"  config.md         — experiment configuration")
    print(f"  outputs/          — {len(all_outputs)} raw response files")
    print(f"  eval_ai.json      — AI judge scores")
    print(f"  eval_human.md     — human scoring template (fill in independently)")
    print(f"  results.md        — summary table (AI scores pre-filled, human column blank)")

    if not dry_run:
        print(warn("\nNext step: open eval_human.md and score responses independently before comparing with AI scores."))


if __name__ == "__main__":
    main()
