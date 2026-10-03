# Documentation Drift Checks

## Goal
Catch drift between kit manifests, README inventory/runtime claims, and local Markdown links without generating narrative documentation.

## Tasks
- [x] Add stdlib checks for manifest exports vs files, README counts/runtime paths, and local Markdown links → `python eval/docs_consistency.py` passes.
- [x] Add regression tests for valid sources, stale counts, manifest export drift, and broken local links → `python -m unittest discover -s eval -p 'test_*.py'` passes.
- [x] Fix the Gemini CLI/Antigravity install-path description and document the docs checker → README now matches installer targets.
- [x] Add consistency checks and evaluator tests to CI → `.github/workflows/smoke.yml` runs compile, docs validation, and unit tests.
- [x] Run complete validation → evaluator passes all tiers; docs checks, unit tests, runtime smoke, Python/JSON/Bash checks, and `git diff --check` pass.

## Decision
Manifests remain the source of truth for exported skill/agent inventories. README narrative remains human-maintained; consistency checks gate duplicated facts. No generated-doc pipeline added.
