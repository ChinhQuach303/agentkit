---
name: pipeline-opt
description: "Profile then vectorize a slow or memory-hungry pipeline step. Use when a DAG stage is slow, OOMs, or the user asks to speed up or slim down a transformation."
---

# Pipeline Opt Skill (Profile, Then Vectorize)

Optimize the measured bottleneck, not the guessed one. Every change carries before/after numbers or it didn't happen.

## Hard Rules
- **PROFILE FIRST**: No rewrite without a baseline (plan output, timing, peak RAM). Guessed hotspots stay untouched.
- **VECTORIZE, DON'T LOOP**: No row iteration (`iterrows`, Python loops) — native `polars` (`select`, `with_columns`, `group_by`) or set-based SQL.
- **LAZY BY DEFAULT**: `pl.scan_parquet()` / `pl.scan_csv()` over eager reads; materialize only at sinks and process boundaries.
- **REQUIRES A PASSING `data-audit` RECEIPT** before touching production pipelines.

## Redact
Query plans and profiles may embed table names, credentials, or customer identifiers. **Redact secrets** (`<REDACTED>`), show plan shapes and timings, not raw connection strings or row samples.

## Protocol
1. **DAG & query profiling**:
   - Get the plan: `EXPLAIN (ANALYZE, BUFFERS)` via `rtk psql`; find sequential scans, hash-join spills, redundant CTE re-evaluations.
   - Time the stage end-to-end and record peak RAM as the baseline pair.
   - Anti-pattern: **premature vectorization** (rewriting unmeasured code). Tell: no baseline numbers exist. Fix: measure first.
   - **Completion criterion:** baseline (plan + latency + peak RAM) recorded; bottleneck named.
2. **dbt incremental efficiency**:
   - `is_incremental()` macros carry partition filters; merges keyed on idempotent `unique_key`; verify pruning with `dbt build --select +model_name+`.
   - **Completion criterion:** incremental run touches only fresh partitions, verified by run output.
3. **Partitioning & IO bounds**:
   - Partitioned assets run bounded chunk sizes; concurrent tasks capped so worker RAM can't exhaust.
   - Anti-pattern: **unbounded fan-out** ("more workers = faster"). Tell: RAM climbs with parallelism. Fix: cap concurrency, stream in chunks.
   - **Completion criterion:** chunk/concurrency bounds written in config, not tribal knowledge.
4. **Deliverable**:
   - Optimization report: before/after latency, RAM footprint, throughput — with the commands that produced each number.
   - Mark intentional simplifications `# ponytail: <reason>`.
   - **Completion criterion:** every claimed gain traces to a recorded run.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Custom kit, no official counterpart. Requires a passing `data-audit` receipt before touching production pipelines.
