# Task Categories — Phil-Router

> This file defines task categories, test prompts, and ground truth. It must be finalized before any experiment run begins. Prompts may be added to new categories freely; do not modify prompts in a category once that category has been run.

---

## Phase 1: Logical Fallacy Identification

### Canonical Fallacy List

The following 12 fallacies constitute the ground truth taxonomy for Phase 1. Recognized synonyms are listed for scoring purposes.

| # | Canonical Name | Recognized Synonyms |
|---|---|---|
| 1 | Ad Hominem | Personal attack |
| 2 | Straw Man | Straw person |
| 3 | False Dilemma | False dichotomy, either/or fallacy |
| 4 | Slippery Slope | Domino fallacy |
| 5 | Appeal to Authority | Argument from authority |
| 6 | Circular Reasoning | Begging the question, petitio principii |
| 7 | Hasty Generalization | Overgeneralization |
| 8 | Post Hoc | Post hoc ergo propter hoc, false cause, correlation/causation |
| 9 | Appeal to Emotion | Argumentum ad passiones, emotional manipulation |
| 10 | Red Herring | Irrelevant conclusion |
| 11 | Tu Quoque | Appeal to hypocrisy, "you too" fallacy |
| 12 | Bandwagon | Appeal to popularity, ad populum |

---

### Test Prompts — Phase 1

Each prompt is labeled with its target fallacy. Labels are withheld from the model; stored here as ground truth.

**Instructions to model (same for all Phase 1 prompts):**
> Read the following argument. State whether it contains a logical fallacy. If yes, name the fallacy and explain why the argument commits it. If no fallacy is present, explain why the argument is valid.

---

**P1-01** *(Ad Hominem)*
> "We shouldn't listen to Dr. Chen's research on climate change — she drives an SUV. Clearly she doesn't even believe what she's saying."

**P1-02** *(Straw Man)*
> "My opponent says we should reduce military spending. So apparently she wants to leave our country completely defenseless and at the mercy of our enemies."

**P1-03** *(False Dilemma)*
> "You're either with us on this policy, or you're against the safety of this community. There's no middle ground."

**P1-04** *(Slippery Slope)*
> "If we allow students to redo one failed exam, next they'll want to redo every assignment, and eventually grades will become meaningless."

**P1-05** *(Appeal to Authority)*
> "A famous actor said this supplement cured his fatigue. That's good enough for me — I'll start taking it."

**P1-06** *(Circular Reasoning)*
> "The Bible is true because it says so in the Bible, and the Bible doesn't lie."

**P1-07** *(Hasty Generalization)*
> "I've met three people from that city and they were all rude. People from there are just unfriendly."

**P1-08** *(Post Hoc)*
> "I started wearing my lucky bracelet, and my back pain went away the next week. The bracelet must be healing me."

**P1-09** *(Appeal to Emotion)*
> "Think of the children growing up without clean water. How can you possibly vote against this bill?"

**P1-10** *(Red Herring)*
> "You're criticizing my business practices, but have you seen how much I donate to charity? I give thousands every year."

**P1-11** *(Tu Quoque)*
> "You're telling me I shouldn't eat junk food? You had fast food twice last week."

**P1-12** *(Bandwagon)*
> "Everyone is switching to this new platform. You should too — it's obviously the right move."

**P1-13** *(No fallacy — valid argument, control)*
> "Regular aerobic exercise has been shown in multiple peer-reviewed studies to reduce the risk of cardiovascular disease. Therefore, incorporating cardio into one's routine is likely to improve heart health."

**P1-14** *(No fallacy — valid argument, control)*
> "If the bridge was built in 1920 and the average lifespan of that construction type is 80 years, an engineering inspection is overdue."

---

## Phase 2: Normative / Ethical Reasoning

### Category Definitions

| Category | Description | Best-fit Framework (predicted) | Worst-fit Framework (predicted) |
|---|---|---|---|
| Resource allocation | Distributing limited goods, triage, budgeting | Utilitarian | Virtue Ethics |
| Rights and duties | Obligations, consent, moral red lines | Deontological | Utilitarian |
| Character and conduct | Advice, relationships, personal virtue | Virtue Ethics | Analytic Philosophy |
| Conflict resolution | Competing valid claims, synthesis | Dialectical | Stoic |
| Resilience and acceptance | Grief, loss, limits of control | Stoic | Deontological |
| Open-ended problems | Creative solutions, experimental thinking | Pragmatist | Analytic Philosophy |

### Test Prompts — Phase 2

*(To be written once Phase 1 is complete and rubric is validated. Prompts will be added here before Phase 2 begins.)*

---

## Phase 3: Language Framing Effects

### Word Pairs (Pre-registered)

See `eval/rubric.md` for philosophical grounding of each pair. Test prompts for Phase 3 use the same base task with only the framing word substituted.

**Base task template:**
> [Framing word], describe the main trade-offs involved in [scenario].

| Pair | Word A | Word B |
|---|---|---|
| 3-01 | candid | honest |
| 3-02 | analyze | critique |
| 3-03 | fair | just |
| 3-04 | persuade | convince |
| 3-05 | explain | justify |

### Test Scenarios for Phase 3

*(To be defined once Phase 1 and 2 are complete. Scenarios should be neutral enough that the framing word is the primary variable.)*

---

## Notes on Prompt Design

- Prompts within a category should be similar in length and complexity to minimize confounds
- No prompt should be identifiable as belonging to a specific framework from the wording alone
- Add new prompts at the bottom of each section; never insert mid-list (preserves run numbering)
- If a prompt is retired (found to be ambiguous or flawed), mark it `[RETIRED: reason]` rather than deleting it
