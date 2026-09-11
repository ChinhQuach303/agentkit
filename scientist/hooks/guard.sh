#!/usr/bin/env bash
# shellcheck disable=SC2016 # ponytail: $/backtick in grep -E patterns below are intentional regex literals, not shell expansions.
# ponytail: Scientist destructive-data guard (enforce).
# Usage: guard.sh "<command>" -> exit 0 allow, exit 1 block
set -uo pipefail

CMD="${*:-}"
if [ -z "$CMD" ]; then
  CMD="$(cat)"
fi
LOW="$(printf '%s' "$CMD" | tr '[:upper:]' '[:lower:]')"

block() {
  echo "[BLOCK scientist-guard] $1: $CMD" >&2
  exit 1
}

# 1. DROP TABLE/DATABASE on prod/production
if printf '%s' "$LOW" | grep -Eq 'drop[[:space:]]+(table|database).*prod'; then
  block "drop prod table/database"
fi
if printf '%s' "$LOW" | grep -Eq 'drop[[:space:]]+database'; then
  block "drop database"
fi

# 2. TRUNCATE prod
if printf '%s' "$LOW" | grep -Eq 'truncate.*prod'; then
  block "truncate prod"
fi

# 3. rm -rf /data variants
if printf '%s' "$LOW" | grep -Eq '(^|[;|&`$ ])(sudo[[:space:]]+)?rm[[:space:]]+.*-[a-z]*r[a-z]*f.*(/data|/warehouse|/lakehouse)'; then
  block "destructive rm data dir"
fi

# 4. aws s3 rm recursive on prod (prod anywhere in command)
if printf '%s' "$LOW" | grep -Eq 'aws[[:space:]]+s3[[:space:]]+rm.*--recursive'; then
  if printf '%s' "$LOW" | grep -Eq 'prod|s3://[^[:space:]]*prod'; then
    block "s3 recursive rm prod"
  fi
fi
if printf '%s' "$LOW" | grep -Eq 'aws[[:space:]]+s3api[[:space:]]+delete-bucket.*prod'; then
  block "s3 delete bucket prod"
fi

exit 0
