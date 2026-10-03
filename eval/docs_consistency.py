#!/usr/bin/env python3
"""Check kit exports, README inventory/runtime facts, and local Markdown links."""

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_RE = re.compile(r"kit\.yaml\s+# Manifest v([0-9.]+) \((\d+) skills?, (\d+) agents?")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")


def parse_manifest(path):
    version = None
    exports = {}
    in_exports = False
    group = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^version:\s*", line):
            version = line.split(":", 1)[1].strip().strip("\"'")
        if line == "exports:":
            in_exports = True
            continue
        if not in_exports:
            continue
        if line and not line[0].isspace():
            break
        section = re.match(r"^  (skills|agents|hooks):\s*$", line)
        if section:
            group = section.group(1)
            exports[group] = []
            continue
        entry = re.match(r"^    - ([A-Za-z0-9._-]+)\s*$", line)
        if entry and group:
            exports[group].append(entry.group(1))
    if not version or not exports:
        raise ValueError(f"{path}: missing version or exports")
    return version, exports


def markdown_link_errors(root):
    errors = []
    for source in sorted(root.rglob("*.md")):
        if ".git" in source.parts:
            continue
        text = source.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("//") or not parsed.path:
                continue
            destination = (source.parent / unquote(parsed.path)).resolve()
            try:
                destination.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{source.relative_to(root)}: link escapes repository: {target}")
                continue
            if not destination.exists():
                errors.append(f"{source.relative_to(root)}: broken local link: {target}")
    return errors


def validate_repo(root=REPO_ROOT):
    errors = []
    manifests = {}
    for kit in ("engineer", "scientist"):
        path = root / kit / "kit.yaml"
        try:
            version, exports = parse_manifest(path)
        except (OSError, ValueError) as error:
            errors.append(str(error))
            continue
        manifests[kit] = (version, exports)
        actual_skills = sorted(
            child.name for child in (root / kit / "skills").iterdir() if child.is_dir()
        )
        actual_agents = sorted(path.stem for path in (root / kit / "agents").glob("*.json"))
        for kind, actual in (("skills", actual_skills), ("agents", actual_agents)):
            declared = sorted(exports.get(kind, []))
            if declared != actual:
                errors.append(f"{kit}: exports.{kind} differs from files (manifest={declared}, files={actual})")
        for skill in exports.get("skills", []):
            if not (root / kit / "skills" / skill / "SKILL.md").is_file():
                errors.append(f"{kit}: exported skill missing SKILL.md: {skill}")
        for hook in exports.get("hooks", []):
            if not (root / kit / "hooks" / hook).is_file():
                errors.append(f"{kit}: exported hook file missing: {hook}")

    readme_path = root / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    summaries = list(MANIFEST_RE.finditer(readme))
    if len(summaries) != 2:
        errors.append(f"README must contain one manifest summary per kit; found {len(summaries)}")
    for kit, match in zip(("engineer", "scientist"), summaries):
        if kit not in manifests:
            continue
        version, exports = manifests[kit]
        expected = (version, len(exports.get("skills", [])), len(exports.get("agents", [])))
        actual = (match.group(1), int(match.group(2)), int(match.group(3)))
        if actual != expected:
            errors.append(f"README {kit} manifest summary is {actual}; expected {expected}")

    installer = (root / "install.sh").read_text(encoding="utf-8")
    for variable, suffix in (("GEMINI_DIR", ".gemini/skills"), ("ANTIGRAVITY_DIR", ".gemini/config/skills")):
        if not re.search(rf'{variable}="\$\{{HOME\}}/{re.escape(suffix)}"', installer):
            errors.append(f"install.sh: {variable} no longer targets {suffix}")
        if suffix not in readme:
            errors.append(f"README.md: missing runtime path {suffix}")

    errors.extend(markdown_link_errors(root))
    return errors


def main():
    errors = validate_repo()
    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1
    print("[PASS] kit exports match skill/agent files")
    print("[PASS] README kit version/count summaries match manifests")
    print("[PASS] README runtime paths match installer targets")
    print("[PASS] local Markdown links resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
