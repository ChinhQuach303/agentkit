# Skill Standard (single source of truth for all skills)

Distilled from `mattpocock/skills` levers (`writing-for-agents`, `code-review`, `tdd`, `diagnosing-bugs`).
Every skill rewrite is reviewed against this file. Changing a rule = editing here first.

> Scope rule: **Ponytail constrains code, never plans.** `cook`/`fix` stay minimal;
> `frame`/`plan`/artifacts stay full and explicit. A "lean" skill below means lean
> prose, not thin decisions.

## 0. Invocation axis

- **User-invoked** (`frame`): orchestrates, interviews, owns the session flow. Triggered by the user naming the outcome.
- **Model-invoked** (rest): reusable discipline the agent reaches for when the task fits, or the chain calls explicitly.
- A user-invoked skill may call model-invoked ones, never the reverse direction for flow control.

## 1. Description is a trigger pointer, not a phase label

- List the **branches** that should trigger the skill: `Use when the user says X / mentions Y / wants Z`.
- Front-load the leading verb. BAD: `"Phase 5: Multi-axis review..."`. GOOD: `"Review the diff since a fixed point along two axes... Use when the user asks to review a branch, a PR, or work-in-progress."`
- No synonyms for one branch; collapse and keep genuinely distinct branches.

## 2. Every phase ends on a completion criterion

- Format: `**Completion criterion:** <observable state>` — clarity (agent can tell done from not-done) + demand (forces legwork, e.g. "one already-run command", not "understanding reached").
- A phase without one invites premature completion → FAIL in eval.

## 3. Concrete commands beat tool names

- ≥3 runnable backtick spans per skill (`git diff A...HEAD`, `guard.sh "<cmd>"`, `pytest -q path`, `ak-eval ...`).
- Naming a tool (`GitNexus`, `rtk`) without an invocation is a cache of nothing — either show the call or drop the mention.
- Prefer environment lookups over restated config (`--help` output, `package.json` scripts).

## 4. Anti-patterns carry tells

- Each anti-pattern: name → what it looks like → the tell (how you know it's happening) → the fix.
- Example shape: "**Tautological**: assertion recomputes the value the way the code does. Tell: passes by construction, can never disagree. Fix: expected values from an independent source."

## 5. Ordered lookups, not single sources

- Where >1 source can answer (spec location, symbol lookup, standards), list the order 1→N and what to do when all miss (ask, skip with note — never silently continue).

## 6. Redact secrets (REDACT_SET)

- Skills that show commands/outputs — `debug, verify, review, ship, deploy, scan, pipeline-opt, experiment-run, promote-gate` — carry a Redact rule: `<REDACTED>` placeholders, env vars for credentials, quote only signal lines.
- If redacted output is insufficient, the skill says so and asks the user. No silent proceeding.

## 7. User checkpoints, not just gates

- Ask for what only the user/higher-context can give: fixed point, seam confirmation, hypothesis ranking. Cheap checkpoint, big time saver. Don't block on AFK — proceed with stated ranking.

## 8. Progressive disclosure (refs earn their place)

- Only 4 skills earn sibling refs: `debug/loop-catalog.md`, `review/smells.md`, `verify/seam-guide.md`, `model-eval/slice-catalog.md`.
- Bar: inline what every branch needs; disclose what only some branches reach. No placeholder dirs.

## 9. Voice: positive, leading words, pruned

- Prompt the positive target ("write one-line comments"), not the prohibition — bans only as hard guardrails, paired with the positive.
- Reuse leading words (`tight`, `red`, `seam`, `tracer bullet`) instead of restating triads.
- Delete no-ops (instruction the model obeys by default) and caches (restated env). One meaning lives in one place.

## 10. Tier budgets

- Deep (debug, review, verify, plan, data-audit, model-eval): 80–140 lines + at most 1 ref.
- Lean (scout, cook, ship, fix, frame, deploy, scan, pipeline-opt, experiment-run, promote-gate): 50–70 lines, inline only.
