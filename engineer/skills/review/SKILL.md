---
name: review
description: "Phase 5: Multi-axis review for correctness, security taint flows, and over-engineering audit."
---

# Review Skill (Phase 5: Multi-Perspective Review)

The Review workflow subjects implemented changes to an adversarial audit across correctness, security, and simplicity.

## Hard Rules
- **OVER-ENGINEERING AUDIT (Ponytail Review)**:
  - Scrutinize all new abstractions, wrappers, and helper functions.
  - Cut out any speculative generality or dead code.
- **SECURITY & TAINT CHECK**:
  - Run GitNexus `explain` (taint analysis) on data flows touching untrusted inputs or critical state when available; otherwise do manual input→sink trace and note degraded mode.

## Protocol
1. **Correctness Review**:
   - Verify boundary conditions, null checks, exception handling, and resource cleanup.
2. **Architecture & Drift Check**:
   - Ensure changes align with established ADRs recorded in Engram (`mem_search "decision"`).
3. **Simplicity Audit**:
   - Check if standard library can replace any newly introduced custom logic.
4. **Verdict**:
    - Emit review verdict:
      - **PASS**: Ready to ship.
      - **CAUTION**: Non-blocking improvements noted.
      - **BLOCK**: Must fix before ship.
- **Second-opinion checkpoint (advisory-only)**: on BLOCK or high-stakes calls, restate task + evidence + exact question for one fresh read (own session or peer agent). Counsel never approves, edits, or replaces this verdict.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Stronger chain when available: read-only `ak:security-scan` first, then `ak:code-review`; this skill is the single-pass alternative.
