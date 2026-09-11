---
name: experiment-run
description: "Package one training run into a signed, reproducible bundle. Use when training finishes and the user wants the run locked down with lineage, manifest, and signature."
---

# Experiment Run Skill (Lineage → Manifest → Signature)

A run that can't be reproduced didn't happen. Lineage first, then bytes, then signature — in that order, no skipping.

## Hard Rules
- **ABSOLUTE REPRODUCIBILITY**: Commit SHA (`git rev-parse HEAD`), dataset hash, random seeds, full hyperparameters, dependency versions. Missing one = incomplete run.
- **NO PICKLE LINEAGE GAPS**: Standard formats only (ONNX, LightGBM binary, Safetensors) — never untrusted pickles.
- **CANONICAL-THEN-SIGN**: Signature covers the exact canonical bytes that ship; sign last, verify after.

## Redact
Training args and manifests may carry storage credentials or internal paths. **Redact secrets** (`<REDACTED>`) in every shown config, manifest excerpt, and log line.

## Protocol
1. **Freeze lineage**:
   - Record: `git rev-parse HEAD`, dataset partition window + `sha256sum` of inputs, seeds, full hyperparams (Hydra/Pydantic schema dump), `pip freeze` dependency pin.
   - Anti-pattern: **"same code, rerun later"** (unpinned deps/seeds). Tell: rerun diverges. Fix: pin everything now.
   - **Completion criterion:** lineage block complete; a stranger could rebuild the env from it.
2. **Serialize artifacts**:
   - Weights + preprocessors to ONNX / LightGBM binary / Safetensors; deterministic settings on.
   - **Completion criterion:** every artifact file exists with byte size recorded.
3. **Canonical manifest**:
   - Build `manifest.json` (see `scientist/templates/manifest.template.json`): `model_id`, `version`, `git_commit`, `created_at`, `feature_contract_version`, `dataset_sha256`, `metrics_summary` (sliced, from `model-eval`), `files: [{path, size_bytes, sha256}]` where each hash comes from `sha256sum <file>`.
   - **Completion criterion:** manifest validates and every listed hash matches disk.
4. **Sign + verify**:
   - HMAC-SHA256 over canonical bytes → sidecar `manifest.json.sig`; then re-verify signature and re-hash all files (catches sign-then-modify).
   - **Completion criterion:** signature verifies; bundle ready for `promote-gate`.
5. **Deliverable**:
   - Bundle path + manifest + `.sig` + lineage block.
   - **Completion criterion:** `promote-gate` Integrity Gate passes on first try.

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Custom kit, no official counterpart. Bundle is promotion-ready only after `promote-gate` signs the receipt.
