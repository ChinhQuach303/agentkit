# Slice Catalog (disclosed reference for `model-eval`)

Slices that hide regressions behind healthy aggregates. Pick the ones matching the domain; every verdict is per-slice, never global-only.

- **Cohorts / tiers**: user segments, subscription tiers, regions. The classic Simpson host: global up, biggest cohort down.
- **Time horizons**: forecast lead times, recency buckets. Degrades at the tail while the head shines.
- **Volume tiers**: head vs long-tail entities. Long-tail collapse is invisible in weighted means — report unweighted too.
- **Categories / labels**: classes, product categories, intents. Per-class precision/recall, not just accuracy.
- **Edge regimes**: cold-start entities, missing-feature rows, out-of-vocabulary inputs. The 5% that decides trust.
- **Latency / cost buckets**: p50/p95/p99 inference time and cost per slice; a smarter model that blows the budget is a No-Go.

For each slice: metric, Champion value, Candidate value, delta, SLA bound, verdict. One regressed SLA-critical slice vetoes promotion regardless of the global number.
