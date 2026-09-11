---
name: plan
description: "Phase 2: Create an evidence-backed atomic roadmap and specification before writing code."
---

# Plan Skill (Phase 2: Roadmap & Spec)

The Plan workflow transforms Scout findings and user requirements into an atomic, phased execution checklist.

## Hard Rule
- **HUMAN APPROVAL GATE**: Never start implementing until the user has reviewed and approved the plan.

## Protocol
1. **Spec-Kit Integration**:
   - For new features or specs, run `specify plan` to draft updates.
   - Ground every planned step in official documentation or project architecture rules.
2. **Atomic Checklist Structure**:
   - Break tasks into small, verifiable steps.
   - Cap checklists to a maximum of 5 items per phase (ADHD mode).
   - Identify explicit dependencies between tasks.
3. **Risk & Mitigation Gate**:
   - Highlight potential breaking changes, data migrations, or API contract updates.
   - Provide concrete time estimates per step.
4. **Deliverable**:
    - Write or update the implementation plan artifact.
    - Request user feedback before unlocking the `cook` phase.

## Plan Artifacts (file-first)
- Canonical path: `plans/<YYYYMMDD-HHMM>-<slug>/plan.md` (phase detail in `phase-NN-*.md` when >1 phase).
- Plan files win over chat history or task views when states disagree; reindex by re-reading the folder.
- Handoff contract every next stage must receive:
  `Goal / Approved scope + non-goals / Evidence & decisions / Artifacts produced / Acceptance criteria / Open risks / Authority granted`.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Need phased `plan.md`, red-team, or `--tdd` gates? Hand the checklist to official `ak:plan`; this skill is the Ponytail fast-path.
