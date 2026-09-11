---
name: experiment-run
description: "Phase 4: Track experiment runs, record hyperparameters, generate reproducible manifests, and sign bundles."
---

# Experiment Run Skill (Phase 4: Experiment Tracking & Manifest Generation)

The Experiment Run workflow manages reproducible experiment execution, hyperparameter optimization tracking, and cryptographic artifact bundle packaging.

## Hard Rules
- **ABSOLUTE REPRODUCIBILITY**: Every experiment must record commit SHA, dataset hash, random seeds, and full hyperparameter sets.
- **CRYPTOGRAPHIC BUNDLE INTEGRITY**: Every artifact bundle must produce a canonical `manifest.json` with SHA-256 hashes for all member files and an HMAC signature sidecar (`.sig`).

## Protocol
1. **Experiment Execution & Configuration**:
   - Record exact training arguments, dataset partition windows, and dependency versions.
   - Maintain clean parameter separation (e.g., Hydra/Pydantic config schemas).
2. **Artifact Serialization**:
   - Serialize model weights and preprocessors to standardized formats (ONNX, LightGBM binary, Safetensors).
   - Ensure serialization is deterministic and free of pickled arbitrary code vulnerabilities.
3. **Canonical Manifest Construction**:
   - Generate `manifest.json` with keys:
     - `model_id`, `version`, `git_commit`, `created_at`
     - `feature_contract_version`, `dataset_sha256`
     - `metrics_summary` (sliced WMAPE / accuracy)
     - `files`: list of objects `{path, size_bytes, sha256}`
4. **Bundle Cryptographic Signing**:
   - Compute HMAC-SHA256 signature over canonical `manifest.json` content.
   - Save signature into sidecar `manifest.json.sig`.
5. **Deliverable**:
   - Packaged Model Bundle with verified `manifest.json` and HMAC signature ready for promote-gate.
