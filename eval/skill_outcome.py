#!/usr/bin/env python3
"""Grade a saved Skill output against deterministic artifact assertions."""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CORPUS_PATH = Path(__file__).with_name("skill_cases.json")
VALID_KITS = {"engineer", "scientist"}
VALID_KINDS = {"contains", "contains_regex"}


def load_cases(path=CORPUS_PATH):
    corpus = json.loads(Path(path).read_text(encoding="utf-8"))
    if corpus.get("schema_version") != 1 or not isinstance(corpus.get("cases"), list):
        raise ValueError("unsupported corpus schema")
    seen = set()
    for case in corpus["cases"]:
        if not isinstance(case, dict) or not all(case.get(key) for key in ("id", "kit", "skill", "prompt")):
            raise ValueError("each case needs id, kit, skill, and prompt")
        if case["id"] in seen:
            raise ValueError(f"duplicate case id: {case['id']}")
        seen.add(case["id"])
        if case["kit"] not in VALID_KITS:
            raise ValueError(f"unknown kit in {case['id']}: {case['kit']}")
        skill_path = REPO_ROOT / case["kit"] / "skills" / case["skill"] / "SKILL.md"
        if not skill_path.is_file():
            raise ValueError(f"skill file missing for case {case['id']}")
        for assertion in [*case.get("assertions", []), *case.get("forbidden", [])]:
            if assertion.get("kind") not in VALID_KINDS or not assertion.get("id") or not assertion.get("value"):
                raise ValueError(f"invalid assertion in {case['id']}")
            if assertion["kind"] == "contains_regex":
                re.compile(assertion["value"])
    return corpus["cases"]


def grade_artifact(case, artifact):
    results = []
    for group, expected in (("required", case.get("assertions", [])), ("forbidden", case.get("forbidden", []))):
        for assertion in expected:
            if assertion["kind"] == "contains":
                found = assertion["value"] in artifact
            else:
                found = re.search(assertion["value"], artifact) is not None
            results.append({
                "id": assertion["id"],
                "group": group,
                "passed": not found if group == "forbidden" else found,
            })
    return results


def skill_hash(case):
    path = REPO_ROOT / case["kit"] / "skills" / case["skill"] / "SKILL.md"
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    cases = load_cases()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_id", nargs="?", choices=[case["id"] for case in cases])
    parser.add_argument("artifact", nargs="?", type=Path, help="Saved text/Markdown output from the real Skill run")
    parser.add_argument("--list", action="store_true", help="List case prompts and skill mappings")
    parser.add_argument("--runtime", help="Runtime used for this run")
    parser.add_argument("--model", help="Model identifier used for this run")
    args = parser.parse_args()
    if args.list:
        print(json.dumps([
            {key: case[key] for key in ("id", "kit", "skill", "title", "prompt")}
            for case in cases
        ], indent=2))
        return 0
    if not args.case_id or not args.artifact or not args.runtime or not args.model:
        parser.error("grading requires CASE_ID ARTIFACT --runtime RUNTIME --model MODEL")
    case = next(item for item in cases if item["id"] == args.case_id)
    try:
        artifact = args.artifact.read_text(encoding="utf-8")
    except OSError as error:
        parser.error(f"cannot read artifact: {error}")
    checks = grade_artifact(case, artifact)
    result = {
        "schema_version": 1,
        "case_id": case["id"],
        "skill": f"{case['kit']}/{case['skill']}",
        "skill_sha256": skill_hash(case),
        "runtime": args.runtime,
        "model": args.model,
        "passed": all(check["passed"] for check in checks),
        "checks": checks,
        "limitations": "Deterministic artifact assertions only; this is not a semantic quality verdict.",
    }
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
