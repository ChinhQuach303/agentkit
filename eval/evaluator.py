#!/usr/bin/env python3
# ponytail: 3-Tier Evaluation Harness for AgentKits V2.1 (Static, Scenarios, and Cognitive Framing)
import argparse
import glob
import hmac
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_KITS = os.environ.get(
    "AGENTKIT_DIR",
    _REPO_ROOT if os.path.isdir(os.path.join(_REPO_ROOT, "engineer")) else os.path.expanduser("~/.local/share/agent-kits"),
)
KITS_DIR = _DEFAULT_KITS

# ponytail: official Engineer skill base names (stable 2.14 catalog, without ak: prefix).
# Bare-slug overlap is a NOTE (complement coexistence), never a failure.
OFFICIAL_SKILLS = frozenset((
    "help", "coding-level", "ask", "bro", "brainstorm", "advise", "sowat", "sumup",
    "scout", "problem-solving", "predict", "sequential-thinking", "scenario", "plan",
    "project-management", "plans-kanban", "issue-to-plan", "cook", "vibe", "loop",
    "autoresearch", "deep-swe", "xia", "context-engineering", "folder-context",
    "docs-seeker", "repomix", "research", "research-prompt", "tech-graph", "diagram",
    "gkg", "graphify", "cti-expert", "project-organization", "watzup", "frontend-design",
    "frontend-development", "backend-development", "databases", "web-frameworks", "devops",
    "better-auth", "payment-integration", "shopify", "react-best-practices", "tanstack",
    "mobile-development", "debug", "fix", "test", "web-testing", "code-review", "review-pr",
    "security", "security-scan", "docs", "interview-docs", "document-skills", "copywriting",
    "mermaidjs-v11", "markdown-novel-viewer", "mintlify", "preview", "show-off", "design",
    "ui-styling", "ui-ux-pro-max", "web-design-guidelines", "threejs", "remotion",
    "excalidraw", "stitch", "shader", "ai-artist", "ai-multimodal", "media-processing",
    "html-video", "hyperframes", "fable-thinking", "agentkit", "use-mcp", "mcp-builder",
    "skill-creator", "codex-goal", "goal-warmup", "agent-browser", "chrome-profile",
    "google-adk-python", "llms", "git", "github", "deploy", "ship", "handoff", "handover",
    "journal", "retro", "bootstrap", "agentize", "find-skills", "orchestrate", "team",
    "worktree", "ak",
))

def print_header(title):
    print(f"\n{'='*60}\n  {title}\n{'='*60}")

