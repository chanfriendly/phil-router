"""
calibrate_classifier.py

Runs all Phase 1 prompts through the meta-router classifier and verifies
that each is correctly classified as framework=analytic, task_category=logical.

Usage:
    python scripts/calibrate_classifier.py

Output:
    - Console table with pass/fail per prompt
    - JSON results saved to experiments/calibration/YYYY-MM-DD_classifier.json
    - Summary appended to router/classifier.md calibration log

Requirements:
    pip install openai
    LM Studio running on localhost:1234 with qwen/qwen3.5-9b loaded
"""

import json
import sys
import re
from datetime import date
from pathlib import Path
from openai import OpenAI

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BASE_URL = "http://localhost:1234/v1"
MODEL = "google/gemma-4-e4b"
TEMPERATURE = 0  # deterministic

REPO_ROOT = Path(__file__).parent.parent
PROMPTS_FILE = REPO_ROOT / "tasks" / "phase1_prompts.json"
RESULTS_DIR = REPO_ROOT / "experiments" / "calibration"
CLASSIFIER_MD = REPO_ROOT / "router" / "classifier.md"

TASK_INSTRUCTION = (
    "Read the following argument. State whether it contains a logical fallacy. "
    "If yes, name the fallacy and explain why the argument commits it. "
    "If no fallacy is present, explain why the argument is valid."
)

CLASSIFIER_SYSTEM = """You are a philosophical framework classifier. Your job is to read a task and identify which philosophical framework is best suited to reason through it. You do not answer the task itself — you only classify it.

Available frameworks:
- analytic: Logical analysis, argument structure, fallacy identification, formal validity, conceptual clarification
- deontological: Rights, duties, obligations, consent, moral red lines, rules that hold regardless of outcome
- utilitarian: Resource allocation, tradeoffs, maximizing well-being, cost-benefit, policy evaluation
- virtue: Character, personal conduct, relationships, advice, what a good person would do
- pragmatist: Open-ended problem solving, experimental thinking, what actually works, creative approaches
- stoic: Grief, loss, resilience, acceptance vs. action, limits of control, equanimity
- dialectical: Resolving contradictions, synthesis of opposing views, debate, exposing hidden assumptions

Classification rules:
1. Choose exactly one framework — the strongest single match.
2. If two frameworks are close, note the secondary match in the "secondary" field.
3. If the task clearly belongs to Phase 3 (word-framing study), classify it as "language_framing" regardless of other content.
4. Do not be influenced by the topic alone — classify by what kind of reasoning the task requires, not what it is about.

Respond in this exact JSON format:
{
  "framework": "<framework name>",
  "secondary": "<framework name or null>",
  "task_category": "<logical | normative_ethical | normative_relational | applied_reasoning | language_framing>",
  "confidence": "<high | medium | low>",
  "rationale": "<one sentence explaining the classification>"
}"""

# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

def color(text, code):
    return f"{code}{text}{RESET}"

def ok(text):   return color(text, GREEN)
def fail(text): return color(text, RED)
def warn(text): return color(text, YELLOW)
def bold(text): return color(text, BOLD)

# ---------------------------------------------------------------------------
# Classifier call
# ---------------------------------------------------------------------------

