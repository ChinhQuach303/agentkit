---
name: debug
description: "Prove the root cause of an error or failure with concrete execution evidence before touching code."
---

# Debug Skill (Root Cause Proof)

The Debug workflow isolates failures systematically, establishing an unbroken chain of evidence from error symptom to root cause without guessing or premature patching.

## Hard Rules
- **ZERO CODE EDITS**: Never edit implementation code while in debug mode.
- **EVIDENCE BEFORE HYPOTHESES**: Formulate hypotheses only after inspecting real logs, stack traces, and variable states.
- **DETERMINISTIC REPRODUCTION**: Isolate the smallest reproducible command or test case before investigating.

## Protocol
1. **Reproduce & Capture**:
   - Run the failing command, test, or API call.
   - Capture exact error output, exit codes, and relevant runtime logs.
2. **Trace Execution Flow**:
   - Use GitNexus (`impact`, `query`, or call stack inspection) to locate the origin of the failing symbol.
   - Examine state at each call boundary.
3. **Isolate Trigger Condition**:
   - Differentiate what makes the passing case pass and the failing case fail (delta debugging).
   - Verify boundary values (null, empty, negative, unicode, concurrent state).
4. **Deliverable**:
   - Root Cause Proof Report:
     - Exact line numbers and failing symbols.
     - Proven mechanism of failure with reproduction command.
      - Hand-off recommendation to `fix` skill.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Same contract as official `ak:debug` (prove cause before touching code); interchangeable.
