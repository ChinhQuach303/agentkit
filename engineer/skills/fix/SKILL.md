---
name: fix
description: "Apply the smallest repair for a proven root cause, then lock it with a regression test. Use when debug has named the cause and the user wants the minimal patch, not a refactor."
---

# Fix Skill (Cause-Aligned Minimal Repair)

One cause, one patch. Anything else in the diff is scope creep wearing a fix costume.

## Hard Rules
- **CAUSE-ALIGNED ONLY**: Touch only lines responsible for the proven bug. No bundled refactoring, formatting, or features.
- **PONYTAIL MINIMAL FOOTPRINT**: Builtins/stdlib before new helpers; contiguous edits; `// ponytail:` / `# ponytail:` on the why.
- **NO PROOF, NO FIX**: Unproven cause → back to `debug`. A fix without a repro command is a guess.

## Protocol
1. **Verify root-cause prerequisites**:
   - Repro command exists and goes red; root-cause report names lines + mechanism.
   - Anti-pattern: **fix-first debugging** (patching the first plausible line). Tell: no red command, no ranked hypotheses. Fix: stop, run `debug`.
   - **Completion criterion:** repro red on demand; cause cited by file:line.
2. **Surgical implementation**:
   - Patch exactly the cited lines; preserve docstrings and neighbors.
   - Confirm minimality after: `git diff --stat` must show only the cause area; record the base with `git rev-parse HEAD` in the report.
   - **Completion criterion:** diff contains the cause lines and nothing unrelated.
3. **Lock with regression test**:
   - Write the test BEFORE the final pass when a correct seam exists: must exercise the real bug pattern at the call site (single-caller unit for a multi-caller chain = false confidence — say so and flag the architecture instead).
   - Watch it fail, apply fix, watch it pass: `pytest -q <test>`, then the relevant suite.
   - **Completion criterion:** red→green observed and recorded; suite counts attached.
4. **Deliverable**:
   - Minimal diff + repro command + test output, ready for `verify` or `review`.
   - **Completion criterion:** reviewer sees cause → patch → proof with zero re-derivation.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Same contract as official `ak:fix` (smallest cause-aligned repair); interchangeable.
