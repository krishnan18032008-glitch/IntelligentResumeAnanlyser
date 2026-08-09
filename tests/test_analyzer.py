import unittest
from app.analyzer import ResumeAnalyzer


class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = ResumeAnalyzer()
        self.jd = "Job Title: Software Engineer\nRequired Skills: Python, SQL, Java, Docker\nEducation: Bachelor\nExperience: 5 years"
        self.resumes = [
            {"name": "Strong Cand", "text": "Senior Dev with 6 years experience. Skills: Python, SQL, Java, Docker. Master degree."},
            {"name": "Weak Cand", "text": "Junior Dev with 1 year experience. Skills: HTML, CSS. Associate degree."}
        ]

    def test_empty_jd_validation(self):
        res = self.analyzer.analyze("", self.resumes)
        self.assertFalse(res["success"])
        self.assertIn("Job Description cannot be empty", res["error"])

    def test_empty_resumes_validation(self):
        res = self.analyzer.analyze(self.jd, [])
        self.assertFalse(res["success"])
        self.assertIn("No resumes provided", res["error"])

    def test_end_to_end_ranking(self):
        res = self.analyzer.analyze(self.jd, self.resumes)
        self.assertTrue(res["success"])
        self.assertEqual(len(res["rankings"]), 2)
        
        # Rank 1 should be Strong Cand
        top = res["rankings"][0]
        self.assertEqual(top["name"], "Strong Cand")
        self.assertEqual(top["rank"], 1)
        self.assertGreater(top["total_score"], res["rankings"][1]["total_score"])


if __name__ == "__main__":
    unittest.main()
