---
name: plan
description: "Turn an accepted direction plus scout evidence into an atomic checklist with risks and a durable artifact. Use when the user wants a roadmap before implementation, or says plan this without coding yet."
---

# Plan Skill (Roadmap & Spec)

Plans are decisions with owners, not wishes. No implementation starts here — the output is an artifact another session or skill can execute verbatim.

## Hard Rules
- **HUMAN APPROVAL GATE**: Never start implementing until the user has reviewed and approved the plan.
- **EVIDENCE-GROUNDED**: Every step cites scout findings, docs, or code; no step floats on assumption.

## Protocol
1. **Alignment checkpoint** (skip if `frame` already locked a `brief.md` — consume it, don't re-ask):
   - Restate: outcome, constraints, non-goals, acceptance criteria. Ask ONLY about material-missing decisions (ones that change scope or risk); never blanket-approve shopping.
   - Scan for overlap first: `ls plans/` and `git status --short` — unfinished plan files and dirty trees are blocking relationships until confirmed otherwise.
   - Kill ambiguity with one question per gap, then lock the answers into the artifact.
   - **Completion criterion:** outcome + non-goals + acceptance criteria written and user-confirmed.
2. **Atomic checklist structure**:
   - ≤5 items per phase (ADHD mode); each item: what, files, done-means (observable check), depends-on.
   - Dependencies explicit (`blockedBy`); independent workstreams flagged for parallel.
   - **Completion criterion:** each item independently verifiable; no "and stuff" items.
3. **Risk & mitigation gate**:
   - Breaking changes, migrations, contract updates, rollback path per risky item; time estimate per step.
   - Anti-pattern: **speculative scope** (phases the outcome doesn't need). Tell: no acceptance criterion traces to it. Fix: cut or park as non-goal.
   - **Completion criterion:** every HIGH risk has a mitigation or an explicit accept.
4. **Deliverable**:
   - Create the folder first (`mkdir -p plans/<YYYYMMDD-HHMM>-<slug>/`), then write `plan.md` (contract, phases, risks) + `phase-NN-*.md` per phase; files win over chat on disagreement.
   - Request user feedback before unlocking `cook`; unresolved questions listed last.
   - Spec-Kit integration when available: `specify plan` drafts, plan files stay authoritative.
   - **Completion criterion:** artifact path reported; `cook` can execute with zero re-derivation.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Need phased red-team, `--tdd` gates, or GitHub projections? Hand the checklist to official `ak:plan`; this skill is the Ponytail fast-path.
