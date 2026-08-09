"""
Comparison engine matching parsed candidate attributes against Job Description requirements.
Focuses on 3 major requirement categories:
1. REQUIRED SKILLS (EXACTLY 8 SKILLS)
2. EDUCATION REQUIREMENT (Bachelor's Degree)
3. EXPERIENCE REQUIREMENT (Minimum 2 Years)
"""
from app.utils import cosine_similarity

# Standard 8 Required Skills List
STANDARD_REQUIRED_SKILLS = [
    "python", "java", "sql", "machine learning",
    "data structures", "git", "rest api", "problem solving"
]

MIN_EXPERIENCE_YEARS = 2.0


def match_skills(candidate_skills: set, jd_skills: set) -> dict:
    """
    Compare candidate skills against required skills (Target: EXACTLY 8 Required Skills).
    """
    target_skills = set(jd_skills) if len(jd_skills) >= 3 else set(STANDARD_REQUIRED_SKILLS)
    if not jd_skills or len(jd_skills) < 3:
        target_skills = set(STANDARD_REQUIRED_SKILLS)

    matched = candidate_skills.intersection(target_skills)
    missing = target_skills.difference(candidate_skills)
    extra = candidate_skills.difference(target_skills)
    
    matched_count = len(matched)
    total_required = len(target_skills)
    match_ratio = matched_count / total_required if total_required > 0 else 0.0
    
    return {
        "matched_skills": sorted(list(matched)),
        "missing_skills": sorted(list(missing)),
        "extra_skills": sorted(list(extra)),
        "matched_count": matched_count,
        "total_required": total_required,
        "match_ratio": min(1.0, match_ratio)
    }


def match_education(candidate_edu: dict, jd_edu: dict = None) -> dict:
    """
    Compare candidate education against standard Bachelor's Degree requirement.
    """
    cand_level = candidate_edu.get("level", "High School / None")
    valid_degrees = ["Bachelor", "Master", "Doctorate"]
    
    if cand_level in valid_degrees:
        match_score = 1.0
        status = "✓ Relevant"
    elif cand_level == "Associate":
        match_score = 0.4
        status = "Not Relevant"
    elif cand_level == "High School / None" and candidate_edu.get("matched_keywords"):
        match_score = 0.2
        status = "Not Relevant"
    else:
        match_score = 0.0
        status = "Not Specified"
        
    return {
        "candidate_level": cand_level,
        "required_level": "Bachelor's Degree",
        "match_score": match_score,
        "status": status
    }


def match_experience(candidate_exp: float, jd_exp: float = 2.0) -> dict:
    """
    Compare candidate experience years against standard 2 years requirement.
    """
    required = jd_exp if (jd_exp and jd_exp > 0) else 2.0
    
    if candidate_exp >= required:
        match_score = 1.0
        status = "✓ Meets Requirement"
    elif candidate_exp > 0.0:
        match_score = candidate_exp / required
        status = "Below Requirement"
    else:
        match_score = 0.0
        status = "Not Specified"
        
    return {
        "candidate_years": candidate_exp,
        "required_years": required,
        "match_score": min(1.0, match_score),
        "status": status
    }


def match_certifications(candidate_certs: list, jd_certs: list = None) -> dict:
    """
    Compare candidate certifications.
    """
    if not candidate_certs:
        return {"match_score": 0.5, "status": "No certifications listed"}
    return {"match_score": 1.0, "status": f"Found {len(candidate_certs)} certification(s)"}


def calculate_keyword_overlap(text1: str, text2: str) -> dict:
    """
    Calculate keyword overlap between two raw strings.
    """
    sim = cosine_similarity(text1, text2)
    return {
        "similarity_score": sim,
        "match_score": sim
    }


def match_keywords(candidate_keywords: set, jd_keywords: set) -> dict:
    """
    Calculate keyword vector overlap using set intersection ratio.
    """
    if not jd_keywords or not candidate_keywords:
        return {"match_score": 0.5, "similarity": 0.5}
        
    overlap = candidate_keywords.intersection(jd_keywords)
    sim = min(1.0, len(overlap) / max(1, len(jd_keywords)))
    return {
        "match_score": sim,
        "similarity": round(sim, 3)
    }


def compare_resume_with_jd(candidate_info: dict, parsed_jd: dict) -> dict:
    """
    Full comparison engine between parsed candidate profile and Job Description requirements.
    """
    skill_res = match_skills(candidate_info["skills"], parsed_jd["skills"])
    edu_res = match_education(candidate_info["education"], parsed_jd["education"])
    exp_res = match_experience(candidate_info["experience_years"], parsed_jd.get("required_experience_years", 2.0))
    cert_res = match_certifications(candidate_info["certifications"], parsed_jd["certifications"])
    kw_res = match_keywords(candidate_info["keywords"], parsed_jd["keywords"])
    
    return {
        "candidate_id": candidate_info["candidate_id"],
        "candidate_name": candidate_info["name"],
        "skill_match": skill_res,
        "education_match": edu_res,
        "experience_match": exp_res,
        "certification_match": cert_res,
        "keyword_match": kw_res
    }
