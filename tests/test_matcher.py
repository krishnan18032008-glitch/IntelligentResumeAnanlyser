import unittest
from app.matcher import (
    match_skills,
    match_education,
    match_experience,
    match_certifications,
    calculate_keyword_overlap
)


class TestMatcher(unittest.TestCase):
    def test_match_skills(self):
        cand_skills = {"python", "java", "sql", "docker"}
        jd_skills = {"python", "sql", "docker", "aws"}
        res = match_skills(cand_skills, jd_skills)
        self.assertEqual(res["matched_skills"], ["docker", "python", "sql"])
        self.assertEqual(res["missing_skills"], ["aws"])
        self.assertEqual(res["match_ratio"], 0.75)

    def test_match_education(self):
        cand_edu = {"level": "Master"}
        jd_edu = {"level": "Bachelor"}
        res = match_education(cand_edu, jd_edu)
        self.assertEqual(res["match_score"], 1.0)
        self.assertTrue("Relevant" in res["status"] or "Qualified" in res["status"])

    def test_match_experience(self):
        res = match_experience(candidate_exp=6.0, jd_exp=5.0)
        self.assertEqual(res["match_score"], 1.0)

        res_under = match_experience(candidate_exp=2.0, jd_exp=5.0)
        self.assertLess(res_under["match_score"], 1.0)

    def test_keyword_overlap(self):
        text1 = "Python developer with experience in SQL databases and cloud API."
        text2 = "Looking for Python developer proficient in SQL databases."
        overlap = calculate_keyword_overlap(text1, text2)
        self.assertGreater(overlap["similarity_score"], 0.0)


if __name__ == "__main__":
    unittest.main()
