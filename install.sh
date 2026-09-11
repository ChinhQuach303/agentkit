#!/usr/bin/env bash
# ponytail: Idempotent installer for Universal AgentKit (Dual-Role Architecture V2.0)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${HOME}/.local/bin"
SKILLS_DIR="${HOME}/.gemini/config/skills"

echo "=== [AgentKit Installer] Installing Universal Dual-Role Toolkit V2.0 ==="
echo "Source: ${SCRIPT_DIR}"

# 1. Ensure ~/.local/bin exists
mkdir -p "${BIN_DIR}"

# 2. Symlink CLI binaries
echo "[+] Linking CLI binaries to ${BIN_DIR}..."
ln -sf "${SCRIPT_DIR}/bin/agent-init-project" "${BIN_DIR}/agent-init-project"
ln -sf "${SCRIPT_DIR}/eval/evaluator.py" "${BIN_DIR}/ak-eval"
chmod +x "${SCRIPT_DIR}/bin/agent-init-project" "${SCRIPT_DIR}/eval/evaluator.py"

# 3. Symlink skills to runtime if skills directory exists or is specified
if [ -d "${SKILLS_DIR}" ]; then
  echo "[+] Linking skills to runtime directory: ${SKILLS_DIR}..."
  # Engineer skills
  for skill_dir in "${SCRIPT_DIR}"/engineer/skills/*; do
    if [ -d "${skill_dir}" ]; then
      skill_name=$(basename "${skill_dir}")
      ln -sfn "${skill_dir}" "${SKILLS_DIR}/${skill_name}"
    fi
  done

  # Scientist skills
  for skill_dir in "${SCRIPT_DIR}"/scientist/skills/*; do
    if [ -d "${skill_dir}" ]; then
      skill_name=$(basename "${skill_dir}")
      ln -sfn "${skill_dir}" "${SKILLS_DIR}/${skill_name}"
    fi
  done
  echo "[+] Skills successfully linked."
fi

# 4. PATH check
if [[ ":$PATH:" != *":${BIN_DIR}:"* ]]; then
  echo "[!] Notice: ${BIN_DIR} is not in your current PATH."
  echo "    Add it to your shell rc (e.g. ~/.bashrc or ~/.zshrc):"
  echo "    export PATH=\"\${HOME}/.local/bin:\$PATH\""
fi

# 5. Run Verification
echo "[+] Running local verification..."
if command -v ak-eval >/dev/null 2>&1; then
  ak-eval --all
elif [ -f "${BIN_DIR}/ak-eval" ]; then
  "${BIN_DIR}/ak-eval" --all
fi

echo "=== [Complete] AgentKit installed successfully! ==="
echo "Usage:"
echo "  agent-init-project <path> --role [engineer|scientist|both]"
echo "  ak-eval --all"
