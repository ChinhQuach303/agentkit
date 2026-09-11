---
name: cook
description: "Phase 3: Implement approved work using Ponytail minimal footprint discipline."
---

# Cook Skill (Phase 3: Implementation)

The Cook workflow executes the approved plan step-by-step with strict minimal code discipline.

## Hard Rules
- **Ponytail Mode**:
  - YAGNI: If code is not strictly required by the plan, do not write it.
  - Standard Library First: Prefer language built-in functions over new dependencies.
  - Minimal Footprint: Keep edits contiguous and concise.
  - Ponytail Comment: Mark deliberate simplifications with `// ponytail:` or `# ponytail:`.
- **Atomic Execution**: Implement one item at a time; do not perform massive multi-file refactors in a single leap.

## Protocol
1. **Pre-edit Impact Confirmation**:
   - Ensure the symbol being edited was verified during the `scout` phase.
2. **Implementation**:
   - Edit files with surgical precision using replace tools or targeted writes.
   - Preserve existing documentation and code styles.
3. **Continuous Local Validation**:
   - Run linter/syntax checks (`ruff check`, `oxlint`, `tsc`) immediately after editing.
4. **Handoff**:
    - Once all planned changes are in place, immediately hand off to the `verify` phase.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Need modes, mandatory review, or `--advice` checkpoints? Hand the approved plan to official `ak:cook`; this skill is the Ponytail fast-path.
