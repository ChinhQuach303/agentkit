# Universal AgentKit: Dual-Role Architecture V2.1

[![Custom Local Kits](https://img.shields.io/badge/AgentKit-Custom%20local%20kits%20v2.1-blue.svg)](https://docs.agentkit.best)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Test Suite](https://img.shields.io/badge/ak--eval-passing-brightgreen.svg)]()

A domain-agnostic, multi-project AI agent toolkit inspired by [AgentKit](https://docs.agentkit.best). Built natively for modern AI coding assistants (Antigravity `agy`, Claude Code, OpenCode, Codex).

> **Positioning (honest):** these are **custom local kits**, not registry Standard kits. They install via the bundled
> `install.sh` (symlinks, no `ak` dependency) and are designed to **complement the official Engineer Kit (stable 2.14)** —
> Ponytail fast-paths (`cook`, `fix`…) with handoff points to the full official workflows (`ak:test`, `ak:code-review`,
> `ak:security-scan`…). Skill slugs are bare (`cook`, not `ak:cook`), so triggers stay distinct from official
> `/ak:cook`-style invocations when both are installed. The `scientist` kit is fully custom (no official counterpart).
> Verified primary runtime: **Gemini/Antigravity**. See §6 Support matrix.

Engineered with **Ponytail mode** (YAGNI, minimal footprint, standard library first) and **ADHD communication style** (next action first, zero filler, state restatement).

---

## Architecture Overview

```
agentkit/
├── bin/
│   ├── agent-init-project      # Universal project scaffolder CLI (v2.1)
│   └── ak-eval                 # Symlink to 3-tier test harness
├── install.sh                  # One-command idempotent installer (--runtime gemini|claude|opencode|codex|all)
│
├── engineer/                   # Role 1: Software Engineer Kit (Full-Stack, Backend, DevOps)
│   ├── kit.yaml                # Manifest v2.1.0 (8 skills, 5 agents, hooks)
│   ├── skills/
│   │   ├── scout, plan, cook, verify, review, ship   # Tier 1: Macro-Phases
│   │   └── debug, fix                                # Tier 2: Atomic Action Skills
│   ├── agents/                 # Staff-Level Framing + self_challenge rubrics (3 questions each)
│   │   ├── code-explorer.json, ponytail-dev.json, test-engineer.json,
│   │   ├── code-reviewer.json, security-auditor.json
│   └── hooks/                  # hooks.json (optional) + guard.sh (advisory)
│       ├── hooks.json          # PreToolUse (advisory), PreCommit/SessionEnd checklists (see §3)
│       └── guard.sh            # Destructive-command screen (advisory, fail-open; see §3)
│
├── scientist/                  # Role 2: Data Scientist / ML Engineer Kit
│   ├── kit.yaml                # Manifest v2.1.0 (5 skills, 4 agents, hooks)
│   ├── skills/                 # data-audit, pipeline-opt, model-eval, experiment-run, promote-gate
│   ├── agents/                 # Staff-Level Framing + self_challenge rubrics
│   │   ├── pipeline-optimizer.json, data-validator.json,
│   │   ├── ml-evaluator.json, experiment-tracker.json
│   ├── hooks/                  # hooks.json (optional) + guard.sh (advisory)
│   │   ├── hooks.json          # PreToolUse screen (advisory), PrePromotion manifest check
│   │   └── guard.sh            # Destructive-data screen (advisory, fail-open; see §3)
│   └── templates/              # manifest.template.json, data_contract.template.json
│
└── eval/                       # 3-Tier Native Python Evaluation Suite (stdlib only, zero-cost)
    └── evaluator.py            # --kits-dir, --strict, scaffold e2e, guard.sh execution
```

---

## 1. Quick Start

### Installation

Clone and install into your local environment in seconds:

```bash
git clone https://github.com/ChinhQuach303/agentkit.git ~/.local/share/agent-kits
cd ~/.local/share/agent-kits
./install.sh
# multi-runtime + selection:
./install.sh --runtime gemini
./install.sh --runtime all --exclude-skills promote-gate
# preview, health, removal (custom lifecycle, no ak dependency):
./install.sh --runtime gemini --dry-run
./install.sh doctor
./install.sh uninstall --runtime gemini
```

This will:
1. Link `agent-init-project` and `ak-eval` to `~/.local/bin/`.
2. Link skills to detected runtime dirs (`~/.gemini/config/skills/`, `~/.claude/skills/`, `~/.config/opencode/skills/`, `~/.agents/skills/` for Codex user scope). Missing runtimes are skipped (degraded mode OK).
3. Back up (never overwrite) foreign content under `~/.agentkit-backups/<timestamp>/` and print the recovery path.
4. Run the complete 3-Tier verification suite (`ak-eval --all --kits-dir .`).

Optional deps (degraded mode OK if missing): `gitnexus`, `rtk`, Engram MCP (`mem_*`), `specify`, `ak` CLI.
`guard.sh` is an **advisory** screen (fail-open): it never replaces runtime permissions — a hook file alone does not
prove any runtime registered or executed it.

### Initialize a New Project

Run `agent-init-project` inside any project folder or specify the target directory:

```bash
# 1. Standard software engineering project
agent-init-project /path/to/my-web-app --role engineer

# 2. Data Science / ML / LLM pipeline project
agent-init-project /path/to/my-ml-model --role scientist

# 3. Hybrid project (both roles active)
agent-init-project /path/to/fullstack-ai --role both
```

This scaffolds:
- `.agents/config.yaml`: Role declaration, runtime runners, contract mappings.
- `.agents/contracts/`: Data contracts, metrics SLA, and API contracts.
- `.agents/AGENTS.md`: Role rules, phase triggers, and cognitive boundaries.
- `.agents/kit.yaml`: AgentKit project integration.

---

## 2. Dual-Role Kits

### Role 1: Software Engineer (`engineer`)
Designed for web services, distributed systems, backend APIs, CLIs, and DevOps:

| Phase / Skill | Tier | Description |
|---|---|---|
| `scout` | Macro | Read-only traversal, call-graph mapping & blast radius (GitNexus MCP when available, grep/AST fallback). |
| `plan` | Macro | Atomic checklists, evidence-backed implementation roadmap (max 5 items, ADHD style). |
| `cook` | Macro | Ponytail implementation (YAGNI, minimal footprint, `// ponytail:` comment). |
| `verify` | Macro | Strict test suite + blast-radius check (`detect_changes` when available, else git diff). |
| `review` | Macro | Multi-axis evaluation (correctness, over-engineering audit, taint analysis when available). |
| `ship` | Macro | Atomic Git commit and decision logging into Engram (optional). |
| `debug` | **Atomic** | Isolate root-cause proof via reproducible tests without premature code modification. |
| `fix` | **Atomic** | Cause-aligned minimal repair strictly bound to the proven defect with regression tests. |

### Role 2: Data Scientist (`scientist`)
Designed for data engineering, feature stores, model training, ML pipelines, and LLM evaluation:

| Phase / Skill | Tier | Description |
|---|---|---|
| `data-audit` | Macro/Atomic | Schema contract validation, nullability bounds, zero target/temporal leakage. |
| `pipeline-opt` | Macro/Atomic | DAG scheduling, dbt incremental optimization, vectorized Polars expressions over loops. |
| `model-eval` | Macro/Atomic | Multi-dimensional sliced evaluation, Simpson's paradox detection, deterministic LLM judge. |
| `experiment-run` | Macro | Reproducible artifact packaging, SHA-256 manifest generation, HMAC signature signing. |
| `promote-gate` | Macro | 3-tier promotion gating (Data Gate -> Performance Gate -> Integrity Gate). |

### Bridge to official skills (use together, not instead)

Ours are Ponytail fast-paths. When the official Engineer Kit is also installed, hand off at these points:

| Ours | Official | Handoff rule |
|---|---|---|
| `scout` | `ak:scout` / `ak:research` | Ours for a quick blast-radius map; official when you need deep evidence or cited research. |
| `plan` | `ak:plan` | Ours for an atomic ≤5-item checklist; official for phased `plan.md` artifacts, red-team, `--tdd`/`--yagni` gates. |
| `cook` | `ak:cook` | Ours implements the approved plan minimally; official adds modes, mandatory review, `--advice` checkpoints. |
| `verify` | `ak:test` | Prefer `ak:test` for independent validation; ours folds test + blast-radius in one pass. |
| `review` | `ak:security-scan` → `ak:code-review` | Run the read-only scan first, then review; ours is the single-pass alternative. |
| `ship` | `ak:git` → `ak:ship` | Use guarded git workflows, then official release gates; ours bundles commit + memory. |
| `debug` / `fix` | `ak:debug` / `ak:fix` | Same contract (prove cause → minimal repair); interchangeable. |
| `ship` (memory) | `ak:handoff` / `ak:journal` | No Engram? Write `HANDOFF.md` (Goal/Decisions/Evidence/Blockers) so any session can resume. |

Coexistence decisions (P0 audit, verified by probe):
- **Skill names stay bare** (`cook`, not `ak:cook`): triggers differ from official `/ak:cook`-style invocations; both kits install side-by-side (verified in `~/.gemini/config/skills/` next to `debugger`, `code-reviewer`, …).
- **`.agents/` scaffold dir stays**: official Codex skills land in `.agents/skills/` alongside our `config.yaml`/`contracts/`/`AGENTS.md` with no overwrite (probed).
- **No `ak` dependency**: `ak kit validate` passes on absolute paths, but the ak adapter discovers 0 skills from this layout (probed on codex + claude-code targets), so `install.sh` remains the supported install path.

---

## 3. Cognitive Framing & Anti-Patterns

All 9 subagents feature Staff-Level Cognitive Framing + `self_challenge` (3 questions, stored in each `agents/*.json`):
- **Mental Models**: First Principles, Blast Radius, Vectorized, Contract-Driven, Defense in Depth.
- **Banned Anti-Patterns**: Explicitly prohibits speculative abstractions, silent `dropna`, unverified mock tests, unindexed joins, and unpinned artifacts.
- **Adversarial Rubrics**: Each agent must answer its 3 `self_challenge` criteria before delivering results (checked by `ak-eval` Tier 1+3).

---

## 4. Evaluation Harness (`ak-eval`)

Evaluate your local kits without paying for external cloud LLM judges (stdlib only):

```bash
ak-eval --all --kits-dir ~/.local/share/agent-kits
# or inside repo:
./eval/evaluator.py --all --kits-dir .
```

- **Tier 1 (Static Gate)**: `kit.yaml` versions, frontmatter, skill structure (Protocol+Hard Rules+Deliverable/Verdict/Handoff), agent `self_challenge` rubric, executable `guard.sh`.
- **Tier 2 (Execution Gate)**: Executes real `guard.sh` (incl. bypass variants like `sudo rm -rf /`, `--force-with-lease`), temporal leakage check, HMAC-SHA256 tamper detection, plus `agent-init-project` scaffold e2e (contracts exist, no hardcoded home path, invalid role rejected).
- **Tier 3 (Cognitive Grading Gate)**: Scores agents on Role Clarity / Refusals / Ponytail+Rubric. Target ≥90% (v2.1 ships at 100%, 135/135).

---

## 5. Multi-Project Domain-Agnostic Design

- **Global Kits (`~/.local/share/agent-kits/`)**: Domain-agnostic. No hardcoded business table names, private APIs, or proprietary domain logic.
- **Local Project (`.agents/`)**: Project-specific SLA thresholds, dataset contracts, and table definitions live strictly inside the target repository.

---

## 6. Runtime Support Matrix

| Runtime | Status | Notes |
|---|---|---|
| Gemini / Antigravity (`~/.gemini/config/skills/`) | **Verified (primary)** | Trigger = skill dir name (`cook`, `data-audit`, …). Coexists with other skills. |
| Claude Code (`~/.claude/skills/`) | Best-effort | Symlinked bare names (`/cook`), distinct from official `/ak:cook`. No plugin delivery. |
| OpenCode (`~/.config/opencode/skills/`) | Best-effort | Same symlink layout; verify discovery per version. |
| Codex (`~/.agents/skills/` user scope) | Supported | Same symlink layout; `doctor` verifies. Shares `.agents/` parent harmlessly with scaffolded project files (different paths). |
| Cursor / Pi / OMP / Grok | Not supported | Docs-only. File presence ≠ active (adapter doctrine). |

Troubleshooting (adapted from official): if a runtime cannot find a skill, check (1) target dir the *running* runtime actually reads,
(2) project vs user scope, (3) restart the session so it reloads, (4) `ak-eval` still green — before reinstalling or forcing anything.

`doctor` exit codes: `0` = healthy or simply not installed (MISS is info; filter with `--runtime`);
`1` = broken/dangling links or foreign content. Foreign `WARN`s also appear when live links point at a *different*
clone than the source you run doctor from (e.g. repo at `~/orca/agentkit` vs installed copy at
`~/.local/share/agent-kits`): sync the copies (pull/re-clone) and reinstall from the copy you want to own the links.

---

## Contributing & License

Contributions, improvements, and custom role extensions are welcome!
Licensed under the [MIT License](LICENSE).
