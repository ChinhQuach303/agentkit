# Universal AgentKit: Dual-Role Architecture V2.1

[![AgentKit Standard](https://img.shields.io/badge/AgentKit-Standard%20v2.1-blue.svg)](https://docs.agentkit.best)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Test Suite](https://img.shields.io/badge/ak--eval-passing-brightgreen.svg)]()

A domain-agnostic, multi-project AI agent toolkit inspired by [AgentKit](https://docs.agentkit.best). Built natively for modern AI coding assistants (Antigravity `agy`, Claude Code, OpenCode, Codex).

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
│   └── hooks/                  # hooks.json (optional) + guard.sh (enforce)
│       ├── hooks.json          # PreToolUse, PreCommit (optional), SessionEnd (optional)
│       └── guard.sh            # Executable destructive-command guard
│
├── scientist/                  # Role 2: Data Scientist / ML Engineer Kit
│   ├── kit.yaml                # Manifest v2.1.0 (5 skills, 4 agents, hooks)
│   ├── skills/                 # data-audit, pipeline-opt, model-eval, experiment-run, promote-gate
│   ├── agents/                 # Staff-Level Framing + self_challenge rubrics
│   │   ├── pipeline-optimizer.json, data-validator.json,
│   │   ├── ml-evaluator.json, experiment-tracker.json
│   ├── hooks/                  # hooks.json (optional) + guard.sh (enforce)
│   │   ├── hooks.json          # PreToolUse guard, PrePromotion (manifest signature check)
│   │   └── guard.sh
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
# multi-runtime:
./install.sh --runtime gemini
./install.sh --runtime claude
./install.sh --runtime all
```

This will:
1. Link `agent-init-project` and `ak-eval` to `~/.local/bin/`.
2. Link skills to detected runtime dirs (`~/.gemini/config/skills/`, `~/.claude/skills/`, `~/.config/opencode/skills/`, `~/.codex/skills/`). Missing runtimes are skipped (degraded mode OK).
3. Run the complete 3-Tier verification suite (`ak-eval --all --kits-dir .`).

Optional deps (degraded mode OK if missing): `gitnexus`, `rtk`, Engram MCP (`mem_*`), `specify`, `ak` CLI. Hooks `guard.sh` always enforce locally.

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

- **Tier 1 (Static Gate)**: `kit.yaml` versions, frontmatter, skill structure (Protocol+Hhard Rules+Deliverable/Verdict/Handoff), agent `self_challenge` rubric, executable `guard.sh`.
- **Tier 2 (Execution Gate)**: Executes real `guard.sh` (incl. bypass variants like `sudo rm -rf /`, `--force-with-lease`), temporal leakage check, HMAC-SHA256 tamper detection, plus `agent-init-project` scaffold e2e (contracts exist, no hardcoded home path, invalid role rejected).
- **Tier 3 (Cognitive Grading Gate)**: Scores agents on Role Clarity / Refusals / Ponytail+Rubric. Target ≥90% (v2.1 ships at 100%, 135/135).

---

## 5. Multi-Project Domain-Agnostic Design

- **Global Kits (`~/.local/share/agent-kits/`)**: 100% domain-agnostic. Contains zero hardcoded business table names, private APIs, or proprietary domain logic.
- **Local Project (`.agents/`)**: Project-specific SLA thresholds, dataset contracts, and table definitions live strictly inside the target repository.

---

## Contributing & License

Contributions, improvements, and custom role extensions are welcome!
Licensed under the [MIT License](LICENSE).
