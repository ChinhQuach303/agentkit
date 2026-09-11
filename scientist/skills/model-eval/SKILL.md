---
name: model-eval
description: "Phase 3: Evaluate model and LLM quality using sliced metrics, Champion vs Candidate scorecards, and LLM-as-a-judge."
---

# Model & LLM Evaluation Skill (Phase 3: Model & LLM Evaluation)

The Model & LLM Evaluation workflow conducts rigorous, multi-dimensional assessment of ML models and LLM outputs, preventing hidden regressions behind aggregate statistics.

## Hard Rules
- **SLICED METRICS MANDATORY**: Never rely solely on aggregate metrics. Measure performance broken down by key project slices (e.g., user cohorts, time horizons, segments, categories, volume tiers).
- **NO SILENT REGRESSIONS**: A Candidate model cannot proceed if any critical slice deteriorates beyond allowed project tolerance compared to the production Champion.
- **DETERMINISTIC JUDGING**: For LLM evaluation, enforce temperature=0, structured rubric criteria, and schema-validated JSON outputs.

## Protocol
1. **Slice-Based Metrics Calculation**:
   - Compute domain-appropriate metrics (e.g. WMAPE, MAE, RMSE, F1, AUC, perplexity, latency) across critical slices defined in the project evaluation spec.
   - Flag any slice where error rate exceeds predefined service-level agreements (SLAs).
2. **Candidate vs Champion Scorecard**:
   - Execute side-by-side comparative backtesting on the exact same holdout period.
   - Calculate delta improvements and verify statistical significance.
3. **LLM Quality & Guardrail Evaluation**:
   - For LLM tasks, use LLM-as-a-judge with explicit multi-point rubrics (faithfulness, schema validity, safety, tone).
   - Check strict JSON schema adherence and detect hallucinated entities.
4. **Residual & Failure Analysis**:
   - Isolate worst-performing 5% cases to identify systematic model blindspots.
5. **Deliverable**:
    - Multi-slice Evaluation Scorecard with explicit Champion vs Candidate delta and Go / No-Go verdict.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Custom kit, no official counterpart. A Go verdict here is the required input to `experiment-run` packaging.
