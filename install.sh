#!/usr/bin/env bash
# ponytail: Idempotent installer for Universal AgentKit (Dual-Role Architecture V2.1)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${HOME}/.local/bin"
RUNTIME_FILTER="${AGENTKIT_RUNTIME:-all}"

usage() {
  echo "Usage: ./install.sh [--runtime gemini|claude|opencode|codex|all]"
  echo "  Env AGENTKIT_RUNTIME overrides default (all)."
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --runtime)
      RUNTIME_FILTER="${2:-all}"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "[!] Unknown arg: $1" >&2
      usage
      exit 2
      ;;
  esac
done

echo "=== [AgentKit Installer] Installing Universal Dual-Role Toolkit V2.1 (runtime: ${RUNTIME_FILTER}) ==="
echo "Source: ${SCRIPT_DIR}"

# 1. Ensure ~/.local/bin exists
mkdir -p "${BIN_DIR}"

# 2. Symlink CLI binaries
echo "[+] Linking CLI binaries to ${BIN_DIR}..."
ln -sf "${SCRIPT_DIR}/bin/agent-init-project" "${BIN_DIR}/agent-init-project"
ln -sf "${SCRIPT_DIR}/eval/evaluator.py" "${BIN_DIR}/ak-eval"
chmod +x "${SCRIPT_DIR}/bin/agent-init-project" "${SCRIPT_DIR}/eval/evaluator.py"

# 3. Symlink skills to detected runtimes (multi-runtime, optional)
link_skills_to() {
  local dest="$1"
  mkdir -p "$dest"
  echo "[+] Linking skills to runtime directory: ${dest}..."
  for skill_dir in "${SCRIPT_DIR}"/engineer/skills/* "${SCRIPT_DIR}"/scientist/skills/*; do
    if [ -d "${skill_dir}" ]; then
      skill_name=$(basename "${skill_dir}")
      ln -sfn "${skill_dir}" "${dest}/${skill_name}"
    fi
  done
}

GEMINI_DIR="${HOME}/.gemini/config/skills"
CLAUDE_DIR="${HOME}/.claude/skills"
OPENCODE_DIR="${HOME}/.config/opencode/skills"
CODEX_DIR="${HOME}/.codex/skills"
LINKED_ANY=0

maybe_link() {
  local name="$1"
  local dir="$2"
  if [[ "$RUNTIME_FILTER" != "all" && "$RUNTIME_FILTER" != "$name" ]]; then
    return 0
  fi
  # ponytail: link if dir exists, or if explicitly requested via --runtime
  if [ -d "$dir" ] || [[ "$RUNTIME_FILTER" == "$name" ]]; then
    link_skills_to "$dir"
    LINKED_ANY=1
  else
    echo "[~] Runtime '$name' not detected at $dir; skipping (degraded mode OK)."
  fi
}

maybe_link gemini "$GEMINI_DIR"
maybe_link claude "$CLAUDE_DIR"
maybe_link opencode "$OPENCODE_DIR"
maybe_link codex "$CODEX_DIR"

if [[ "$LINKED_ANY" == "0" ]]; then
  echo "[!] No runtime skills dir found. Skills remain in-repo at engineer/skills + scientist/skills."
  echo "    Re-run with e.g. ./install.sh --runtime gemini to force a target."
fi

# 4. PATH check
if [[ ":$PATH:" != *":${BIN_DIR}:"* ]]; then
  echo "[!] Notice: ${BIN_DIR} is not in your current PATH."
  echo "    Add it to your shell rc (e.g. ~/.bashrc or ~/.zshrc):"
  echo "    export PATH=\"\${HOME}/.local/bin:\$PATH\""
fi

# 5. Run Verification (use direct path; PATH may not be reloaded yet)
echo "[+] Running local verification..."
if [ -x "${BIN_DIR}/ak-eval" ]; then
  "${BIN_DIR}/ak-eval" --all --kits-dir "${SCRIPT_DIR}" || echo "[!] Verification reported issues (see above)."
elif command -v ak-eval >/dev/null 2>&1; then
  ak-eval --all --kits-dir "${SCRIPT_DIR}" || echo "[!] Verification reported issues (see above)."
fi

echo "=== [Complete] AgentKit installed successfully! ==="
echo "Usage:"
echo "  agent-init-project <path> --role [engineer|scientist|both]"
echo "  ak-eval --all"
