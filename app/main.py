"""
Command Line Interface (CLI) for running Intelligent Resume Analyzer directly in terminal.
"""
import sys
import json
import os
from app.analyzer import ResumeAnalyzer


def print_banner():
    print("=" * 70)
    print("        INTELLIGENT RESUME ANALYZER (100% Rule-Based Stdlib)")
    print("=" * 70)


def run_cli():
    print_banner()

    sample_jd_path = os.path.join("data", "sample_jd", "software_engineer.txt")
    sample_resumes_dir = os.path.join("data", "sample_resumes")

    if not os.path.exists(sample_jd_path):
        print(f"Error: Sample Job Description not found at {sample_jd_path}")
        print("Please run from the project root directory.")
        return

    # Load sample JD
    with open(sample_jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    # Load sample resumes
    resumes = []
    if os.path.exists(sample_resumes_dir):
        for filename in sorted(os.listdir(sample_resumes_dir)):
            if filename.endswith(".txt"):
                filepath = os.path.join(sample_resumes_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    resumes.append({
                        "name": filename.replace(".txt", "").replace("_", " ").title(),
                        "text": content
                    })

    if not resumes:
        print("No sample resumes found.")
        return

    print(f"\nAnalyzing {len(resumes)} candidate resumes against Job Description: Senior Software Engineer...\n")

    analyzer = ResumeAnalyzer()
    results = analyzer.analyze(jd_text, resumes)

    if not results.get("success"):
        print(f"Analysis Error: {results.get('error')}")
        return

    print("-" * 70)
    print(f"{'RANK':<6} | {'CANDIDATE NAME':<25} | {'SCORE':<8} | {'RECOMMENDATION':<18}")
    print("-" * 70)

    for candidate in results["rankings"]:
        rank = candidate.get("rank", "-")
        name = candidate.get("name", "Unknown")[:25]
        score = f"{candidate.get('total_score', 0.0)}%"
        rec = candidate.get("recommendation", "Low Match")
        print(f"{rank:<6} | {name:<25} | {score:<8} | {rec:<18}")

    print("-" * 70)

    # Print Top Candidate Detailed Explanation
    if results["rankings"]:
        top = results["rankings"][0]
        print(f"\n TOP CANDIDATE DETAILS: {top['name']} ({top['total_score']}%)")
        print(f" Recommendation: {top['recommendation']}")
        print(f"\n Score Breakdown:")
        bd = top['breakdown']
        print(f"   - Skill Match:        {bd['skill_match']['score']}/{bd['skill_match']['max_score']} pts")
        print(f"   - Education Match:    {bd['education_match']['score']}/{bd['education_match']['max_score']} pts")
        print(f"   - Experience Match:   {bd['experience_match']['score']}/{bd['experience_match']['max_score']} pts")
        print(f"   - Keyword Overlap:    {bd['keyword_match']['score']}/{bd['keyword_match']['max_score']} pts")
        print(f"   - Certifications:     {bd['certification_match']['score']}/{bd['certification_match']['max_score']} pts")
        print(f"\n Matched Skills: {', '.join(top['comparison']['skill_match']['matched_skills']) or 'None'}")
        print(f" Missing Skills: {', '.join(top['comparison']['skill_match']['missing_skills']) or 'None'}")
        print(f"\n Explanation Summary:\n   {top['explanation']['summary']}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    run_cli()
