---
name: model-eval
description: "Score a Candidate against the production Champion per slice, catching Simpson's-paradox regressions. Use when a model or prompt change needs a Go/No-Go verdict, or the user asks how the candidate compares."
---

# Model Eval Skill (Sliced Champion vs Candidate)

Aggregates lie: a global win routinely hides a cohort collapse. Every verdict here is per-slice; one regressed SLA-critical slice vetoes promotion.

## Hard Rules
- **SLICED METRICS MANDATORY**: Never certify on a global number alone. Slices from `slice-catalog.md` matched to the domain.
- **NO SILENT REGRESSIONS**: Any SLA-critical slice worse than Champion beyond tolerance = No-Go, regardless of globals.
- **DETERMINISTIC JUDGING**: LLM-as-judge at temperature=0, multi-point rubric (faithfulness, schema validity, safety, tone), schema-validated JSON outputs.

## Protocol
1. **Slice-based metrics**:
   - Same holdout period for both models, side by side. Metrics per domain: WMAPE/MAE/RMSE (forecast), F1/AUC (classification), perplexity/latency (LLM).
   - Per slice record: metric, Champion, Candidate, delta, SLA bound, verdict. Compute with vectorized ops (`df.group_by("slice").agg(...)`), not loops.
   - Anti-pattern: **weighted-mean blindness** (long-tail collapse hidden in the average). Tell: unweighted slice table disagrees with the global. Fix: report both, judge by slices.
   - **Completion criterion:** full slice table, no empty cells, every SLA breach flagged.
2. **Champion vs Candidate scorecard**:
   - Deltas + significance check on the same holdout; name the window (`holdout=2026-08-01..2026-08-31`).
   - Verify both runs actually used that window (`grep -h holdout runs/*.json`); compare artifacts with `diff champion.json candidate.json` on shared keys.
   - Anti-pattern: **shifting holdouts** (different periods per model). Tell: windows differ in the fine print. Fix: re-run on one frozen window.
   - **Completion criterion:** scorecard with deltas, window, and significance noted.
3. **LLM quality & guardrails** (LLM tasks only):
   - Judge rubric scored 1–5 per axis; validate output JSON against schema before scoring (`python -m jsonschema -i out.json schema.json` or equivalent).
   - Hallucination check: entities in output must trace to retrieved context; untraceable = fail.
   - **Completion criterion:** rubric table + schema pass/fail + hallucination verdict.
4. **Residual & failure analysis**:
   - Isolate the worst 5%: cluster by slice to find systematic blindspots (cold-start, OOV, missing-feature regimes).
   - **Completion criterion:** blindspot list with slice attribution, or explicit "no pattern found".
5. **Deliverable**:
   - Scorecard + **Go / No-Go** verdict with the vetoing slice named (or "no vetoes"). Go feeds `experiment-run` packaging.
   - **Completion criterion:** verdict reproducible from the tables alone.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Custom kit, no official counterpart. A Go verdict here is the required input to `experiment-run` packaging.
