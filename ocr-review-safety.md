# Optional OCR Review Safety

## Goal
Keep OCR supplemental, explicitly consented, cost-bounded, secret-aware, and non-blocking without allowing its output to own the review verdict.

## Tasks
- [x] Update review instructions for external-data consent, positive token budget, secret-bearing diffs, config writes, stdout output, and missing/failing fallback → Verify: OCR is skipped by default absent consent and never blocks manual review. **Done:** OCR is opt-in per review, output streams to stdout, and secrets/config changes are prohibited without separate approval.
- [x] Add evaluator doctrine checks and focused unit tests → Verify: tests reject blind trust, implicit consent/configuration, unbounded use, and blocking failure language. **Done:** Tier 1 enforces the core consent/budget/privacy/fallback doctrine; unit tests exercise missing consent and fallback rules.
- [x] Clarify installer/README OCR status as availability-only, not a review invocation → Verify: installation and doctor never trigger OCR analysis or configuration. **Done:** installer only calls `ocr --version`; README discloses external processing and cost.
- [x] Run evaluator, OCR doctrine tests, docs consistency, runtime smoke, Python/shell validation, and diff review → Verify: no model/provider call is made by validation. **Done:** evaluator passes all tiers; 9 unit tests, docs check, runtime smoke, Python/JSON/Bash checks, and `git diff --check` pass. Claude runtime remains UNVERIFIED as previously documented.
