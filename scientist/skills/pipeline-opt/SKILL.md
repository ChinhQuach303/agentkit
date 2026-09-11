---
name: pipeline-opt
description: "Phase 2: Optimize data pipelines, dbt incremental models, Dagster DAGs, and vectorized Polars operations."
---

# Pipeline Optimization Skill (Phase 2: Pipeline & DAG Optimization)

The Pipeline Optimization workflow profiles and streamlines transformation DAGs, maximizing throughput and minimizing memory footprint without unnecessary complexity.

## Hard Rules
- **PONYTAIL VECTORIZATION**: Never iterate over rows (`iterrows`, Python loops). Use native `polars` expressions (`select`, `with_columns`, `group_by`) or set-based SQL.
- **LAZY BY DEFAULT**: In Polars, prefer `pl.scan_parquet()` / `pl.scan_csv()` over immediate in-memory eager reads.
- **NO INTERMEDIATE BLOAT**: Materialize DataFrames only when feeding sinks or crossing process boundaries.

## Protocol
1. **DAG & Query Profiling**:
   - Inspect query execution plans with `EXPLAIN (ANALYZE, BUFFERS)` via `rtk psql`.
   - Identify sequential scans, hash-join spills, or redundant CTE re-evaluations.
2. **dbt & Incremental Efficiency**:
   - Ensure `is_incremental()` macros include correct partition filtering and idempotent `unique_key` merging.
   - Verify upstream dependency pruning (`--select +model_name+`).
3. **Dagster Partitioning & IO Management**:
   - Verify partitioned assets run with bounded chunk sizes.
   - Guard against unbounded concurrent tasks exhausting worker RAM.
4. **Memory Profiling & Streaming**:
   - Profile memory usage and prevent OOM spikes with lazy batching.
   - Mark intentional simplifications with `# ponytail: <reason>`.
5. **Deliverable**:
    - Pipeline Optimization Report showing before/after latency, RAM footprint, and throughput improvements.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Custom kit, no official counterpart. Requires a passing `data-audit` receipt before touching production pipelines.
