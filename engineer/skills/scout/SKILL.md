---
name: scout
description: "Map the symbols, flows, and blast radius behind a change question without touching code. Use when the user asks what touches X, where a feature lives, or whether changing Y is safe."
---

# Scout Skill (Explore & Map)

Answer "what/where/how-risky" with call-graph evidence, never edits. Text search alone is a guess: ground every claim in a trace.

## Hard Rules
- **ZERO CODE MODIFICATIONS**: Never create, edit, or delete source files during this phase.
- **TRACE OR IT DIDN'T HAPPEN**: Every usage claim cites a caller chain; uncalled ≠ dead (check dynamic dispatch, public API, runtime wiring).

## Protocol
1. **Locate symbols & execution flows** (in order):
   - Read `CONTEXT.md` first when present: reuse its terms verbatim for files, symbols, and findings.
   - GitNexus MCP `query` when available: `query("<concept>")` for flows, `context("<symbol>")` for the 360° view.
   - Fallback: `gitnexus query "<concept>"` CLI, then grep/AST search — label fallback findings as lower-confidence.
   - Legacy local runner only: `node .gitnexus/run.cjs query "<concept>"`.
   - **Completion criterion:** every named symbol has file:line + at least one caller chain or an explicit "no callers found (checked dispatch/API)".
2. **Impact & blast radius analysis**:
   - For each candidate symbol, run `impact` upstream; record direct callers (WILL BREAK), indirect (LIKELY), transitive (TEST), plus affected processes/flows.
   - Risk is LOW/MEDIUM/HIGH/CRITICAL with the reason named (fan-out count, critical-path membership). HIGH/CRITICAL flags go first in the report, not buried.
   - **Completion criterion:** blast radius table complete; no "probably safe" without a trace behind it.
3. **Context optimization**:
   - Use `rtk read <path>` / `rtk ls` for compressed inspection; quote file:line ranges instead of pasting files.
   - **Completion criterion:** findings fit one screen; full dumps stay out.
4. **Deliverable**:
   - Findings summary: target files & line ranges, upstream callers & flows, blast-radius table with risk levels, handoff to `plan`.
   - **Completion criterion:** `plan` can scope checklists from this alone — zero re-derivation.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Need deeper evidence? Hand the findings to official `ak:scout` / `ak:research`; this skill is the Ponytail fast-path.
