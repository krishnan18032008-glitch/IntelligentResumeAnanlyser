"""
Main orchestrator for Intelligent Resume Analysis system.
Handles input validation, parsing, matching, scoring, dynamic ranking, and report generation.
"""
from app.parser import parse_job_description, parse_resume
from app.matcher import compare_resume_with_jd
from app.scorer import calculate_score


class ResumeAnalyzer:
    def __init__(self, custom_weights: dict = None):
        self.custom_weights = custom_weights

    def analyze(self, jd_text: str, resumes: list) -> dict:
        """
        Analyze a Job Description against multiple candidate resumes.

        :param jd_text: Raw string content of Job Description.
        :param resumes: List of dicts [{"name": optional, "text": resume_string}] or strings.
        :return: Structured analysis result with JD info, candidate scores, ranking, and explainability.
        """
        # 1. Input Validation
        if not jd_text or not jd_text.strip():
            return {
                "success": False,
                "error": "Job Description cannot be empty. Please provide a valid Job Description.",
                "rankings": []
            }

        if not resumes or len(resumes) == 0:
            return {
                "success": False,
                "error": "No resumes provided. Please add at least one candidate resume for analysis.",
                "rankings": []
            }

        # 2. Parse Job Description
        parsed_jd = parse_job_description(jd_text)

        processed_candidates = []

        # 3. Process & Compare Each Candidate Resume
        for index, item in enumerate(resumes, start=1):
            if isinstance(item, dict):
                r_text = item.get("text", "")
                r_name = item.get("name", None)
            else:
                r_text = str(item)
                r_name = None

            if not r_text or not r_text.strip():
                # Handle empty resume input gracefully
                candidate_data = {
                    "candidate_id": index,
                    "name": r_name or f"Candidate {index} (Empty)",
                    "match_score": 0.0,
                    "recommendation": "Low Match",
                    "error": "Empty resume content provided.",
                    "details": None
                }
                processed_candidates.append(candidate_data)
                continue

            # Parse candidate resume
            candidate_info = parse_resume(r_text, candidate_id=index)
            if r_name and r_name.strip():
                candidate_info["name"] = r_name.strip()

            # Compare candidate resume with JD
            comparison = compare_resume_with_jd(candidate_info, parsed_jd)

            # Calculate weighted score & explanation
            score_res = calculate_score(comparison, self.custom_weights)

            processed_candidates.append({
                "candidate_id": candidate_info["candidate_id"],
                "name": candidate_info["name"],
                "total_score": score_res["total_score"],
                "recommendation": score_res["recommendation"],
                "comparison": comparison,
                "breakdown": score_res["breakdown"],
                "explanation": score_res["explanation"],
                "candidate_info": {
                    "skills": sorted(list(candidate_info["skills"])),
                    "education": candidate_info["education"],
                    "experience_years": candidate_info["experience_years"],
                    "certifications": candidate_info["certifications"]
                }
            })

        # 4. Rank Candidates Descending by Total Score
        ranked_candidates = sorted(
            processed_candidates,
            key=lambda c: c.get("total_score", 0.0),
            reverse=True
        )

        # Assign Rank Ordinals
        for rank_idx, cand in enumerate(ranked_candidates, start=1):
            cand["rank"] = rank_idx

        return {
            "success": True,
            "total_candidates": len(ranked_candidates),
            "job_description_summary": {
                "extracted_skills": sorted(list(parsed_jd["skills"])),
                "required_education": parsed_jd["education"]["level"],
                "required_experience_years": parsed_jd["required_experience_years"],
                "certifications": parsed_jd["certifications"]
            },
            "rankings": ranked_candidates
        }
