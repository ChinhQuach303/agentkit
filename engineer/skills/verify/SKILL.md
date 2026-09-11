---
name: verify
description: "Prove a change works with tests at confirmed seams plus a blast-radius check. Use when implementation is done and the user wants proof before review, or asks to run the tests and check what else is affected."
---

# Verify Skill (Seams + Blast Radius)

Proof, not assertion: code is broken until a run says otherwise. Tests verify behavior through public interfaces; the blast-radius check proves nothing else moved.

## Hard Rules
- **EVIDENCE BEFORE ASSERTIONS**: Never claim code works without showing run output.
- **SEAMS FIRST**: No test at an unconfirmed seam (see `seam-guide.md`).
- **GRAPH INTEGRITY CHECK**: Run `gitnexus detect-changes --scope all --repo .` before commit when available; otherwise `git status --short && git diff --stat` (degraded mode OK).

## Redact
Test output and diffs may leak secrets or customer data. **Redact first** (`<REDACTED>`), quote only failing lines plus the summary count. A credential in output is itself a finding — report it, don't propagate it.

## Protocol
1. **Confirm seams**:
   - Write down the seams under test from `seam-guide.md` (HTTP route, CLI argv/stdout, public function, pipeline stage boundary, LLM JSON schema) and confirm with the user.
   - Anti-pattern screen — reject and reshape tests that are:
     - **Implementation-coupled** (mocks internals, privates, side-channel DB reads). Tell: breaks on behavior-preserving refactors.
     - **Tautological** (`expect(add(a,b)).toBe(a+b)`, hand-derived snapshots). Tell: passes by construction, can never disagree. Fix: expected values from an independent source (known-good literal, worked example, spec).
     - **Horizontal slicing** (all tests first, then all code). Tell: tests verify imagined shapes, go insensitive to real changes. Fix: vertical slices — one test → one check → repeat (already-implemented code just needs the test side).
   - **Completion criterion:** confirmed seam list written; every planned test maps to one.
2. **Run the suites**:
   - Targeted first: `pytest -q <path> -k "<seam>"`, then the full suite: `pytest -q`. Compress floods with `rtk` when available.
   - Record: command + pass/fail counts + the failing lines (redacted). No summary without numbers.
   - **Completion criterion:** per-seam results recorded with counts; zero unaccounted failures.
3. **Blast-radius validation**:
   - Run GitNexus `detect_changes` (MCP) when available; fallback `gitnexus detect-changes --scope all --repo .` or `git status/diff`.
   - Changes must touch ONLY expected symbols/flows. Unexpected impacted symbols → halt, investigate regression risk, do not explain away.
   - **Completion criterion:** impacted set ⊆ expected set, evidenced by tool output.
4. **Handoff**:
   - Failures → `debug` (reproduce → isolate → fix → re-verify). Loop rules: red first (repro command before any touch), one slice at a time, refactoring belongs to `review`, not here.
   - All green + blast radius clean → `review` with the seam list and counts attached.
   - **Completion criterion:** `review` receives commands, counts, seam list, and blast-radius evidence — zero re-derivation needed.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Prefer official `ak:test` for independent validation; this skill folds test + blast-radius into one pass.
