---
name: deploy
description: "Release a shipped change to a K8s/cloud target behind gates, with rollback ready. Use when the user asks to deploy, release to staging/prod, or roll out a new image."
---

# Deploy Skill (Gated K8s Release)

Deploy is a gate sequence, not a command. Every gate has a completion criterion; a failed gate stops the chain — never `--force` past red.

## Hard Rules
- **TARGET FIRST**: `kubectl config current-context` must name the intended cluster. Prod deploys on an assumed context are banned.
- **IMMUTABLE TAGS**: Never deploy `:latest` to prod. Tag by commit SHA (`git rev-parse --short HEAD`).
- **ROLLBACK BEFORE ROLLOUT**: The undo command is written and verified possible before anything is applied.
- **NO DIRTY DEPLOYS**: `git status --short` must be clean; the deployed commit is recorded.

## Redact
Deploy output carries kubeconfigs, cloud keys, and internal endpoints. **Redact secrets** (`<REDACTED>`), show resource names and rollout lines only. A credential in any log aborts the run — rotate it, then restart the gates.

## Protocol
1. **Target guard**:
   - Run `kubectl config current-context` and `git status --short`. Confirm the context matches the intended environment (staging vs prod) with the user when prod is involved.
   - Anti-pattern: **assumed context** ("it's probably staging"). Tell: nobody printed the context. Fix: print it, confirm it.
   - **Completion criterion:** context named + confirmed; tree clean; deployed commit SHA recorded.
2. **Image & manifests**:
   - Build and tag immutably (`:git-<sha>`); `kubectl diff -f <manifests>` reviewed before apply. No `:latest`, no unreviewed diff.
   - Anti-pattern: **floating tags** (`:latest`, `:stable`). Tell: tag resolves differently over time. Fix: re-tag immutably.
   - **Completion criterion:** reviewed diff + immutable tag, both recorded.
3. **Migrate & back up**:
   - Migration plan written (ordered steps, reversibility each); back up persistent state first (DB snapshot / volume snapshot command recorded).
   - Anti-pattern: **migrate-and-pray** (apply migration with no backout). Tell: no reverse step exists. Fix: write the reverse before proceeding.
   - **Completion criterion:** backup verified restorable (or explicitly accepted risk), reverse steps written.
4. **Rollout & verify**:
   - Apply, then `kubectl rollout status deployment/<name>` to completion; smoke-check the live URL/endpoints (status codes + one golden-path request).
   - **Completion criterion:** rollout reports success AND smoke checks pass — one without the other is not done.
5. **Rollback on red**:
   - Any gate or smoke failure → `kubectl rollout undo deployment/<name>`, re-run smoke, confirm recovery.
   - Record outcome (deployed version, verification evidence, rollback used?) into HANDOFF/memory via `ship` conventions.
   - **Completion criterion:** live state verified good, or rolled back and verified good — never left unknown.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Runs after `ship`. Official counterpart: `ak:deploy` (provider authority, URL verify, rollback guidance).
