---
name: review
description: "Review the diff since a fixed point along two axes: Standards (repo conventions plus a smell baseline) and Spec (what the originating issue asked for). Use when the user wants a branch, PR, or work-in-progress reviewed, or asks to review since X."
---

# Review Skill (Two-Axis Review)

A change can pass one axis and fail the other: standard-clean but wrong thing, or exactly-asked but convention-breaking. Report both separately so neither masks the other. Never merge or rerank across axes.

## Hard Rules
- **READ-ONLY**: Never edit code under review. Findings only; `fix` owns repairs.
- **SPEC ANCHORS STANDARDS**: A documented repo standard always overrides the smell baseline.
- **NO PERFORMATIVE AGREEMENT**: Evaluate on evidence and technical rigor alone.

## Redact
Review output quotes diffs and specs. **Redact every secret first** (`<REDACTED>`), quote only hunks carrying findings. Diffs with credentials: report the leak as a finding, don't propagate it.

## Protocol
1. **Pin the fixed point**:
   - Whatever the user named (SHA, branch, tag, `main`, `HEAD~5`); unsaid → ask, don't guess.
   - Capture once: `git diff <fixed-point>...HEAD` (three-dot, merge-base) plus `git log <fixed-point>..HEAD --oneline`.
   - Confirm `git rev-parse <fixed-point>` resolves and the diff is non-empty. Bad ref or empty diff fails here, not later.
   - **Completion criterion:** valid fixed point, non-empty diff command recorded.
2. **Identify the spec source** (in order):
   - Issue refs in commits (`#123`, `Closes #45`), fetched via tracker.
   - A path the user passed.
   - A spec under `docs/`, `specs/`, or `plans/` matching branch/feature.
   - Nothing found → ask where; "no spec" means the Spec axis reports "no spec available", not silence.
   - **Completion criterion:** spec located, or explicit no-spec recorded.
3. **Identify the standards sources**:
   - Repo docs (`CODING_STANDARDS.md`, `CONTRIBUTING.md`, project glossary in `CONTEXT.md`, Engram `mem_search "decision"` ADRs), plus the `smells.md` baseline in full.
   - **Completion criterion:** source list written; repo-overrides noted.
4. **Run both axes in parallel** (separate contexts so neither pollutes the other; subagents when available, else sequential passes):
   - Standards brief: "Per file/hunk: (a) documented-standard breaches with file+rule cites; (b) baseline smells by name with quoted hunk. Documented breaches may be hard; smells are always judgement calls. Skip tooling-enforced items. Under 400 words."
   - Spec brief: "(a) spec requirements missing/partial; (b) unasked behaviour (scope creep); (c) implemented-but-wrong. Quote the spec line per finding. Under 400 words."
   - Taint pass (fold into Standards): trace untrusted inputs to sinks with GitNexus `explain` when available (`gitnexus explain --target <file>`), else manual input→sink trace; raw interpolation into shell/SQL is a hard finding.
   - **Completion criterion:** two bounded reports exist, each quotable to diff/spec lines.
5. **Verdict**:
    - Present `## Standards` and `## Spec` verbatim or lightly cleaned — do not merge findings.
    - End with per-axis totals and the worst issue *within each axis*.
    - Emit: **PASS** (ready to ship), **CAUTION** (non-blocking noted), **BLOCK** (must fix before ship).
- **Second-opinion checkpoint (advisory-only)**: on BLOCK or high-stakes calls, restate task + evidence + exact question for one fresh read (own session or peer agent). Counsel never approves, edits, or replaces this verdict.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Stronger chain when available: read-only `ak:security-scan` first, then `ak:code-review`; this skill is the single-pass alternative.
