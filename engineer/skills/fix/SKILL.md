---
name: fix
description: "Implement the smallest, cause-aligned repair based on a proven root cause with zero speculative changes."
---

# Fix Skill (Cause-Aligned Minimal Repair)

The Fix workflow takes a proven root cause and applies the smallest surgical correction necessary, adhering strictly to Ponytail discipline.

## Hard Rules
- **CAUSE-ALIGNED ONLY**: Only modify lines directly responsible for the proven bug. Never bundle unrelated refactoring, formatting, or feature changes.
- **PONYTAIL MINIMAL FOOTPRINT**: Reach for language built-in functions or standard library before writing new helper abstractions.
- **MANDATORY NOTATION**: Always document the fix reason with `// ponytail:` or `# ponytail:`.

## Protocol
1. **Verify Root Cause Prerequisites**:
   - Confirm that a reproduction case and proven root cause exist (from `debug` skill).
   - If root cause is unproven, drop back to `debug`.
2. **Surgical Implementation**:
   - Apply the targeted patch to the exact lines identified.
   - Maintain contiguous edits and preserve surrounding docstrings.
3. **Immediate Local Verification**:
   - Run the reproduction test case to confirm the bug is squashed.
   - Run the full test suite to guarantee zero regression.
4. **Deliverable**:
   - Verified minimal diff and test output ready for `verify` or `review`.
