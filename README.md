# Universal AgentKit: Dual-Role Architecture V2.0

[![AgentKit Standard](https://img.shields.io/badge/AgentKit-Standard%20v2.15-blue.svg)](https://docs.agentkit.best)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Test Suite](https://img.shields.io/badge/ak--eval-100%25%20passing-brightgreen.svg)]()

A production-grade, domain-agnostic, multi-project AI agent toolkit inspired by [AgentKit](https://docs.agentkit.best). Built natively for modern AI coding assistants (Antigravity `agy`, Claude Code, OpenCode, Codex).

Engineered with **Ponytail mode** (YAGNI, minimal footprint, standard library first) and **ADHD communication style** (next action first, zero filler, state restatement).

---

## Architecture Overview

```
agentkit/
├── bin/
│   ├── agent-init-project      # Universal project scaffolder CLI (v2.0)
│   └── ak-eval                 # Symlink to 3-tier test harness
├── install.sh                  # One-command idempotent installer
│
├── engineer/                   # Role 1: Software Engineer Kit (Full-Stack, Backend, DevOps)
│   ├── kit.yaml                # Manifest (8 skills, 5 agents, 1 hook file)
│   ├── skills/
│   │   ├── scout, plan, cook, verify, review, ship   # Tier 1: Macro-Phases
│   │   └── debug, fix                                # Tier 2: Atomic Action Skills
│   ├── agents/                 # Staff-Level Framing & 3-Tier Adversarial Rubrics
│   │   ├── code-explorer.json, ponytail-dev.json, test-engineer.json,
│   │   ├── code-reviewer.json, security-auditor.json
│   └── hooks/hooks.json        # PreToolUse, PreCommit, SessionEnd
│
├── scientist/                  # Role 2: Data Scientist / ML Engineer Kit
│   ├── kit.yaml                # Manifest (5 skills, 4 agents, 1 hook file)
│   ├── skills/                 # data-audit, pipeline-opt, model-eval, experiment-run, promote-gate
│   ├── agents/                 # Staff-Level Framing & 3-Tier Adversarial Rubrics
│   │   ├── pipeline-optimizer.json, data-validator.json,
│   │   ├── ml-evaluator.json, experiment-tracker.json
│   ├── hooks/hooks.json        # PreToolUse (gold tables guard), PrePromotion (manifest signature check)
│   └── templates/              # manifest.template.json, data_contract.template.json
│
└── eval/                       # 3-Tier Native Python Evaluation Suite
    └── evaluator.py            # Local evaluation harness (static, simulation, cognitive)
```

---

## 1. Quick Start

### Installation

Clone and install into your local environment in seconds:

```bash
git clone https://github.com/ChinhQuach303/agentkit.git ~/.local/share/agent-kits
cd ~/.local/share/agent-kits
./install.sh
```

This will:
1. Link `agent-init-project` and `ak-eval` to `~/.local/bin/`.
2. Link skills to your agent runtime environment (`~/.gemini/config/skills/`).
3. Run the complete 3-Tier verification suite.

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
| `scout` | Macro | Read-only codebase traversal, call-graph mapping & blast radius analysis with GitNexus. |
| `plan` | Macro | Atomic checklists, evidence-backed implementation roadmap (max 5 items, ADHD style). |
| `cook` | Macro | Ponytail implementation (YAGNI, minimal footprint, `// ponytail:` comment). |
| `verify` | Macro | Strict test suite execution and GitNexus `detect_changes` verification. |
| `review` | Macro | Multi-axis evaluation (correctness, over-engineering audit, security taint analysis). |
| `ship` | Macro | Atomic Git commit and architectural decision logging into Engram. |
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

All 9 subagents feature Staff-Level Cognitive Framing:
- **Mental Models**: First Principles, Blast Radius, Vectorized, Contract-Driven, Defense in Depth.
- **Banned Anti-Patterns**: Explicitly prohibits speculative abstractions, silent `dropna`, unverified mock tests, unindexed joins, and unpinned artifacts.
- **Adversarial Rubrics**: Each agent is mandated to self-challenge with 3 rigorous criteria before delivering results.

---

## 4. Evaluation Harness (`ak-eval`)

Evaluate your local kits without paying for external cloud LLM judges:

```bash
ak-eval --all
```

- **Tier 1 (Static Gate)**: Validates `kit.yaml` schema, agent JSON configurations, and skill markdown frontmatters.
- **Tier 2 (Execution Gate)**: Simulates destructive command interceptions, temporal leakage guardrails, and cryptographic HMAC-SHA256 tampering detection.
- **Tier 3 (Cognitive Grading Gate)**: Scores all agent instructions across mental models, banned anti-patterns, and self-challenge rubrics (standard target: >90%).

---

## 5. Multi-Project Domain-Agnostic Design

- **Global Kits (`~/.local/share/agent-kits/`)**: 100% domain-agnostic. Contains zero hardcoded business table names, private APIs, or proprietary domain logic.
- **Local Project (`.agents/`)**: Project-specific SLA thresholds, dataset contracts, and table definitions live strictly inside the target repository.

---

## Contributing & License

Contributions, improvements, and custom role extensions are welcome!
Licensed under the [MIT License](LICENSE).
