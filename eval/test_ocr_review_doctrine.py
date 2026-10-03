import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evaluator import ocr_review_doctrine_issues

REVIEW_SKILL = Path(__file__).resolve().parent.parent / "engineer/skills/review/SKILL.md"


class OcrReviewDoctrineTests(unittest.TestCase):
    def test_review_skill_keeps_ocr_opt_in_and_non_blocking(self):
        self.assertEqual(ocr_review_doctrine_issues(REVIEW_SKILL.read_text(encoding="utf-8")), [])

    def test_missing_consent_or_fallback_rule_is_rejected(self):
        content = REVIEW_SKILL.read_text(encoding="utf-8")
        content = content.replace("explicit per-review approval", "automatic review")
        content = content.replace("never a review failure", "review blocker")
        issues = ocr_review_doctrine_issues(content)
        self.assertIn("per-review consent", issues)
        self.assertIn("non-blocking fallback", issues)


if __name__ == "__main__":
    unittest.main()
