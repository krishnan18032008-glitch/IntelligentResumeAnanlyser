import unittest
from app.scorer import calculate_score, get_recommendation


class TestScorer(unittest.TestCase):
    def test_recommendation_tiers(self):
        self.assertEqual(get_recommendation(95.0), "Excellent Match")
        self.assertEqual(get_recommendation(82.0), "Strong Match")
        self.assertEqual(get_recommendation(68.0), "Moderate Match")
        self.assertEqual(get_recommendation(45.0), "Low Match")

    def test_calculate_score(self):
        comparison = {
            "skill_match": {"match_ratio": 1.0, "matched_skills": ["python"], "missing_skills": []},
            "education_match": {"match_score": 1.0, "candidate_level": "Master", "status": "Fully Qualified"},
            "experience_match": {"match_score": 1.0, "candidate_years": 6.0, "status": "Fully Qualified"},
            "certification_match": {"match_score": 1.0, "candidate_certs": ["AWS"]},
            "keyword_match": {"match_score": 1.0, "similarity_score": 0.8}
        }
        score_res = calculate_score(comparison)
        self.assertEqual(score_res["total_score"], 100.0)
        self.assertEqual(score_res["recommendation"], "Excellent Match")
        self.assertIn("summary", score_res["explanation"])


if __name__ == "__main__":
    unittest.main()
