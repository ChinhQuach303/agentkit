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
- **OCR IS EVIDENCE, NOT VERDICT**: `ocr` output feeds the Standards axis only. Verdict stays with the two axes; missing `ocr` is a gap, never a block on running the review.
- **OCR NEEDS CONSENT**: `ocr` sends diffs/files to a configured LLM and may incur cost. Run only with explicit per-review approval for that provider and a positive token budget; never send secrets or sensitive data.
- **STAGE CHECKPOINT**: After each numbered protocol stage, report its result and evidence; wait for explicit approval before the next stage or skill handoff. Starting this skill approves only stage 1.

## Redact
Review output quotes diffs, specs, and `ocr` JSON. **Redact every secret first** (`<REDACTED>`), quote only hunks carrying findings. Diffs with credentials: report the leak as a finding, don't propagate it. Redact `ocr.json` the same way before quoting.

## Protocol
1. **Pin the fixed point**:
   - Whatever the user named (SHA, branch, tag, `main`, `HEAD~5`); unsaid → ask, don't guess.
   - Capture once: `git diff <fixed-point>...HEAD` (three-dot, merge-base) plus `git log <fixed-point>..HEAD --oneline`.
   - Confirm `git rev-parse <fixed-point>` resolves and the diff is non-empty. Bad ref or empty diff fails here, not later.
   - **Completion criterion:** valid fixed point, non-empty diff command recorded.
2. **OCR pre-pass, Standards-only (opt-in, degraded OK)**:
    - Before any OCR request, confirm the user approves sending this review's diff/files to the configured provider and approves a positive token budget. A review request alone is not OCR consent.
    - Skip OCR if consent is absent, configuration is missing, or the input contains secrets/customer data that cannot be removed safely. Record the reason and continue with manual + GitNexus checks.
    - With consent and safe input, use `ocr review --from <fixed-point> --to HEAD --format json --audience agent --output - --max-tokens-budget <approved-positive-limit>`; for no usable diff/history, use `ocr scan --path <touched-paths> --format json --audience agent --output - --max-tokens-budget <approved-positive-limit>`.
    - Never run `ocr config` or change provider/model settings automatically. Ask separately before any persistent configuration change. A resumed session also needs explicit consent and a positive budget.
    - OCR missing, denied, or failing is never a review failure. Record `not checked (<reason>)` and continue; never retry or resume silently.
    - Anti-pattern: **Blind-trust OCR**. Tell: copying its verdict as the skill verdict. Fix: redact output, tie each kept finding to a diff line and repo rule, and discard tooling-enforced noise.
    - **Completion criterion:** each OCR finding used has a redacted file:line and rule cite, or the report records `not checked (<reason>)`.
3. **Identify the spec source** (in order):
   - Issue refs in commits (`#123`, `Closes #45`), fetched via tracker.
   - A path the user passed.
   - A spec under `docs/`, `specs/`, or `plans/` matching branch/feature.
   - Nothing found → ask where; "no spec" means the Spec axis reports "no spec available", not silence.
   - **Completion criterion:** spec located, or explicit no-spec recorded.
4. **Identify the standards sources**:
    - OCR report from step 2 (only when consented and available) + repo docs (`CODING_STANDARDS.md`, `CONTRIBUTING.md`, project glossary in `CONTEXT.md`, Engram `mem_search "decision"` ADRs), plus the `smells.md` baseline in full.
    - **Completion criterion:** source list written; repo-overrides noted; OCR coverage or skip reason noted.
5. **Run both axes in parallel** (separate contexts so neither pollutes the other; subagents when available, else sequential passes):
    - Standards brief: "If consented OCR output exists, triage it per file/hunk: (a) documented-standard breaches with file+rule cites; (b) baseline smells by name with quoted hunk. Documented breaches may be hard; smells are always judgement calls. Skip tooling-enforced items. Under 400 words."
    - Spec brief: "(a) spec requirements missing/partial; (b) unasked behaviour (scope creep); (c) implemented-but-wrong. Quote the spec line per finding. Under 400 words."
    - Taint pass (fold into Standards): trace untrusted inputs to sinks with `ocr` findings + GitNexus `explain` when available (`gitnexus explain --target <file>`), else manual input→sink trace with `git grep -nE "shell=True|pickle\.load|yaml\.load" -- ':!*.lock'`; raw interpolation into shell/SQL is a hard finding.
   - Consume a `scan` report first when one exists (triage its BLOCK-worthy items before the axes); without one, note security coverage as a gap rather than assuming clean.
   - UI in the diff? Require the screenshots from `cook`; check them against the spec (layout, states, error paths) instead of re-reading JSX.
   - **Completion criterion:** two bounded reports exist, each quotable to diff/spec lines.
6. **Verdict**:
    - Present `## Standards` and `## Spec` verbatim or lightly cleaned — do not merge findings.
    - End with per-axis totals and the worst issue *within each axis*.
    - Emit: **PASS** (ready to ship), **CAUTION** (non-blocking noted), **BLOCK** (must fix before ship).
- **Second-opinion checkpoint (advisory-only)**: on BLOCK or high-stakes calls, restate task + evidence + exact question for one fresh read (own session or peer agent). Counsel never approves, edits, or replaces this verdict.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Stronger chain when available: read-only `ak:security-scan` first, then `ak:code-review`; this skill is the single-pass alternative.
