"""
Scoring and explainability engine calculating weighted match scores and detailed dynamic explanations.
"""

DEFAULT_WEIGHTS = {
    "skill": 40.0,
    "education": 20.0,
    "experience": 20.0,
    "keyword": 10.0,
    "certification": 10.0
}


def get_recommendation(total_score: float) -> str:
    """Generate human-readable match recommendation tier based on calculated score."""
    if total_score >= 90.0:
        return "Excellent Match"
    elif total_score >= 75.0:
        return "Strong Match"
    elif total_score >= 60.0:
        return "Moderate Match"
    else:
        return "Low Match"


def calculate_score(comparison: dict, custom_weights: dict = None) -> dict:
    """
    Calculate weighted match score and itemized breakdown from comparison results.
    """
    weights = DEFAULT_WEIGHTS.copy()
    if custom_weights:
        weights.update(custom_weights)
        
    # Ensure total weights sum up properly
    total_weight = sum(weights.values())
    if total_weight > 0 and total_weight != 100.0:
        # Normalize weights to 100%
        weights = {k: (v / total_weight) * 100.0 for k, v in weights.items()}

    # Individual category match ratios (0.0 to 1.0)
    skill_ratio = comparison["skill_match"]["match_ratio"]
    edu_ratio = comparison["education_match"]["match_score"]
    exp_ratio = comparison["experience_match"]["match_score"]
    cert_ratio = comparison["certification_match"]["match_score"]
    kw_ratio = comparison["keyword_match"]["match_score"]

    # Calculate itemized score points
    skill_pts = round(skill_ratio * weights["skill"], 1)
    edu_pts = round(edu_ratio * weights["education"], 1)
    exp_pts = round(exp_ratio * weights["experience"], 1)
    cert_pts = round(cert_ratio * weights["certification"], 1)
    kw_pts = round(kw_ratio * weights["keyword"], 1)

    total_score = round(skill_pts + edu_pts + exp_pts + cert_pts + kw_pts, 1)
    total_score = min(100.0, max(0.0, total_score))

    recommendation = get_recommendation(total_score)

    breakdown = {
        "skill_match": {
            "score": skill_pts,
            "max_score": round(weights["skill"], 1),
            "ratio": round(skill_ratio, 2)
        },
        "education_match": {
            "score": edu_pts,
            "max_score": round(weights["education"], 1),
            "ratio": round(edu_ratio, 2)
        },
        "experience_match": {
            "score": exp_pts,
            "max_score": round(weights["experience"], 1),
            "ratio": round(exp_ratio, 2)
        },
        "keyword_match": {
            "score": kw_pts,
            "max_score": round(weights["keyword"], 1),
            "ratio": round(kw_ratio, 2)
        },
        "certification_match": {
            "score": cert_pts,
            "max_score": round(weights["certification"], 1),
            "ratio": round(cert_ratio, 2)
        },
        "total_score": total_score,
        "max_total": 100.0
    }

    explanation = generate_explanation(comparison, breakdown, recommendation)

    return {
        "total_score": total_score,
        "recommendation": recommendation,
        "breakdown": breakdown,
        "explanation": explanation
    }


def generate_explanation(comparison: dict, breakdown: dict, recommendation: str) -> dict:
    """
    Generate dynamic human-readable explainability report explaining why the candidate received the score.
    """
    skills = comparison["skill_match"]
    edu = comparison["education_match"]
    exp = comparison["experience_match"]
    certs = comparison["certification_match"]

    summary_bullets = []

    # Skill explanation
    matched_cnt = len(skills["matched_skills"])
    total_req_cnt = matched_cnt + len(skills["missing_skills"])
    if total_req_cnt > 0:
        summary_bullets.append(
            f"Matched {matched_cnt} of {total_req_cnt} required skills "
            f"({breakdown['skill_match']['score']}/{breakdown['skill_match']['max_score']} pts)."
        )
        if skills["missing_skills"]:
            summary_bullets.append(
                f"Missing critical required skills: {', '.join([s.title() for s in skills['missing_skills'][:5]])}."
            )
    else:
        summary_bullets.append("Skill requirements met based on parsed resume technical terms.")

    # Education explanation
    summary_bullets.append(
        f"Education: {edu['candidate_level']} degree ({edu['status']}, "
        f"{breakdown['education_match']['score']}/{breakdown['education_match']['max_score']} pts)."
    )

    # Experience explanation
    summary_bullets.append(
        f"Experience: {exp['candidate_years']:g} years detected ({exp['status']}, "
        f"{breakdown['experience_match']['score']}/{breakdown['experience_match']['max_score']} pts)."
    )

    # Certification explanation
    cand_certs = certs.get("candidate_certs", [])
    if cand_certs:
        summary_bullets.append(
            f"Certifications: Found {len(cand_certs)} certification(s) "
            f"({breakdown['certification_match']['score']}/{breakdown['certification_match']['max_score']} pts)."
        )
    else:
        summary_bullets.append(
            f"Certifications: No explicit certifications detected "
            f"({breakdown['certification_match']['score']}/{breakdown['certification_match']['max_score']} pts)."
        )

    text_summary = f"Candidate scored {breakdown['total_score']}% and is evaluated as '{recommendation}'. " + " ".join(summary_bullets)

    return {
        "summary": text_summary,
        "bullets": summary_bullets
    }
