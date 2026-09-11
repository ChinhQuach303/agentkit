---
name: cook
description: "Implement one approved plan phase with surgical minimal edits. Use when a plan or clear task is approved and the user wants code, not more discussion."
---

# Cook Skill (Implementation)

Execute the plan order, nothing else. Unplanned scope discovered mid-flight goes back to `plan` — it never sneaks into the diff.

## Hard Rules
- **PLAN-BOUND**: If code isn't in the approved phase, don't write it (YAGNI). New scope → stop, replan.
- **STANDARD LIBRARY FIRST**: Prefer builtins over new deps; <20 lines of stdlib beats a dependency.
- **ATOMIC EXECUTION**: One checklist item at a time; no multi-file refactor leaps without per-item verification.
- **PONYTAIL NOTATION**: Mark deliberate simplifications `// ponytail: <reason>` / `# ponytail: <reason>`.

## Protocol
1. **Pre-edit impact confirmation**:
   - The symbol was scouted: re-check `impact` upstream if the tree moved since scouting; confirm the edit stays inside the blast radius `plan` approved.
   - **Completion criterion:** impacted set still ⊆ approved set, or plan is updated first.
2. **Implementation**:
   - Contiguous surgical edits via replace tools; preserve docstrings, styles, and surrounding conventions.
   - Anti-pattern: **drive-by refactoring** (touching adjacent code "while here"). Tell: hunks outside the phase's files. Fix: revert, file separately.
   - **Completion criterion:** diff touches only phase files; every hunk traces to a checklist item.
3. **Continuous local validation**:
   - After each item: `ruff check <paths>` / `oxlint` / `tsc --noEmit` (whichever the repo uses) plus the item's done-means check.
   - Fix failures now; don't accumulate red across items.
   - **Completion criterion:** linters clean, each item's observable check passes.
4. **Handoff**:
   - Hand to `verify` with: changed files, per-item checks run, known risks left open.
   - **Completion criterion:** `verify` needs no re-read of the plan to start.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Need modes, mandatory review, or `--advice` checkpoints? Hand the approved plan to official `ak:cook`; this skill is the Ponytail fast-path.
