---
name: data-audit
description: "Catch leaking features, broken schemas, and drifted distributions before training. Use when a new dataset or feature set arrives, or when the user asks whether the data is safe to train on."
---

# Data Audit Skill (Leakage, Contract & Drift)

No model outruns its data: a leaking feature beats every architecture choice silently. Audit first, train never on a No-Go.

## Hard Rules
- **ZERO TARGET / TEMPORAL LEAKAGE**: Fail immediately on future information (look-ahead bias) or target proxies. A leaky feature is deleted, never "handled downstream".
- **CONTRACT BEFORE STATISTICS**: Schema compliance first; distributions only on contract-clean data.

## Protocol
1. **Schema & contract verification**:
   - Load the formal contract (`.agents/contracts/data_contract.json`): primary keys, temporal column, per-column type/nullability/range.
   - Check in order: (a) missing/extra columns, (b) nulls in non-nullable, (c) dtype coercions (`pl.read_csv` guessing dates as strings), (d) range violations, (e) duplicate primary keys: `df.group_by(["entity_id","timestamp"]).len().filter(pl.col("len") > 1)`.
   - Anti-pattern: **silent `dropna`/fillna to pass the audit**. Tell: row counts change without a logged decision. Fix: quarantine + report, never mute.
   - **Completion criterion:** contract checklist all-green with row counts quoted, or explicit FAIL items listed.
2. **Temporal boundary & leakage hunt**:
   - Assert `event_timestamp <= evaluation_cutoff` per row: `df.filter(pl.col("timestamp") > cutoff).height == 0`.
   - Purge/embargo: train/test split must leave a gap ≥ autocorrelation window; overlapping windows = leakage.
   - Proxy hunt (ordered): (a) feature names containing target synonyms, (b) post-cutoff-derived columns (timestamps, IDs assigned after the event), (c) suspiciously perfect correlation (`|corr| > 0.95` with target on a holdout slice).
   - Anti-pattern: **target-shaped proxy** ("it's just a count"). Tell: ablation drops performance to baseline. Fix: drop the feature, re-audit.
   - **Completion criterion:** leakage hunt table (feature → verdict → evidence) complete; zero open suspects.
3. **Drift & distribution audit**:
   - Per critical slice: mean/variance shift vs reference (`df.group_by("slice").agg(pl.col("x").mean(), pl.col("x").std())`), out-of-vocabulary categories, missing-partition gaps.
   - Inspect via `rtk psql` / `rtk read` without dumping raw rows.
   - **Completion criterion:** drift table with magnitudes; shifts above SLA flagged, not averaged away.
4. **Deliverable**:
   - Data Integrity Audit Report: contract table, leakage table, drift table, **Go / No-Go** verdict. No-Go names the exact fix (drop feature X, re-cut split at date D).
   - Feed Go receipts into `pipeline-opt` or `model-eval` — never straight to training.
   - **Completion criterion:** verdict + receipt consumable with zero re-derivation.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Custom kit, no official counterpart. Feed the Go/No-Go receipt into `pipeline-opt` or `model-eval`, never straight to training.
