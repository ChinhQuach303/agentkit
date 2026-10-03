#!/usr/bin/env python3
"""Run runtime discovery checks in disposable temporary homes; never call a model."""

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_TARGETS = {
    "gemini": (".gemini/skills", "gemini", ["skills", "list", "--all"]),
    "claude": (".claude/skills", "claude", ["doctor"]),
    "opencode": (".config/opencode/skills", "opencode", ["debug", "skill"]),
    "codex": (".agents/skills", "codex", ["debug", "prompt-input"]),
}


def run_cli(argv, env, cwd):
    try:
        return subprocess.run(
            argv,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return error


def check_runtime(runtime):
    relative_root, executable, args = SKILL_TARGETS[runtime]
    cli = shutil.which(executable)
    if not cli:
        return "SKIP", f"{executable} CLI unavailable"

    with tempfile.TemporaryDirectory(prefix=f"agentkit-{runtime}-") as temp:
        home = Path(temp) / "home"
        project = Path(temp) / "project"
        skills_root = home / relative_root
        project.mkdir()
        skills_root.mkdir(parents=True)
        (home / ".codex").mkdir()
        env = dict(os.environ)
        env.update({
            "HOME": str(home),
            "XDG_CONFIG_HOME": str(home / ".config"),
            "XDG_CACHE_HOME": str(home / ".cache"),
            "CODEX_HOME": str(home / ".codex"),
            "CI": "1",
        })
        install_env = dict(env, AGENTKIT_SKIP_VERIFY="1")
        installed = run_cli(["bash", str(REPO_ROOT / "install.sh"), "--runtime", runtime], install_env, project)
        if isinstance(installed, Exception) or installed.returncode != 0:
            return "FAIL", f"isolated installer failed for {runtime}"
        cook_link = skills_root / "cook"
        if not cook_link.is_symlink() or cook_link.resolve() != REPO_ROOT / "engineer/skills/cook":
            return "FAIL", f"installer did not create the expected {runtime} skill link"

        result = run_cli([cli, *args], env, project)
        if isinstance(result, Exception):
            return "FAIL", f"CLI check failed: {type(result).__name__}"
        if result.returncode != 0:
            return "FAIL", f"{executable} exited {result.returncode}"
        output = result.stdout + "\n" + result.stderr

        if runtime == "claude":
            if not (skills_root / "cook" / "SKILL.md").is_file():
                return "FAIL", "isolated Claude skill path is missing SKILL.md"
            return "UNVERIFIED", "Claude doctor passed; CLI has no non-interactive skill inventory command"

        if runtime == "codex":
            try:
                messages = json.loads(result.stdout)
                text = "\n".join(
                    part.get("text", "")
                    for message in messages
                    for part in message.get("content", [])
                    if part.get("type") == "input_text"
                )
            except (json.JSONDecodeError, AttributeError, TypeError):
                return "FAIL", "Codex prompt-input output was not the expected JSON shape"
            if "Implement one approved plan phase with surgical minimal edits." not in text:
                return "FAIL", "Codex prompt input did not include the linked cook skill"
            return "PASS", "Codex prompt input contains the linked cook skill"

        if runtime == "gemini":
            if not re.search(r"cook\s+\[Enabled\]", output):
                return "FAIL", "Gemini skill inventory did not list cook as enabled"
            return "PASS", "Gemini skill inventory lists cook as enabled"

        if runtime == "opencode":
            if not re.search(r'"name"\s*:\s*"cook"', output):
                return "FAIL", "OpenCode skill inventory did not list cook"
            if str(skills_root / "cook" / "SKILL.md") not in output:
                return "FAIL", "OpenCode inventory did not resolve cook from the isolated kit path"
            return "PASS", "OpenCode skill inventory resolves cook from the isolated kit path"

    return "FAIL", "unhandled runtime"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", choices=[*SKILL_TARGETS, "all"], default="all")
    parser.add_argument(
        "--require-discovery",
        action="store_true",
        help="Fail if a runtime exposes no safe, non-interactive skill discovery check.",
    )
    args = parser.parse_args()
    runtimes = list(SKILL_TARGETS) if args.runtime == "all" else [args.runtime]
    failures = 0
    for runtime in runtimes:
        status, detail = check_runtime(runtime)
        print(f"[{status}] {runtime}: {detail}")
        if status == "FAIL" or (args.require_discovery and status != "PASS"):
            failures += 1
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
