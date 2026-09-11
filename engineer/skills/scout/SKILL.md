---
name: scout
description: "Phase 1: Explore and map codebase structure, symbols, and blast radius without modifying code."
---

# Scout Skill (Phase 1: Explore & Map)

The Scout workflow investigates the codebase, traces execution flows, and establishes blast radius bounds before any plan or implementation begins.

## Hard Rule
- **ZERO CODE MODIFICATIONS**: Never create, edit, or delete source files during this phase.

## Protocol
1. **Locate Symbols & Execution Flows**:
   - Use `gitnexus` to locate functions, classes, and execution traces.
   - Run `node .gitnexus/run.cjs query "<concept>"` or MCP `query`.
2. **Impact & Blast Radius Analysis**:
   - For every symbol identified for modification, run `impact` analysis upstream.
   - Determine callers, affected execution flows, and risk level (LOW, MEDIUM, HIGH, CRITICAL).
   - If risk is HIGH or CRITICAL, flag immediately in the findings.
3. **Context Optimization**:
   - Use `rtk read` or `rtk ls` to inspect files with compressed token overhead.
4. **Deliverable**:
   - A concise findings summary containing:
     - Target files & line ranges
     - Upstream callers & execution flows
     - Blast radius assessment
     - Handoff to `plan` phase
