---
name: scan
description: "Read-only security sweep for secrets, vulnerable deps, and dangerous patterns. Use when the user wants a pre-review security check, or asks to security-check a change or PR."
---

# Scan Skill (Read-Only Security Sweep)

Find, don't fix. This skill reports findings with file:line + severity; `review` judges them, `fix` repairs them. A clean report names the tools that ran — "secure" without tool evidence is not a verdict.

## Hard Rules
- **READ-ONLY**: Never edit code, never auto-fix, never commit. Findings only.
- **NO SILENT SKIPS**: Every check is pass, flagged, or explicitly "not checked (tool missing)". Absence of a tool is a gap, not a pass.
- **FIX OWNERSHIP ELSEWHERE**: Repairs belong to `fix`; risk calls belong to `review`.

## Redact
Findings may contain live secrets. **Redact secret values** (`<REDACTED>`, keep file:line + pattern kind); a finding with a real credential also aborts any pending `ship` until rotated.

## Protocol
1. **Secret sweep**:
   - Preferred: `gitleaks detect --source .` or `trufflehog git file://.` when installed.
   - Fallback: `git grep -nE "password|passwd|api[_-]?key|secret|token" -- ':!*.lock'` plus history check `git log -p --all -S "api_key" --oneline | head -20`.
   - Anti-pattern: **tracked-then-removed** ("deleted already"). Tell: secret in history. Fix: rotate, then purge (deleting the file is not enough).
   - **Completion criterion:** per-tool result recorded (findings or clean-with-tool-named).
2. **Dependency audit**:
   - Per lockfile present: `npm audit --omit=dev`, `pip audit`, `cargo audit`. No lockfile / no tool → "not checked", never "secure".
   - **Completion criterion:** each ecosystem reports checked-with-counts or explicitly not-checked.
3. **Dangerous patterns** (grep first, `semgrep` when configured):
   - Raw SQL/string interpolation into queries or shell (`shell=True`, `subprocess` with `shell=`, backtick execution).
   - `pickle.load` / `yaml.load` (no Loader) on untrusted input.
   - Hardcoded credentials, overly broad permissions (`chmod 777`, `0.0.0.0/0`, `*` IAM).
   - Crypto red flags: MD5/SHA1 for security, hardcoded IVs, disabled TLS verification.
   - **Completion criterion:** each pattern family reports findings or clean-with-method.
4. **Deliverable**:
   - Report: findings (`file:line`, severity, why it matters) + tool coverage table (checked / not-checked per family).
   - Hand to `review` with the report attached; BLOCK-worthy items flagged up front.
   - **Completion criterion:** `review` can triage from the report alone; coverage table has no silent gaps.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Runs before `review`. Official counterpart for deeper runs: `ak:security-scan`.
