# Hook Wiring (advisory screens, fail-open)

`guard.sh` screens a command string and exits 1 with `[BLOCK ...]` on match, 0 otherwise.
A snippet below only *runs* the screen — whether a non-zero exit blocks anything depends
entirely on the runtime. Verify signaling before relying on it; default posture is
notify/ask, not block.

## Install

Replace `$KIT_DIR` with the absolute path of this repo (e.g. `~/.local/share/agent-kits`):

```bash
KIT_DIR=~/.local/share/agent-kits
python3 -c "print(open('$KIT_DIR/engineer/hooks/claude-snippet.json').read().replace('\$KIT_DIR', '$KIT_DIR'))"
# merge the PreToolUse entry into ~/.claude/settings.json hooks (keep your existing entries)
```

## Verify signaling (do this first)

1. Dry-run the screen manually: `echo 'git push origin main --force' | $KIT_DIR/engineer/hooks/guard.sh; echo "exit=$?"` → expect exit 1.
2. In the runtime, run a harmless blocked-shaped command and observe: does the runtime surface the `[BLOCK]` text? Does it stop, ask, or ignore?
3. Claude Code: only an applicable `PreToolUse` denial blocks; timeout/crash/malformed output fails open (official doctrine).
4. Gemini/Antigravity: hook file uses a `decision` JSON protocol (`ask`/`block` semantics vary) — confirm against your app version before trusting a block.
5. If the runtime ignores the snippet, the content stays *inactive supporting content*: the skills still work, the screen just doesn't auto-run.

## Uninstall

Remove the merged `PreToolUse` entry pointing at `guard.sh` from your settings. Nothing else was touched.
