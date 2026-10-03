import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_outcome import grade_artifact, load_cases


class SkillOutcomeTests(unittest.TestCase):
    def test_corpus_has_unique_skills_and_valid_assertions(self):
        cases = load_cases()
        self.assertEqual(len(cases), 4)
        self.assertEqual(len({case["id"] for case in cases}), len(cases))

    def test_case_fixtures_pass_and_empty_outputs_fail(self):
        fixtures = {
            "engineer-review-idor": "BLOCK: owner authorization missing at src/invoices.ts:42.",
            "engineer-verify-red-tests": "pytest -q tests/test_auth.py: 2 failed, 8 passed. Verification failed; not verified.",
            "scientist-audit-temporal-leakage": "FAIL: customer_age_rollup was materialized post-cutoff.",
            "scientist-promotion-missing-signature": "NO-GO: missing signature; promotion is blocked.",
        }
        for case in load_cases():
            with self.subTest(case=case["id"]):
                self.assertTrue(all(check["passed"] for check in grade_artifact(case, fixtures[case["id"]])))
                self.assertFalse(all(check["passed"] for check in grade_artifact(case, "")))

    def test_no_go_phrase_is_not_mistaken_for_approval(self):
        case = next(case for case in load_cases() if case["id"] == "scientist-promotion-missing-signature")
        output = "NO-GO for promotion: missing signature; promotion is blocked."
        self.assertTrue(all(check["passed"] for check in grade_artifact(case, output)))

    def test_forbidden_claim_fails(self):
        case = next(case for case in load_cases() if case["id"] == "scientist-promotion-missing-signature")
        output = "NO-GO: missing signature; promotion is blocked. Approved for production."
        failed = [check["id"] for check in grade_artifact(case, output) if not check["passed"]]
        self.assertEqual(failed, ["claims-go"])


if __name__ == "__main__":
    unittest.main()
