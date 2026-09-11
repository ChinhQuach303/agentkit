---
name: ship
description: "Commit a reviewed change cleanly and preserve session memory for the next session. Use when review passes and the user wants to commit, open a PR, or close out the session."
---

# Ship Skill (Ship & Memory Persistence)

Delivery is a gate, not a reflex: clean tree, honest message, memory saved. Never commit to skip a gate.

## Hard Rules
- **CLEAN REPO ONLY**: No commit with untracked secrets, stray artifacts, or red builds. `git status --short` must be explainable line by line.
- **NO COMMIT WITHOUT APPROVAL**: The user approves the diff first; `--auto` never implies push/PR/merge authority.
- **MEMORY BEFORE EXIT**: A session that learned nothing on record wasted the learning.

## Redact
Commit messages, PR bodies, and memory entries are public-by-default surfaces. **Redact secrets** (`<REDACTED>`); never commit `.env`, keys, or customer data. A secret in `git status` aborts the ship — clean it first.

## Protocol
1. **Git status audit**:
   - Run `git status --short && git diff --stat`; every line accounted for (in-scope, or reverted/stashed).
   - Blast-radius re-check when available: `gitnexus detect-changes --scope all --repo .` — unexpected symbols → back to `debug`.
   - **Completion criterion:** tree fully explained; nothing unintended ships.
2. **Conventional commit**:
   - Message shape: `feat|fix|refactor(<scope>): <what + why>`; body cites the review verdict and the hypothesis that held (for fixes).
   - Push/PR/merge only on explicit approval; record the branch state otherwise.
   - Anti-pattern: **checkpoint commits** ("wip", "fix again"). Tell: message explains nothing. Fix: squash to one honest commit per change.
   - **Completion criterion:** `git log -1 --stat` reads as the whole story.
3. **Engram memory sync** (or HANDOFF.md when Engram is missing):
   - Decisions → `mem_save(type='decision', topic_key='decision/<name>')`; lessons → `mem_save(type='learning', topic_key='lesson/<name>')`.
   - Fallback file `.agents/HANDOFF.md`: Goal / Decisions+why / Evidence (files, commits, test counts) / Blockers / Next step + authority.
   - Close with `mem_session_summary` when available.
   - **Completion criterion:** a fresh session resumes from memory/HANDOFF alone.
4. **Deliverable**:
   - Commit hash + PR/branch status to the user.
   - **Completion criterion:** hash exists, message honest, memory written.

## HANDOFF.md (when the chain continues in another session)
- Location: project root or `.agents/HANDOFF.md` (one file, overwritten per session; Engram `mem_session_summary` when available is the durable copy).
- Sections: Goal / Decisions (with why) / Evidence (files, commits, test counts) / Blockers / Next step + authority.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Prefer official `ak:git` guarded workflows + `ak:ship` release gates when available; this skill bundles commit + memory for the fast path.