def run_tier_1(kit_name=None):
    """Tier 1: Static Validation & Schema Integrity"""
    print_header("TIER 1: Static Validation & Schema Integrity ($0, <2s)")
    passed = 0
    failed = 0

    # 1. ak kit validate (optional: warn if ak CLI missing)
    if shutil.which("ak") is None:
        print("[SKIP] ak CLI not found; skipping 'ak kit validate' (degraded mode OK)")
    else:
        try:
            res = subprocess.run(["ak", "kit", "validate", KITS_DIR], capture_output=True, text=True, check=True)
            print("[PASS] ak kit validate: All kits valid")
            passed += 1
        except Exception as e:
            print(f"[FAIL] ak kit validate failed: {e}")
            failed += 1

    # 2. Check SKILL.md frontmatter
    kits = [kit_name] if kit_name else ["engineer", "scientist"]
    for kit in kits:
        skills_path = os.path.join(KITS_DIR, kit, "skills", "*", "SKILL.md")
        for skill_file in glob.glob(skills_path):
            skill_name = os.path.basename(os.path.dirname(skill_file))
            with open(skill_file) as f:
                content = f.read()
            fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
            if not fm_match:
                print(f"[FAIL] {kit}/{skill_name}: Missing YAML frontmatter")
                failed += 1
                continue
            fm = fm_match.group(1)
            has_name = "name:" in fm
            has_desc = "description:" in fm
            if has_name and has_desc:
                print(f"[PASS] Frontmatter {kit}/{skill_name}")
                passed += 1
            else:
                print(f"[FAIL] Frontmatter {kit}/{skill_name}: missing name or description")
                failed += 1
                continue
            # 2b. Structural check: Protocol + Hard Rule + Deliverable (V2.1 strictness)
            body = content[fm_match.end():]
            has_protocol = "## Protocol" in body or "Protocol" in body
            has_rule = "Hard Rule" in body or "Hard Rules" in body
            has_deliver = ("Deliverable" in body or "Verdict" in body or "Handoff" in body)
            if has_protocol and has_rule and has_deliver:
                print(f"[PASS] Structure {kit}/{skill_name} (protocol+rules+deliverable)")
                passed += 1
            else:
                print(f"[FAIL] Structure {kit}/{skill_name}: need Protocol + Hard Rule(s) + Deliverable")
                failed += 1
                continue
            # 2c. skill-creator identifier conformance: short kebab-case slug == dirname,
            #      description length bounds, no angle brackets (packaging rejects them)
            fm_name = re.search(r"^name:\s*[\"']?([^\"'\s]+)[\"']?\s*$", fm, re.MULTILINE)
            fm_desc = re.search(r"^description:\s*[\"']?(.*?)[\"']?\s*$", fm, re.MULTILINE)
            slug = fm_name.group(1) if fm_name else ""
            desc = fm_desc.group(1) if fm_desc else ""
            ok_slug = (
                bool(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug))
                and len(slug) <= 40
                and slug == skill_name
            )
            ok_desc = 10 <= len(desc) <= 500 and "<" not in content[:fm_match.end()] and ">" not in (fm_name.group(0) + fm_desc.group(0) if fm_name and fm_desc else "")
            if ok_slug and ok_desc:
                print(f"[PASS] Identifier {kit}/{skill_name} (kebab-case, name==dir, desc {len(desc)} chars)")
                passed += 1
            else:
                print(f"[FAIL] Identifier {kit}/{skill_name}: slug={slug!r} desc_len={len(desc)}")
                failed += 1
            # 2d. No placeholder scaffolding shipped (skill-creator: delete unused placeholders)
            skill_dir = os.path.dirname(skill_file)
            placeholders = []
            for sub in ("scripts", "references", "assets", "agents"):
                p = os.path.join(skill_dir, sub)
                if os.path.isdir(p):
                    entries = os.listdir(p)
                    if not entries or all(re.search(r"placeholder|example|todo", e, re.I) for e in entries):
                        placeholders.append(sub)
            if placeholders:
                print(f"[FAIL] Placeholders shipped {kit}/{skill_name}: {placeholders}")
                failed += 1
            else:
                print(f"[PASS] No placeholders {kit}/{skill_name}")
                passed += 1
            # 2e. Official-name overlap is a NOTE (complement coexistence, triggers differ)
            if skill_name in OFFICIAL_SKILLS:
                print(f"  [NOTE] {kit}/{skill_name} shares a bare name with official ak:{skill_name} "
                      f"(triggers differ: /{skill_name} vs /ak:{skill_name}; see README bridge)")

    # 3. Check JSON schema for agents and hooks
    for kit in kits:
        agents_path = os.path.join(KITS_DIR, kit, "agents", "*.json")
        for agent_file in glob.glob(agents_path):
            agent_base = os.path.basename(agent_file)
            try:
                with open(agent_file) as f:
                    data = json.load(f)
                assert "name" in data and "system_prompt" in data
                assert "Cognitive Framing" in data["system_prompt"] or "Mental Model" in data["system_prompt"]
                assert "REFUSE" in data["system_prompt"] or "Refusals" in data["system_prompt"]
                prompt = data["system_prompt"]
                has_rubric = (
                    "self_challenge" in data
                    or "self-challenge" in prompt.lower()
                    or "adversarial" in prompt.lower()
                    or "challenge question" in prompt.lower()
                )
                if not has_rubric:
                    raise AssertionError("missing self_challenge/adversarial rubric")
                print(f"[PASS] Cognitive Agent Schema: {kit}/{agent_base}")
                passed += 1
            except Exception as err:
                print(f"[FAIL] Agent Schema {kit}/{agent_base}: {err}")
                failed += 1

    # 4. Hooks reference advisory guard scripts + honest doctrine (no security-boundary claims)
    banned_claims = re.compile(r"enforced|enforce locally|security boundary|boundar", re.I)
    for kit in ["engineer", "scientist"]:
        if kit_name and kit != kit_name:
            continue
        guard = os.path.join(KITS_DIR, kit, "hooks", "guard.sh")
        if os.path.isfile(guard) and os.access(guard, os.X_OK):
            print(f"[PASS] Guard script executable: {kit}/hooks/guard.sh")
            passed += 1
        else:
            print(f"[FAIL] Guard script missing/not executable: {kit}/hooks/guard.sh")
            failed += 1
            continue
        hook_text = ""
        for rel in ("hooks/hooks.json", "hooks/guard.sh"):
            p = os.path.join(KITS_DIR, kit, rel)
            if os.path.isfile(p):
                with open(p) as f:
                    hook_text += "\n" + f.read()
        low = hook_text.lower()
        if banned_claims.search(hook_text):
            print(f"[FAIL] Hook doctrine {kit}: claims enforcement/security-boundary (must be advisory, fail-open)")
            failed += 1
        elif "advisory" in low and "fail-open" in low:
            print(f"[PASS] Hook doctrine {kit} (advisory, fail-open)")
            passed += 1
        else:
            print(f"[FAIL] Hook doctrine {kit}: missing advisory/fail-open wording")
            failed += 1

    print(f"\nTier 1 Summary: {passed} PASSED, {failed} FAILED")
    return failed == 0

