---
name: frame
description: "Lock fuzzy requirements into a confirmed brief through relentless one-at-a-time questions. Use when the user says 'build X', when the outcome is unclear, or always before planning."
---

# Frame Skill (Requirement Locking)

Misalignment is the most common failure mode: nobody knows exactly what they want until forced to say it. This skill forces it — **before** `plan` spends anything.

## Hard Rules
- **ONE QUESTION AT A TIME**: Never batch questions. One gap, one question, one locked answer, then next.
- **NO SOLUTIONEERING**: Tech choices before the problem is locked are banned. Problem first, always.
- **NO BLANKET APPROVALS**: "Cứ làm đi" never covers a scope-changing decision. Split gaps, ask separately.

## Protocol
1. **Overlap scan**:
   - `ls plans/` and `git status --short` — unfinished briefs and dirty trees are blocking context until confirmed otherwise.
   - **Completion criterion:** no hidden prior art; or prior brief explicitly superseded.
2. **Branch coverage interview** (one question per turn, in this order):
   - Outcome: observable behavior when done (not tech, not effort).
   - Users: who benefits, who is affected.
   - Constraints: stack, modules, compatibility, tools that must be preserved.
   - Non-goals: tempting adjacent work explicitly excluded.
   - Acceptance: observable checks, including edge cases and expected errors.
   - Authority: whether external research, publication, deployment, or destructive actions are allowed.
   - Anti-pattern: **solutioneering** (user or agent names tools/frameworks before outcome locks). Tell: tech nouns appear in outcome answers. Fix: park them in a "parking lot" section, return to problem.
   - Anti-pattern: **question batching** (3 questions in one message). Tell: user answers 1 of 3. Fix: re-ask the unanswered ones singly.
   - **Completion criterion:** every branch has a locked answer; parking lot reviewed (adopted or explicitly dropped).
3. **Shared language capture**:
   - New domain terms coined during interview go straight into `CONTEXT.md` (Term / Means / Does-NOT-mean). Reuse them verbatim from here on.
   - **Completion criterion:** no term used in the brief is undefined in `CONTEXT.md`.
4. **Deliverable**:
   - `mkdir -p plans/<YYYYMMDD-HHMM>-<slug>/`, write `brief.md`: Goal / Users / Constraints / Non-goals / Acceptance / Authority / Parking lot disposition.
   - Read the brief back for user confirmation; unresolved items listed last, never silently assumed.
   - **Completion criterion:** user-confirmed `brief.md` exists; `plan` can execute with zero re-derivation.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Feeds `plan` directly. Official counterpart for deeper runs: `ak:brainstorm` (+ `ak:advise` for pressure-testing).
