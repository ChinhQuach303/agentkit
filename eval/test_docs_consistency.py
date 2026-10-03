import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from docs_consistency import markdown_link_errors, parse_manifest, validate_repo


class DocsConsistencyTests(unittest.TestCase):
    def test_repository_documents_match_current_sources(self):
        self.assertEqual(validate_repo(), [])

    def test_manifest_parser_reads_export_lists(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "kit.yaml"
            manifest.write_text(
                "name: sample\nversion: 1.2.3\nexports:\n  skills:\n    - scout\n  agents:\n    - reviewer\n",
                encoding="utf-8",
            )
            self.assertEqual(parse_manifest(manifest), (
                "1.2.3", {"skills": ["scout"], "agents": ["reviewer"]}
            ))

    def test_readme_count_drift_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for kit in ("engineer", "scientist"):
                (root / kit / "skills" / "scout").mkdir(parents=True)
                (root / kit / "skills" / "scout" / "SKILL.md").write_text("skill\n", encoding="utf-8")
                (root / kit / "agents").mkdir()
                (root / kit / "agents" / "reviewer.json").write_text("{}", encoding="utf-8")
                (root / kit / "hooks").mkdir()
                (root / kit / "hooks" / "hooks.json").write_text("{}", encoding="utf-8")
                (root / kit / "kit.yaml").write_text(
                    "name: " + kit + "\nversion: 1.0.0\nexports:\n  skills:\n    - scout\n  agents:\n    - reviewer\n  hooks:\n    - hooks.json\n",
                    encoding="utf-8",
                )
            (root / "install.sh").write_text(
                'GEMINI_DIR="${HOME}/.gemini/skills"\nANTIGRAVITY_DIR="${HOME}/.gemini/config/skills"\n',
                encoding="utf-8",
            )
            readme = (
                "engineer/kit.yaml # Manifest v1.0.0 (1 skill, 1 agent, hooks)\n"
                "scientist/kit.yaml # Manifest v1.0.0 (1 skill, 1 agent, hooks)\n"
                "~/.gemini/skills/ ~/.gemini/config/skills/\n"
            )
            (root / "README.md").write_text(readme, encoding="utf-8")
            self.assertEqual(validate_repo(root), [])
            (root / "README.md").write_text(readme.replace("1 skill", "2 skills", 1), encoding="utf-8")
            self.assertTrue(any("README engineer manifest summary" in error for error in validate_repo(root)))
            (root / "README.md").write_text(readme, encoding="utf-8")
            manifest = root / "engineer" / "kit.yaml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace("    - scout\n", "    - scout\n    - missing\n"),
                encoding="utf-8",
            )
            self.assertTrue(any("exports.skills differs from files" in error for error in validate_repo(root)))

    def test_broken_local_markdown_link_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("[missing](./not-here.md)\n", encoding="utf-8")
            errors = markdown_link_errors(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("broken local link", errors[0])


if __name__ == "__main__":
    unittest.main()
