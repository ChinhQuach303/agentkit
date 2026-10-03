# Skill Outcome Evaluation and Improvement Loop

## Goal
Add a deterministic, offline grader and small artifact-based corpus for manual real-runtime skill runs, plus a reviewed audit/update lifecycle that stores no raw session transcripts.

## Tasks
- [x] Define a versioned corpus with four representative engineer/scientist scenarios and artifact assertions → Verify: each case names its skill, prompt, required evidence, and disallowed claim. **Done:** four cases cover review, verification, leakage audit, and promotion integrity.
- [x] Add a stdlib grader that reports assertions without printing artifact contents → Verify: pass/fail fixtures and malformed inputs are covered by unit tests. **Done:** grader emits assertion IDs and skill SHA only; three unit tests cover corpus, positive/negative outputs, and forbidden claims.
- [x] Document the scrubbed audit → proposed diff → approval → regression-evaluation workflow → Verify: no automatic transcript collection or skill writes are prescribed. **Done:** added `docs/skill-lifecycle.md` with manual, scrubbed, approval-gated process.
- [x] Integrate corpus/test commands and honest evaluation limits into README and skill standard → Verify: docs distinguish grader self-tests from real agent outcome evidence. **Done:** documented manual real runs and limitations; no model is run by the grader.
- [x] Run grader tests, prior evaluator, four-runtime smoke, Python/shell validation, and diff review → Verify: all checks pass, and no model is called. **Done:** grader unit tests (3 pass), Tier 1 (155 pass), runtime smoke remains Gemini/OpenCode/Codex PASS and Claude UNVERIFIED; compile/JSON/diff checks pass.
