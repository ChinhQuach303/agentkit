---
name: ship
description: "Phase 6: Commit changes cleanly, prepare pull requests, and persist episodic memory to Engram."
---

# Ship Skill (Phase 6: Ship & Memory Persistence)

The Ship workflow finalizes delivery, ensures clean version control, and updates persistent project memory.

## Hard Rules
- **CLEAN REPO ONLY**: Never commit if there are untracked secrets, stray artifacts, or broken builds.
- **ENGRAM PERSISTENCE (optional)**: Call `mem_session_summary` before ending the session when Engram is available; otherwise write `HANDOFF.md` (Goal/Decisions/Evidence/Blockers) so any session can resume.

## Protocol
1. **Git Status Audit**:
   - Run `rtk git status` to review modified and staged files.
2. **Conventional Commit**:
   - Write semantic, clear commit messages (`feat(...)`, `fix(...)`, `refactor(...)`).
3. **Engram Memory Sync**:
   - If architectural decisions were made, save them with `mem_save(type='decision', topic_key='decision/<name>')`.
   - If bugs were solved, save lessons with `mem_save(type='learning', topic_key='lesson/<name>')`.
   - Call `mem_session_summary`:
     - Goal
     - Discoveries
     - Accomplished
     - Next Steps (clearing in-flight task state)
4. **Deliverable**:
    - Provide commit hash and PR branch status to user.

## HANDOFF.md (when the chain continues in another session)
- Location: project root or `.agents/HANDOFF.md` (one file, overwritten per session; Engram `mem_session_summary` when available is the durable copy).
- Sections: Goal / Decisions (with why) / Evidence (files, commits, test output) / Blockers & open risks / Next step + authority granted.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Prefer official `ak:git` guarded workflows + `ak:ship` release gates when available; this skill bundles commit + memory for the fast path.
