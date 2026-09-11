---
name: data-audit
description: "Phase 1: Audit data contracts, schema constraints, target leakage, and temporal boundaries."
---

# Data Audit Skill (Phase 1: Data & Leakage Audit)

The Data Audit workflow verifies incoming datasets, enforces strict data contracts, and detects leakage vulnerabilities before model training or transformation begins.

## Hard Rules
- **ZERO TARGET / TEMPORAL LEAKAGE**: Fail immediately if features contain future information (look-ahead bias) or target proxies.
- **DATA CONTRACT INTEGRITY**: Enforce schema constraints (nullability, dtypes, range checks) strictly.

## Protocol
1. **Schema & Contract Verification**:
   - Inspect data schemas against formal contracts (e.g. `feature_contract.json`, dbt tests).
   - Check for unexpected nulls, missing partitions, or unexpected datatype coercions.
2. **Temporal Boundary & Partition Guard**:
   - In time series pipelines, assert `event_timestamp <= evaluation_cutoff`.
   - Verify train/test splits have an adequate purge window / embargo to prevent auto-correlation leakage.
3. **Data Drift & Distribution Audit**:
   - Compute distribution statistics across feature slices using `polars` / native vectorized operations.
   - Detect significant mean/variance shift or out-of-vocabulary categories.
4. **Context Optimization**:
   - Use `rtk psql` or `rtk read` to examine tabular outputs without flooding the LLM context.
5. **Deliverable**:
    - Data Integrity Audit Report with Go / No-Go verdict for downstream pipelines.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Custom kit, no official counterpart. Feed the Go/No-Go receipt into `pipeline-opt` or `model-eval`, never straight to training.
