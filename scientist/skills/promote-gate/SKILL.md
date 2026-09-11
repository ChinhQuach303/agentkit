---
name: promote-gate
description: "Phase 5: Enforce 3-tier promotion safety gates (Data, Performance, Integrity) and record decisions in Engram."
---

# Promote Gate Skill (Phase 5: 3-Tier Promotion Gate & Engram Sync)

The Promote Gate workflow enforces strict, automated verification gates before promoting any candidate model to production, syncing artifacts and recording decisions into Engram.

## Hard Rules
- **ZERO BYPASS ON 3-TIER GATES**:
  1. **Tier 1 - Data Gate**: 0 leakage flags and 100% schema contract compliance verified.
  2. **Tier 2 - Performance Gate**: Candidate meets or exceeds Champion on key metrics with zero unacceptable slice regressions.
  3. **Tier 3 - Integrity Gate**: All SHA-256 hashes in `manifest.json` match bundle files and HMAC signature is valid.
- **ENGRAM PERSISTENCE**: Promotion decisions must be immediately committed to Engram memory (`type: decision`, topic `decision/ml-promotion-*`).

## Protocol
1. **Tier 1: Data Contract & Leakage Check**:
   - Confirm passed audit from Phase 1 (`data-audit`). Fail immediately on missing audit receipt.
2. **Tier 2: Multi-slice Performance Validation**:
   - Compare Candidate metrics against production baseline from Phase 3 (`model-eval`).
   - Validate regression limits across critical cohorts, segments, and evaluation slices specified in project config.
3. **Tier 3: Cryptographic Integrity Verification**:
   - Validate `manifest.json` checksums against local bundle files.
   - Verify HMAC signature sidecar matches expected verification key.
4. **Registry & Object Store Sync**:
   - Sync verified bundle to object store (MinIO/S3) or model registry atomically.
   - Evict stale serving cache in staging/production endpoints.
5. **Engram SSoT Recording**:
   - Record decision via `mem_save`:
     - `title`: "Promoted <model_id> to production"
     - `type`: "decision"
     - `topic_key`: "decision/ml-promotion-<model_id>"
     - `content`: What was promoted, why (metrics delta), where (storage path), learned (gotchas).
6. **Deliverable**:
    - Production Promotion Receipt containing gate checklist, storage URI, and Engram memory ID (or `HANDOFF.md` entry when Engram is unavailable).

## Availability & Handoff
- Verified on Gemini/Antigravity; elsewhere file presence ≠ active — confirm the running runtime reads this dir.
- Custom kit, no official counterpart. Never bypass the 3-tier gates; a promotion without a receipt is a failed run.