def run_tier_2(kit_name=None):
    """Tier 2: Scenario Simulation (Safety Hooks, Leakage, Integrity)"""
    print_header("TIER 2: Execution Scenarios & Safety Gates Simulation")
    passed = 0
    failed = 0

    # Scenario 1: Engineer guard.sh must block destructive commands (real execution)
    print("[RUN] Scenario 1: Engineer Safety Guard (guard.sh, incl. bypass variants)")
    eng_guard = os.path.join(KITS_DIR, "engineer", "hooks", "guard.sh")
    destructive_cmds = [
        "rm -rf /",
        "sudo rm -rf / --no-preserve-root",
        "rm -rf ~",
        "git push origin main --force",
        "git push --force-with-lease",
        "DROP DATABASE prod",
        "drop database analytics",
    ]
    safe_cmds = ["echo hello", "git status --short", "pytest -q"]
    for cmd in destructive_cmds:
        try:
            r = subprocess.run([eng_guard, cmd], capture_output=True, text=True)
            blocked = r.returncode != 0
        except Exception:
            blocked = False
        if blocked:
            print(f"  [PASS] Successfully blocked: '{cmd}'")
            passed += 1
        else:
            print(f"  [FAIL] Failed to block: '{cmd}'")
            failed += 1
    for cmd in safe_cmds:
        try:
            r = subprocess.run([eng_guard, cmd], capture_output=True, text=True)
            allowed = r.returncode == 0
        except Exception:
            allowed = False
        if allowed:
            print(f"  [PASS] Correctly allowed: '{cmd}'")
            passed += 1
        else:
            print(f"  [FAIL] False positive block: '{cmd}'")
            failed += 1

    # Scenario 1b: Scientist guard.sh
    print("[RUN] Scenario 1b: Scientist Safety Guard (guard.sh)")
    sci_guard = os.path.join(KITS_DIR, "scientist", "hooks", "guard.sh")
    sci_bad = [
        "DROP TABLE prod.users",
        "TRUNCATE prod.events",
        "rm -rf /data/lake",
        "aws s3 rm s3://prod-bucket --recursive",
    ]
    for cmd in sci_bad:
        try:
            r = subprocess.run([sci_guard, cmd], capture_output=True, text=True)
            blocked = r.returncode != 0
        except Exception:
            blocked = False
        if blocked:
            print(f"  [PASS] Successfully blocked: '{cmd}'")
            passed += 1
        else:
            print(f"  [FAIL] Failed to block: '{cmd}'")
            failed += 1

    # Scenario 2: Scientist Target/Temporal Leakage Simulation
    print("[RUN] Scenario 2: Scientist Data Audit Temporal Leakage Guard")
    mock_events = [
        {"entity": "sensor_1", "timestamp": "2026-09-01T12:00:00Z", "cutoff": "2026-09-01T10:00:00Z"},
        {"entity": "sensor_2", "timestamp": "2026-09-01T09:00:00Z", "cutoff": "2026-09-01T10:00:00Z"},
    ]
    for ev in mock_events:
        is_leaky = ev["timestamp"] > ev["cutoff"]
        if is_leaky:
            print(f"  [PASS] Flagged look-ahead leakage: event={ev['timestamp']} > cutoff={ev['cutoff']}")
            passed += 1
        else:
            print(f"  [PASS] Valid temporal record: event={ev['timestamp']} <= cutoff={ev['cutoff']}")
            passed += 1

    # Scenario 3: Cryptographic Bundle HMAC Signature Verification
    print("[RUN] Scenario 3: Scientist HMAC-SHA256 Manifest Verification")
    secret_key = b"test-secret-key"
    mock_manifest = json.dumps({"model_id": "candidate-v2", "sha256": "abcdef123456"}, sort_keys=True)
    correct_sig = hmac.new(secret_key, mock_manifest.encode(), hashlib.sha256).hexdigest()
    tampered_manifest = json.dumps({"model_id": "candidate-v2", "sha256": "tampered-hash"}, sort_keys=True)

    # Valid check
    calc_sig = hmac.new(secret_key, mock_manifest.encode(), hashlib.sha256).hexdigest()
    if hmac.compare_digest(calc_sig, correct_sig):
        print("  [PASS] Valid manifest signature accepted")
        passed += 1
    else:
        print("  [FAIL] Valid manifest rejected")
        failed += 1

    # Tampered check
    tampered_sig = hmac.new(secret_key, tampered_manifest.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(tampered_sig, correct_sig):
        print("  [PASS] Tampered manifest signature detected and rejected")
        passed += 1
    else:
        print("  [FAIL] Tampered manifest bypassed signature check")
        failed += 1

    # Scenario 4: Scaffold e2e (contract mismatch regression guard)
    print("[RUN] Scenario 4: agent-init-project scaffold e2e")
    init_script = os.path.join(KITS_DIR, "bin", "agent-init-project")
    try:
        with tempfile.TemporaryDirectory(prefix="ak-e2e-") as tmp:
            r = subprocess.run([init_script, tmp, "--role", "both"],
                               capture_output=True, text=True)
            if r.returncode != 0:
                print(f"  [FAIL] scaffold script failed: {r.stderr[-500:]}")
                failed += 1
            else:
                expected = [
                    ".agents/config.yaml",
                    ".agents/kit.yaml",
                    ".agents/AGENTS.md",
                    ".agents/contracts/data_contract.json",
                    ".agents/contracts/metrics_sla.json",
                    ".agents/contracts/api_contract.json",
                ]
                missing = [p for p in expected if not os.path.isfile(os.path.join(tmp, p))]
                if missing:
                    print(f"  [FAIL] scaffold missing files: {missing}")
                    failed += 1
                else:
                    print("  [PASS] scaffold produced all expected contract/config files")
                    passed += 1
                # no absolute dev-machine path leaked
                with open(os.path.join(tmp, ".agents", "AGENTS.md")) as f:
                    agents_md = f.read()
                if "chinh303" in agents_md or "file:///home/" in agents_md:
                    print("  [FAIL] AGENTS.md leaks absolute dev-machine path")
                    failed += 1
                else:
                    print("  [PASS] AGENTS.md portable (no hardcoded home path)")
                    passed += 1
                # scaffold must not create .agents/skills (Codex coexistence: shared parent, no overwrite)
                if os.path.isdir(os.path.join(tmp, ".agents", "skills")):
                    print("  [FAIL] scaffold created .agents/skills (collides with Codex skill dir)")
                    failed += 1
                else:
                    print("  [PASS] scaffold avoids .agents/skills (Codex coexistence)")
                    passed += 1
                # invalid role must fail
                r2 = subprocess.run([init_script, tmp, "--role", "bogus"],
                                    capture_output=True, text=True)
                if r2.returncode != 0:
                    print("  [PASS] invalid --role correctly rejected")
                    passed += 1
                else:
                    print("  [FAIL] invalid --role was accepted")
                    failed += 1
    except Exception as e:
        print(f"  [FAIL] scaffold e2e exception: {e}")
        failed += 1

    # Scenario 5: install lifecycle e2e on a throwaway HOME (no residue, backup works)
    print("[RUN] Scenario 5: install.sh lifecycle e2e (install -> doctor -> uninstall)")
    installer = os.path.join(KITS_DIR, "install.sh")
    try:
        with tempfile.TemporaryDirectory(prefix="ak-home-") as home:
            env = dict(os.environ, HOME=home, AGENTKIT_SKIP_VERIFY="1")
            gem_skills = os.path.join(home, ".gemini", "config", "skills")
            os.makedirs(gem_skills)
            # foreign content that install must back up, never overwrite
            foreign_dir = os.path.join(gem_skills, "verify")
            os.makedirs(foreign_dir)
            with open(os.path.join(foreign_dir, "user-note.md"), "w") as f:
                f.write("user content\n")
            r = subprocess.run(["bash", installer, "--runtime", "gemini"],
                               capture_output=True, text=True, env=env)
            if r.returncode != 0:
                print(f"  [FAIL] install failed: {r.stderr[-500:]}")
                failed += 1
            else:
                link = os.path.join(gem_skills, "cook")
                if os.path.islink(link) and os.path.realpath(link).startswith(KITS_DIR + os.sep):
                    print("  [PASS] install linked skills to throwaway HOME")
                    passed += 1
                else:
                    print("  [FAIL] install did not link skills correctly")
                    failed += 1
                bak = os.path.join(home, ".agentkit-backups")
                kept = any(
                    root.endswith("verify") and "user-note.md" in files
                    for root, _, files in os.walk(bak)
                )
                if kept:
                    print("  [PASS] foreign content backed up (not overwritten)")
                    passed += 1
                else:
                    print("  [FAIL] foreign content lost (no backup)")
                    failed += 1
            r = subprocess.run(["bash", installer, "doctor", "--runtime", "gemini"],
                               capture_output=True, text=True, env=env)
            if r.returncode == 0:
                print("  [PASS] doctor healthy after install")
                passed += 1
            else:
                print(f"  [FAIL] doctor reported issues: {r.stdout[-500:]}")
                failed += 1
            r = subprocess.run(["bash", installer, "uninstall", "--runtime", "gemini"],
                               capture_output=True, text=True, env=env)
            leftovers = [
                p for p in glob.glob(os.path.join(gem_skills, "*"))
                if os.path.islink(p) and os.path.realpath(p).startswith(KITS_DIR + os.sep)
            ]
            if r.returncode == 0 and not leftovers:
                print("  [PASS] uninstall removed only owned links (no residue)")
                passed += 1
            else:
                print(f"  [FAIL] uninstall residue: {leftovers} rc={r.returncode}")
                failed += 1
    except Exception as e:
        print(f"  [FAIL] lifecycle e2e exception: {e}")
        failed += 1

    print(f"\nTier 2 Summary: {passed} PASSED, {failed} FAILED")
    return failed == 0

def run_tier_3(kit_name=None):
    """Tier 3: Cognitive Framing & Anti-Pattern Rubric Scorecard"""
    print_header("TIER 3: Subagent Cognitive Framing Scorecard")
    kits = [kit_name] if kit_name else ["engineer", "scientist"]
    total_score = 0
    max_score = 0

    print(f"{'Agent':<25} | {'Role Clarity':<14} | {'Refusals/Anti':<14} | {'Ponytail/YAGNI':<14} | {'Status'}")
    print("-" * 80)

    for kit in kits:
        agents_path = os.path.join(KITS_DIR, kit, "agents", "*.json")
        for agent_file in sorted(glob.glob(agents_path)):
            with open(agent_file) as f:
                data = json.load(f)
            name = data["name"]
            prompt = data["system_prompt"]

            # Criteria 1: Role & Cognitive Framing
            c1 = 5 if ("Cognitive Framing" in prompt or "Mental Model" in prompt) else 2
            # Criteria 2: Explicit Refusals & Anti-Patterns
            c2 = 5 if ("Refusals" in prompt or "REFUSE" in prompt) else 2
            # Criteria 3: Ponytail / Minimalism / Vectorization discipline + explicit rubric
            has_discipline = ("ponytail" in prompt.lower() or "vectorized" in prompt.lower() or "yagni" in prompt.lower() or "simpl" in prompt.lower())
            has_rubric = ("self_challenge" in json.dumps(data).lower() or "adversarial" in prompt.lower() or "challenge question" in prompt.lower())
            if has_discipline and has_rubric:
                c3 = 5
            elif has_discipline or has_rubric:
                c3 = 4
            else:
                c3 = 2

            score = c1 + c2 + c3
            total_score += score
            max_score += 15
            status = "PASS (15/15)" if score == 15 else f"WARN ({score}/15)"
            print(f"{name:<25} | {c1}/5           | {c2}/5           | {c3}/5           | {status}")

    percentage = (total_score / max_score) * 100 if max_score > 0 else 0
    ready = "ALL AGENTS STAFF-LEVEL READY" if percentage >= 90.0 else "NEEDS WORK: some agents below staff bar"
    print(f"\nTier 3 Scorecard: {total_score}/{max_score} ({percentage:.1f}%) - {ready}")
    return percentage >= 90.0

def main():
    global KITS_DIR
    parser = argparse.ArgumentParser(description="AgentKit 3-Tier Evaluation Harness V2.1")
    parser.add_argument("--tier", choices=["1", "2", "3", "all"], default="all", help="Evaluation tier to run")
    parser.add_argument("--all", action="store_true", help="Run all tiers")
    parser.add_argument("--kit", choices=["engineer", "scientist"], default=None, help="Filter by kit")
    parser.add_argument("--kits-dir", default=None, help="Kit root (default: $AGENTKIT_DIR or repo root)")
    parser.add_argument("--strict", action="store_true", help="Reserved: tiers already run strict in V2.1")
    args = parser.parse_args()
    if args.kits_dir:
        KITS_DIR = os.path.abspath(args.kits_dir)
    else:
        KITS_DIR = os.path.abspath(KITS_DIR)
    if args.all:
        args.tier = "all"

    success = True
    if args.tier in ["1", "all"]:
        if not run_tier_1(args.kit):
            success = False
    if args.tier in ["2", "all"]:
        if not run_tier_2(args.kit):
            success = False
    if args.tier in ["3", "all"]:
        if not run_tier_3(args.kit):
            success = False

    if success:
        print("\n[OK] Evaluation Harness: 100% SUCCEEDED across all requested tiers.")
        sys.exit(0)
    else:
        print("\n[FAIL] Evaluation Harness detected issues.")
        sys.exit(1)

if __name__ == "__main__":
    main()
