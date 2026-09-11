# Changelog

## Unreleased (toward v2.1.1)
- Docs: honest custom-local positioning, official skill bridge tables, runtime support matrix, per-skill availability notes.
- `install.sh`: `install|uninstall|doctor` actions, `--dry-run` preview, `--skills/--exclude-skills`, timestamped backup of foreign content (`~/.agentkit-backups/`), Codex target fixed to `~/.agents/skills`, `AGENTKIT_SKIP_VERIFY=1`.
- Hooks doctrine: advisory + fail-open; `PreCommit`/`SessionEnd`/`PrePromotion` moved to skill-protocol checklists.
- Skills: durable `plans/<ts>-<slug>/plan.md` artifacts, `HANDOFF.md` convention, second-opinion checkpoint in review.
- `ak-eval`: skill-creator identifier checks, placeholder guard, official-name overlap NOTEs, hook-doctrine honesty gate, install lifecycle e2e, `.agents/skills` coexistence probe.

## v2.1.0 — Public usable
Focus: blockers fixed, multi-runtime, optional deps, honest strict evaluator.

### Fixed (P0 blockers)
- `bin/agent-init-project`: removed hardcoded `/home/chinh303/...` path from generated `AGENTS.md`; now portable runtime-agnostic reference.
- `bin/agent-init-project`: contract mismatch fixed — templates now copied to live `data_contract.json`, `metrics_sla.json`, `api_contract.json` that `config.yaml` points to.
- `bin/agent-init-project`: validates `--role engineer|scientist|both`, rejects bogus roles; `config.yaml` version `2.1`.
- `install.sh`: multi-runtime `--runtime gemini|claude|opencode|codex|all` with autodetect; no longer Gemini-only; verification uses direct `${BIN_DIR}/ak-eval --all --kits-dir`.
- `kit.yaml`: aligned to `2.1.0` (was 1.0.0 vs README V2.0 vs badge v2.15).

### Safety (P1)
- Added executable `engineer/hooks/guard.sh` + `scientist/hooks/guard.sh`: case-insensitive, blocks `sudo rm -rf /`, `--no-preserve-root`, `--force-with-lease`, `DROP DATABASE` any case, `TRUNCATE prod`, `rm -rf /data`, `aws s3 rm --recursive` on prod.
- `hooks.json`: `command` points to guard.sh; PreCommit/SessionEnd marked `optional` with fallbacks.
- GitNexus/rtk/Engram/specify/ak are now optional (degraded mode with warning) across `AGENTS.md`, skills (`scout`, `verify`, `review`), and installer.

### Evaluator (strict, zero-cost stdlib)
- `eval/evaluator.py V2.1`: `--kits-dir` + `$AGENTKIT_DIR` (defaults to repo root), `--strict` reserved.
- Tier 1: `ak` optional; checks skill structure (Protocol + Hard Rules + Deliverable/Verdict/Handoff), agent `self_challenge` rubric, executable guard.sh.
- Tier 2: executes real `guard.sh` incl. bypass variants + safe-allow checks; scaffold e2e in tmpdir (contracts exist, portable AGENTS.md, invalid role rejected).
- Tier 3: requires discipline + rubric for 5/5; honest score (v2.0 91.1% → v2.1 100%, 135/135).
- Baseline v2.0 log: `/tmp/agentkit-baseline-v20.log` (tag `v2.0-baseline`).

### Agents/Skills
- All 9 `agents/*.json` gain `self_challenge[3]` + Ponytail discipline sentence.
- `verify`: `systematic-debugging` → `debug` skill; GitNexus MCP primary with CLI/git fallback.
- `scout`/`review`: MCP primary, degraded-mode notes.

### Docs/CI
- README v2.1: multi-runtime install, degraded-mode note, evaluator usage, honest badge.
- Added `.github/workflows/smoke.yml`: shellcheck/py_compile + ak-eval strict + scaffold e2e.
