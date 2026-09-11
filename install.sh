#!/usr/bin/env bash
# ponytail: Idempotent installer for Universal AgentKit (Dual-Role Architecture V2.1)
# Custom local installer (no ak dependency): preview, backup, uninstall, skill selection, doctor.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${HOME}/.local/bin"
RUNTIME_FILTER="${AGENTKIT_RUNTIME:-all}"
ACTION="install"
DRY_RUN=0
SKILLS_ONLY=""
SKILLS_EXCLUDE=""
BACKUP_ROOT="${AGENTKIT_BACKUP_DIR:-${HOME}/.agentkit-backups}"

usage() {
  echo "Usage: ./install.sh [install|uninstall|doctor] [--runtime gemini|claude|opencode|codex|all]"
  echo "                     [--skills a,b] [--exclude-skills c] [--dry-run]"
  echo "  Env AGENTKIT_RUNTIME / AGENTKIT_BACKUP_DIR override defaults."
  echo "  install (default): preview-able symlink install with backup of foreign content."
  echo "  uninstall: remove only symlinks pointing at this repo; never touch real files."
  echo "  doctor: report link health per runtime (dangling, foreign, missing)."
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    install|uninstall|doctor)
      ACTION="$1"
      shift
      ;;
    --runtime)
      RUNTIME_FILTER="${2:-all}"
      shift 2
      ;;
    --skills)
      SKILLS_ONLY="${2:-}"
      shift 2
      ;;
    --exclude-skills)
      SKILLS_EXCLUDE="${2:-}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
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

GEMINI_DIR="${HOME}/.gemini/config/skills"
CLAUDE_DIR="${HOME}/.claude/skills"
OPENCODE_DIR="${HOME}/.config/opencode/skills"
CODEX_DIR="${HOME}/.agents/skills"

# ponytail: ownership = symlink resolving under this repo. Never adopt real files.
is_ours() {
  local p="$1"
  [[ -L "$p" ]] || return 1
  local target
  target="$(readlink -f "$p" 2>/dev/null || true)"
  [[ -n "$target" && "$target" == "${SCRIPT_DIR}/"* ]]
}

# ours-but-dangling (repo moved): plain readlink works on broken links
is_ours_dangling() {
  local p="$1"
  [[ -L "$p" ]] || return 1
  local target
  target="$(readlink "$p" 2>/dev/null || true)"
  [[ "$target" == "${SCRIPT_DIR}/"* || "$target" == "${SCRIPT_DIR}" ]]
}

wanted_skill() {
  local name="$1"
  if [[ -n "$SKILLS_ONLY" && ",${SKILLS_ONLY}," != *",${name},"* ]]; then
    return 1
  fi
  if [[ -n "$SKILLS_EXCLUDE" && ",${SKILLS_EXCLUDE}," == *",${name},"* ]]; then
    return 1
  fi
  return 0
}

runtime_dirs() {
  # echo "name dir" lines honoring filter
  for pair in "gemini:${GEMINI_DIR}" "claude:${CLAUDE_DIR}" "opencode:${OPENCODE_DIR}" "codex:${CODEX_DIR}"; do
    local name="${pair%%:*}"
    local dir="${pair#*:}"
    if [[ "$RUNTIME_FILTER" == "all" || "$RUNTIME_FILTER" == "$name" ]]; then
      echo "$name $dir"
    fi
  done
}

