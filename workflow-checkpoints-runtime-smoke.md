# Skill Stage Checkpoints and Runtime Smoke Tests

## Goal
Require user confirmation after every workflow stage across all 16 skills, and add a read-only smoke test for Gemini, Claude Code, OpenCode, and Codex that distinguishes runtime discovery evidence from file-presence checks.

## Tasks
- [x] Define the shared stage-checkpoint rule in `docs/skill-standard.md` and add it to all 16 skill `Hard Rules` → Verify: every skill requires a result report and explicit approval before the next stage or skill handoff. **Done:** added the shared rule to all 16 skills; approval covers only the next stage.
- [x] Extend `eval/evaluator.py` static validation for stage checkpoints → Verify: removing the checkpoint rule from any skill causes Tier 1 failure. **Done:** Tier 1 now fails a skill missing the marker/rule.
- [x] Implement an opt-in runtime smoke test with runtime-specific discovery checks and explicit `unsupported/unverified` results → Verify: no prompt/model call, no persistent config mutation, and each runtime's reported evidence is bounded and identifiable. **Done:** `eval/runtime_smoke.py` installs into disposable HOME directories and runs local CLI discovery; Claude remains unverified because no safe inventory CLI is available.
- [x] Document invocation, per-runtime limits, and meaning of results in README → Verify: examples work as shown; docs never equate file presence with runtime discovery. **Done:** documented smoke command and Claude limitation.
- [x] Run static evaluator, Tier 2 lifecycle tests, runtime smoke for all four CLIs, JSON/shell validation, and diff review → Verify: all applicable checks pass; missing discovery evidence is reported as unverified, not pass. **Done:** evaluator Tier 1 155/0, Tier 2 29/0, Tier 3 135/135; Gemini/OpenCode/Codex discovery PASS; Claude UNVERIFIED; Python compile, bash syntax, and diff check passed.

## Decisions
- Checkpoint rule applies to every skill and every numbered Protocol stage; approval covers only the next stage.
- Runtime smoke is opt-in, invokes no model, and installs only inside disposable temporary HOME directories.
- Gemini CLI and Antigravity have distinct discovery roots; installer links both, while runtime smoke verifies Gemini CLI's `~/.gemini/skills` route.
- Use currently installed runtime CLIs; skip missing runtimes and report unavailable capability honestly. Claude reports `UNVERIFIED` because its CLI has no non-interactive skill inventory surface.
