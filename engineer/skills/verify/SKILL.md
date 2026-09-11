---
name: verify
description: "Phase 4: Test suite execution and blast radius change detection before claiming success."
---

# Verify Skill (Phase 4: Verification & Blast Radius)

The Verify workflow provides concrete proof of correctness and ensures no unintended side effects were introduced.

## Hard Rules
- **EVIDENCE BEFORE ASSERTIONS**: Never claim code works without running verification commands.
- **GRAPH INTEGRITY CHECK**: Run `gitnexus detect-changes` before commit when available; otherwise `git status/diff` (degraded mode OK).

## Protocol
1. **Automated Test Execution**:
   - Run relevant unit, integration, and regression test suites.
   - Use `rtk` to filter and compress test logs when running large suites.
2. **Blast Radius Validation**:
   - Run GitNexus `detect_changes` (MCP) when available; fallback `gitnexus detect-changes --scope all --repo .` or `git status/diff` in degraded mode.
   - Verify that changes ONLY touched expected symbols and execution flows.
   - If unexpected symbols are flagged as affected, halt and investigate regression risk.
3. **Fail-Closed Gate**:
   - If tests fail, drop into `debug` skill mode: reproduce -> isolate -> fix -> re-verify.
4. **Handoff**:
    - Once 100% tests pass and blast radius matches the plan, proceed to the `review` phase.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Prefer official `ak:test` for independent validation; this skill folds test + blast-radius into one pass.
