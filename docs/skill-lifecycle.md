# Skill Audit and Improvement Lifecycle

Use this process when a skill repeatedly misses its trigger, skips a required step, or produces an incomplete artifact. The goal is to improve observed behavior, not to optimize prose in isolation.

## 1. Record a scrubbed case

Capture the skill, trigger, intended result, observed failure, and the smallest evidence needed to reproduce it. Remove credentials, private paths, customer data, and unrelated transcript text. Do not collect or persist raw runtime transcripts automatically.

Prefer an existing case in `eval/skill_cases.json`. Add a case only when it tests a distinct behavior and has assertions that can be checked against the resulting artifact.

## 2. Audit before editing

Read the target skill, its referenced files, relevant project standards, and cases that exercise it. Report:

- Observed behavior and evidence.
- The smallest suspected instruction gap.
- Expected behavior before and after the proposed change.
- Cases that should detect a regression.

Audit is read-only. Do not rewrite a skill just because a style heuristic flags it.

## 3. Propose and approve a focused diff

Change only instructions tied to the observed gap. Preserve unrelated local edits. Show the proposed diff and affected cases; wait for approval before applying it. Do not update other skills unless a shared rule is the demonstrated cause.

## 4. Validate the change

Run the static evaluator and unit tests for the deterministic grader:

```bash
python eval/evaluator.py --tier 1 --strict
python -m unittest eval/test_skill_outcome.py
```

For an actual runtime run, invoke the case prompt from `python eval/skill_outcome.py --list`, save a scrubbed text artifact, then grade it:

```bash
python eval/skill_outcome.py engineer-review-idor /path/to/scrubbed-review.md --runtime gemini --model '<model-id>'
```

The grader records the current skill SHA-256 and checks required/forbidden artifact signals. It does not judge semantic correctness, call a model, or treat its own fixtures as agent evidence. Store real run artifacts only when they are safe to retain; otherwise keep the sanitized receipt and remove the artifact.

## 5. Compare and report honestly

Report static checks, grader self-tests, and real agent runs as separate evidence. A grader fixture passing proves only that the grader behaves as expected. A missing real run is `NOT RUN`, not a pass. Do not claim improvement unless the changed skill passes the relevant cases and no accepted behavior regresses.
