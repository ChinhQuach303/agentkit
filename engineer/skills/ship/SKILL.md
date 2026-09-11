---
name: ship
description: "Phase 6: Commit changes cleanly, prepare pull requests, and persist episodic memory to Engram."
---

# Ship Skill (Phase 6: Ship & Memory Persistence)

The Ship workflow finalizes delivery, ensures clean version control, and updates persistent project memory.

## Hard Rules
- **CLEAN REPO ONLY**: Never commit if there are untracked secrets, stray artifacts, or broken builds.
- **ENGRAM PERSISTENCE MANDATORY**: Bắt buộc gọi `mem_session_summary` trước khi kết thúc session.

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