do_install() {
  echo "=== [AgentKit Installer] Installing Universal Dual-Role Toolkit V2.1 (runtime: ${RUNTIME_FILTER}) ==="
  echo "Source: ${SCRIPT_DIR}"
  [[ "$DRY_RUN" == "1" ]] && echo "(dry-run: preview only, no writes)"

  local stamp=""
  stamp="$(date +%Y%m%d-%H%M%S)"
  local backed_up=0

  # 1. CLI binaries
  for pair in "agent-init-project:bin/agent-init-project" "ak-eval:eval/evaluator.py"; do
    local linkname="${pair%%:*}"
    local src="${SCRIPT_DIR}/${pair#*:}"
    local dest="${BIN_DIR}/${linkname}"
    if is_ours "$dest"; then
      echo "[=] up-to-date: $dest"
      continue
    elif [[ -e "$dest" || -L "$dest" ]]; then
      echo "[!] foreign content at $dest — backing up, not overwriting blindly"
      [[ "$DRY_RUN" == "0" ]] || continue
      mkdir -p "${BACKUP_ROOT}/${stamp}/bin"
      mv "$dest" "${BACKUP_ROOT}/${stamp}/bin/${linkname}"
      backed_up=1
    fi
    if [[ "$DRY_RUN" == "1" ]]; then
      echo "[dry-run] link $dest -> $src"
    else
      mkdir -p "${BIN_DIR}"
      ln -sfn "$src" "$dest"
      echo "[+] linked $dest"
    fi
  done
  [[ "$DRY_RUN" == "0" ]] && chmod +x "${SCRIPT_DIR}/bin/agent-init-project" "${SCRIPT_DIR}/eval/evaluator.py"

  # 2. Skills per runtime
  while read -r name dir; do
    if [[ ! -d "$dir" ]]; then
      if [[ "$RUNTIME_FILTER" == "$name" ]]; then
        [[ "$DRY_RUN" == "1" ]] || mkdir -p "$dir"
        echo "[+] created runtime dir: $dir"
      else
        echo "[~] Runtime '$name' not detected at $dir; skipping (degraded mode OK)."
        continue
      fi
    fi
    echo "[+] Linking skills to runtime directory ($name): ${dir}..."
    for skill_dir in "${SCRIPT_DIR}"/engineer/skills/* "${SCRIPT_DIR}"/scientist/skills/*; do
      [[ -d "$skill_dir" ]] || continue
      local skill_name
      skill_name=$(basename "$skill_dir")
      wanted_skill "$skill_name" || { echo "    [skip] $skill_name (selection)"; continue; }
      local dest="${dir}/${skill_name}"
      if is_ours "$dest"; then
        echo "    [=] up-to-date: $skill_name"
        continue
      fi
      if [[ -e "$dest" || -L "$dest" ]]; then
        echo "    [!] foreign content at $dest — backing up"
        if [[ "$DRY_RUN" == "0" ]]; then
          mkdir -p "${BACKUP_ROOT}/${stamp}/${name}"
          mv "$dest" "${BACKUP_ROOT}/${stamp}/${name}/${skill_name}"
          backed_up=1
        fi
      fi
      if [[ "$DRY_RUN" == "1" ]]; then
        echo "    [dry-run] link $dest -> $skill_dir"
      else
        ln -sfn "$skill_dir" "$dest"
        echo "    [+] linked $skill_name"
      fi
    done
  done < <(runtime_dirs)

  if [[ "$backed_up" == "1" ]]; then
    echo "[*] Recovery snapshot (analogue): ${BACKUP_ROOT}/${stamp}/ — keep until verified."
  fi

  # 3. PATH check
  if [[ ":$PATH:" != *":${BIN_DIR}:"* ]]; then
    echo "[!] Notice: ${BIN_DIR} is not in your current PATH."
    echo "    Add it to your shell rc (e.g. ~/.bashrc or ~/.zshrc):"
    echo "    export PATH=\"\${HOME}/.local/bin:\$PATH\""
  fi

  # 4. Verification (skipped in dry-run or AGENTKIT_SKIP_VERIFY=1, e.g. nested eval e2e)
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "[dry-run] would run: ak-eval --all --kits-dir ${SCRIPT_DIR}"
  elif [[ "${AGENTKIT_SKIP_VERIFY:-0}" == "1" ]]; then
    echo "[~] Verification skipped (AGENTKIT_SKIP_VERIFY=1)"
  else
    echo "[+] Running local verification..."
    if [ -x "${BIN_DIR}/ak-eval" ]; then
      "${BIN_DIR}/ak-eval" --all --kits-dir "${SCRIPT_DIR}" || echo "[!] Verification reported issues (see above)."
    elif command -v ak-eval >/dev/null 2>&1; then
      ak-eval --all --kits-dir "${SCRIPT_DIR}" || echo "[!] Verification reported issues (see above)."
    fi
  fi

  echo "=== [Complete] AgentKit installed successfully! ==="
  echo "Usage:"
  echo "  agent-init-project <path> --role [engineer|scientist|both]"
  echo "  ak-eval --all"
}

do_uninstall() {
  echo "=== [AgentKit Uninstaller] Removing only repo-owned symlinks (source: ${SCRIPT_DIR}) ==="
  [[ "$DRY_RUN" == "1" ]] && echo "(dry-run: preview only, no writes)"
  local removed=0
  for bin in agent-init-project ak-eval; do
    local dest="${BIN_DIR}/${bin}"
    if is_ours "$dest"; then
      if [[ "$DRY_RUN" == "1" ]]; then
        echo "[dry-run] remove $dest"
      else
        rm "$dest"
        echo "[-] removed $dest"
      fi
      removed=1
    else
      echo "[~] kept (not ours): $dest"
    fi
  done
  while read -r name dir; do
    [[ -d "$dir" ]] || continue
    for skill_dir in "${SCRIPT_DIR}"/engineer/skills/* "${SCRIPT_DIR}"/scientist/skills/*; do
      [[ -d "$skill_dir" ]] || continue
      local skill_name
      skill_name=$(basename "$skill_dir")
      local dest="${dir}/${skill_name}"
      if is_ours "$dest"; then
        if [[ "$DRY_RUN" == "1" ]]; then
          echo "[dry-run] remove $dest"
        else
          rm "$dest"
          echo "[-] removed ($name) $dest"
        fi
        removed=1
      fi
    done
  done < <(runtime_dirs)
  [[ "$removed" == "0" ]] && echo "[=] Nothing owned found; unknown or user content preserved."
  echo "=== [Done] Uninstall complete. Backups (if any) live under ${BACKUP_ROOT}/ ==="
}

do_doctor() {
  local issues=0
  local missing=0
  echo "=== [AgentKit Doctor] source: ${SCRIPT_DIR} ==="
  echo "(ownership = symlink resolving under source; foreign links are WARN, absent skills are info)"
  for bin in agent-init-project ak-eval; do
    local dest="${BIN_DIR}/${bin}"
    if is_ours "$dest"; then
      if [[ -e "$dest" ]]; then
        echo "[OK] bin $bin -> $(readlink "$dest")"
      else
        echo "[BROKEN] bin $bin is dangling: $dest"; issues=1
      fi
    elif [[ -L "$dest" ]]; then
      echo "[WARN] bin $bin is a foreign/dangling symlink: $dest"; issues=1
    elif [[ -e "$dest" ]]; then
      echo "[WARN] bin $bin is a foreign file: $dest"; issues=1
    else
      echo "[MISS] bin $bin not linked: $dest"; missing=1
    fi
  done
  while read -r name dir; do
    if [[ ! -d "$dir" ]]; then
      echo "[~] runtime '$name' absent: $dir"
      continue
    fi
    for skill_dir in "${SCRIPT_DIR}"/engineer/skills/* "${SCRIPT_DIR}"/scientist/skills/*; do
      [[ -d "$skill_dir" ]] || continue
      local skill_name
      skill_name=$(basename "$skill_dir")
      local dest="${dir}/${skill_name}"
      if is_ours "$dest"; then
        if [[ -e "$dest" ]]; then
          echo "[OK] ($name) $skill_name"
        else
          echo "[BROKEN] ($name) dangling: $dest"
          issues=1
        fi
      elif is_ours_dangling "$dest"; then
        echo "[BROKEN] ($name) ours but dangling (source moved?): $dest"; issues=1
      elif [[ -L "$dest" ]]; then
        echo "[WARN] ($name) $skill_name is a foreign symlink"; issues=1
      elif [[ -e "$dest" ]]; then
        echo "[WARN] ($name) $skill_name is foreign content (would be backed up on install)"; issues=1
      else
        echo "[MISS] ($name) $skill_name not installed"; missing=1
      fi
    done
  done < <(runtime_dirs)
  if [[ "$issues" == "0" ]]; then
    if [[ "$missing" == "0" ]]; then
      echo "[OK] All checked links healthy."
    else
      echo "[OK] No breakage. MISS entries = runtimes/skills not installed (filter with --runtime, or install to add)."
    fi
    return 0
  else
    echo "[!] Breakage or foreign content found (see above). Re-run install (backs up foreign content) or uninstall first."
    return 1
  fi
}

case "$ACTION" in
  install) do_install ;;
  uninstall) do_uninstall ;;
  doctor) do_doctor ;;
esac
