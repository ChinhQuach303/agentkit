#!/usr/bin/env bash
# ponytail: Engineer destructive-command guard (enforce, not just declarative).
# Usage: guard.sh "<command>"  -> exit 0 allow, exit 1 block
#        echo "<command>" | guard.sh
set -uo pipefail

CMD="${*:-}"
if [ -z "$CMD" ]; then
  CMD="$(cat)"
fi
LOW="$(printf '%s' "$CMD" | tr '[:upper:]' '[:lower:]')"

block() {
  echo "[BLOCK engineer-guard] $1: $CMD" >&2
  exit 1
}

# 1. rm -rf variants on /, ~, $HOME, /data, /*, trailing wildcards
if printf '%s' "$LOW" | grep -Eq '(^|[;|&`$ ])(sudo[[:space:]]+)?rm[[:space:]]+[^;|&]*-[a-z]*r[a-z]*f'; then
  if printf '%s' "$LOW" | grep -Eq 'rm[[:space:]]+.*(^|[[:space:]])(/|/[*]|~|\$home|\$home/|/data|/data/)[[:space:]]*(--no-preserve-root)?[[:space:]]*$|rm[[:space:]]+.*(/[[:space:]]*$|~[[:space:]]*$|--no-preserve-root)'; then
    block "destructive rm target"
  fi
  # catch rm -rf / anything absolute root-level wipe
  if printf '%s' "$CMD" | grep -Eq 'rm[[:space:]]+.*-[a-zA-Z]*r[a-zA-Z]*f[^;]*[[:space:]]+/[[:space:]]*( |$|;)'; then
    block "destructive rm root"
  fi
fi

# 2. git force push
if printf '%s' "$LOW" | grep -Eq 'git[[:space:]]+push.*--force'; then
  block "git force push"
fi

# 3. DROP DATABASE (any case)
if printf '%s' "$LOW" | grep -Eq 'drop[[:space:]]+database'; then
  block "drop database"
fi

# 4. mkfs / dd to raw device (extra safety, cheap)
if printf '%s' "$LOW" | grep -Eq '(^|[;|& ])(mkfs|dd[[:space:]]+.*of=/dev/)'; then
  block "raw disk write"
fi

exit 0