def classify(client, task_text):
    """Send a task to the classifier. Returns parsed JSON dict or None on error."""
    user_message = f"Classify the following task:\n\n<task>\n{task_text}\n</task>"
    try:
        response = client.chat.completions.create(
            model=MODEL,
            temperature=TEMPERATURE,
            messages=[
                {"role": "system", "content": CLASSIFIER_SYSTEM},
                {"role": "user",   "content": user_message},
            ],
        )
        raw = response.choices[0].message.content.strip()
        # Extract JSON block if wrapped in markdown code fences
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            print(warn(f"  Could not find JSON in response:\n  {raw[:200]}"))
            return None
        return json.loads(match.group())
    except json.JSONDecodeError as e:
        print(warn(f"  JSON parse error: {e}"))
        return None
    except Exception as e:
        print(fail(f"  API error: {e}"))
        return None

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(result):
    """Return (passed, issues) where passed is bool and issues is a list of strings."""
    issues = []
    if result is None:
        return False, ["No parseable response"]
    if result.get("framework") != "analytic":
        issues.append(f"framework={result.get('framework')} (expected analytic)")
    if result.get("task_category") != "logical":
        issues.append(f"task_category={result.get('task_category')} (expected logical)")
    return len(issues) == 0, issues

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(bold("\n=== Phil-Router: Classifier Calibration ==="))
    print(f"Model : {MODEL}")
    print(f"Date  : {date.today()}")
    print(f"Goal  : All 14 Phase 1 prompts → framework=analytic, task_category=logical\n")

    # Load prompts
    prompts = json.loads(PROMPTS_FILE.read_text())
    print(f"Loaded {len(prompts)} prompts from {PROMPTS_FILE.name}\n")

    # Connect to LM Studio
    client = OpenAI(base_url=BASE_URL, api_key="lm-studio")

    results = []
    passed = 0
    failed = 0

    print(f"{'ID':<8} {'Expected Fallacy':<22} {'Framework':<14} {'Category':<14} {'Confidence':<10} {'Status'}")
    print("-" * 85)

    for prompt in prompts:
        pid = prompt["id"]
        fallacy_label = prompt["fallacy"] if prompt["fallacy"] else "(none — valid)"

        # Build the full task text as the model would see it
        task_text = f"{TASK_INSTRUCTION}\n\n\"{prompt['text']}\""

        result = classify(client, task_text)
        valid, issues = validate(result)

        if valid:
            passed += 1
            status = ok("PASS")
        else:
            failed += 1
            status = fail("FAIL")

        framework = result.get("framework", "—") if result else "ERROR"
        category  = result.get("task_category", "—") if result else "ERROR"
        confidence = result.get("confidence", "—") if result else "ERROR"

        print(f"{pid:<8} {fallacy_label:<22} {framework:<14} {category:<14} {confidence:<10} {status}")
        if issues:
            for issue in issues:
                print(f"         {warn('→ ' + issue)}")

        results.append({
            "id": pid,
            "fallacy": prompt["fallacy"],
            "has_fallacy": prompt["has_fallacy"],
            "classifier_output": result,
            "passed": valid,
            "issues": issues,
        })

    # Summary
    print("-" * 85)
    total = len(prompts)
    pct = passed / total * 100
    summary_color = ok if passed == total else (warn if passed >= total * 0.8 else fail)
    print(f"\n{bold('Result:')} {summary_color(f'{passed}/{total} passed ({pct:.0f}%)')}")

    if passed == total:
        print(ok("Classifier calibration complete. Ready to run Phase 1 experiments.\n"))
    else:
        print(warn(f"{failed} prompt(s) misclassified. Review before running experiments.\n"))

    # Save JSON results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_file = RESULTS_DIR / f"{date.today()}_classifier_calibration.json"
    out_file.write_text(json.dumps({
        "date": str(date.today()),
        "model": MODEL,
        "passed": passed,
        "failed": failed,
        "total": total,
        "results": results,
    }, indent=2))
    print(f"Results saved → {out_file.relative_to(REPO_ROOT)}")

    # Append to calibration log in classifier.md
    append_to_calibration_log(results)

    return 0 if passed == total else 1


def append_to_calibration_log(results):
    """Append rows to the calibration table in router/classifier.md."""
    today = str(date.today())
    md = CLASSIFIER_MD.read_text()

    new_rows = []
    for r in results:
        out = r["classifier_output"] or {}
        framework = out.get("framework", "ERROR")
        category  = out.get("task_category", "ERROR")
        match = "YES" if r["passed"] else "NO"
        new_rows.append(
            f"| {today} | {r['id']} ({r['fallacy'] or 'valid'}) "
            f"| analytic / logical | {framework} / {category} | {match} |"
        )

    marker = "| — | — | — | — | — |"
    if marker in md:
        md = md.replace(marker, "\n".join(new_rows), 1)
    else:
        # Marker already replaced — append after last row in the table
        rows_block = "\n".join(new_rows)
        md = md + f"\n{rows_block}"

    CLASSIFIER_MD.write_text(md)
    print(f"Calibration log updated → {CLASSIFIER_MD.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
