import unittest
from app.parser import (
    extract_candidate_name,
    extract_skills,
    extract_education,
    extract_experience_years,
    extract_certifications,
    parse_job_description,
    parse_resume
)


class TestParser(unittest.TestCase):
    def test_extract_candidate_name(self):
        text = "Alex Dev\nEmail: alex@example.com\nSoftware Engineer"
        name = extract_candidate_name(text)
        self.assertIn("Alex", name)

    def test_extract_skills(self):
        text = "Experienced in Python, Java, SQL, Docker, and Machine Learning."
        skills = extract_skills(text)
        self.assertIn("python", skills)
        self.assertIn("java", skills)
        self.assertIn("sql", skills)
        self.assertIn("docker", skills)
        self.assertIn("machine learning", skills)

    def test_extract_education(self):
        text = "Holds a Master of Science (MSc) in Computer Science."
        edu = extract_education(text)
        self.assertEqual(edu["level"], "Master")

    def test_extract_experience_years(self):
        text = "Over 6+ years of professional software engineering experience."
        exp = extract_experience_years(text)
        self.assertEqual(exp, 6.0)

    def test_extract_certifications(self):
        text = "AWS Certified Solutions Architect and Certified Scrum Master."
        certs = extract_certifications(text)
        self.assertTrue(len(certs) >= 1)

    def test_parse_job_description(self):
        jd = "Looking for Senior Developer with Python, SQL, 5 years experience, Bachelor degree."
        parsed = parse_job_description(jd)
        self.assertIn("python", parsed["skills"])
        self.assertEqual(parsed["education"]["level"], "Bachelor")
        self.assertEqual(parsed["required_experience_years"], 5.0)


if __name__ == "__main__":
    unittest.main()
