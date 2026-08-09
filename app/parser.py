"""
Resume and Job Description parser implemented using standard Python standard library.
Extracts Candidate Info, Skills, Education, Experience, Certifications, and Keywords.
"""
import re
from app.utils import normalize_text, tokenize, remove_stopwords, extract_ngrams

# Comprehensive Taxonomy of Skills for Matching (categorized)
SKILL_TAXONOMY = {
    "Programming Languages": [
        "python", "javascript", "typescript", "java", "c++", "c#", "c", "go", "golang",
        "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "perl", "dart", "html",
        "html5", "css", "css3", "sql", "bash", "shell", "powershell", "assembly"
    ],
    "Frameworks & Libraries": [
        "react", "react.js", "reactjs", "angular", "vue", "vue.js", "next.js", "nextjs",
        "node.js", "nodejs", "express", "express.js", "django", "flask", "fastapi",
        "spring", "spring boot", "asp.net", ".net", "laravel", "rails", "ruby on rails",
        "flutter", "react native", "tensorflow", "pytorch", "scikit-learn", "pandas",
        "numpy", "keras", "opencv", "bootstrap", "tailwind", "jquery"
    ],
    "Databases & Storage": [
        "sql", "mysql", "postgresql", "postgres", "mongodb", "sqlite", "oracle",
        "redis", "elasticsearch", "dynamodb", "cassandra", "neo4j", "mariadb",
        "firebase", "snowflake", "bigquery"
    ],
    "Cloud & DevOps": [
        "aws", "amazon web services", "azure", "microsoft azure", "gcp",
        "google cloud", "google cloud platform", "docker", "kubernetes", "k8s",
        "jenkins", "gitlab", "github actions", "terraform", "ansible", "ci/cd",
        "cicd", "linux", "unix", "nginx", "apache", "prometheus", "grafana"
    ],
    "Data Science & AI": [
        "machine learning", "deep learning", "artificial intelligence", "data analysis",
        "data science", "nlp", "natural language processing", "computer vision",
        "data engineering", "etl", "data mining", "statistical modeling", "neural networks",
        "tableau", "power bi"
    ],
    "Software Engineering": [
        "rest api", "restful api", "graphql", "microservices", "system design",
        "object oriented programming", "oop", "functional programming", "agile",
        "scrum", "git", "github", "bitbucket", "jira", "unit testing", "tdd",
        "clean code", "code review", "design patterns", "software architecture"
    ],
    "Soft Skills & Management": [
        "leadership", "communication", "problem solving", "teamwork", "collaboration",
        "project management", "time management", "critical thinking", "analytical skills",
        "mentorship", "stakeholder management"
    ]
}

# Flat skill list for fast lookup
ALL_TAXONOMY_SKILLS = set()
for category, skills in SKILL_TAXONOMY.items():
    for s in skills:
        ALL_TAXONOMY_SKILLS.add(s.lower())

# Education Level Taxonomy
EDUCATION_KEYWORDS = {
    "Doctorate": ["phd", "ph.d", "doctorate", "doctor of philosophy"],
    "Master": ["master", "masters", "msc", "m.sc", "m.s", "ms", "mtech", "m.tech", "mba"],
    "Bachelor": ["bachelor", "bachelors", "bsc", "b.sc", "b.s", "bs", "btech", "b.tech", "be", "b.e", "bca", "b.com", "bba"],
    "Associate": ["associate", "associates", "diploma"]
}

# Common Certification Keywords
CERTIFICATION_KEYWORDS = [
    "certified", "certification", "certificate", "aws certified", "azure certified",
    "pmp", "scrum master", "csm", "cisco", "ccna", "ccnp", "cissp", "ckad", "cka",
    "gcp certified", "oracle certified", "comptia"
]


def extract_candidate_name(text: str) -> str:
    """Extract candidate name using heuristic rules from the first lines of resume."""
    if not text:
        return "Unknown Candidate"
        
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines:
        return "Unknown Candidate"
        
    invalid_name_words = {
        'resume', 'curriculum', 'vitae', 'cv', 'contact', 'email', 'phone',
        'address', 'experience', 'education', 'skills', 'summary', 'profile',
        'objective', 'work', 'projects', 'job', 'description'
    }
    
    for line in lines[:5]:
        # Clean line
        clean_l = re.sub(r'[^a-zA-Z\s\.\-]', '', line).strip()
        words = clean_l.split()
        
        # Candidate name usually has 2-4 words, capitalized, no header words
        if 2 <= len(words) <= 4:
            if not any(w.lower() in invalid_name_words for w in words):
                # Ensure words look like real names (capitalized or alpha)
                if all(w[0].isupper() or len(w) > 1 for w in words if len(w) > 0):
                    return " ".join(words)
                    
    # Fallback to line 1 first two words if alpha
    first_words = re.sub(r'[^a-zA-Z\s]', '', lines[0]).strip().split()
    if first_words:
        return " ".join(first_words[:3]).title()
        
    return "Candidate"


def extract_skills(text: str) -> set:
    """
    Extract skills present in text by matching single-word and multi-word skills
    against the taxonomy as well as dynamically identifying technical tokens.
    """
    if not text:
        return set()
        
    norm_text = normalize_text(text)
    tokens = tokenize(norm_text)
    
    # Extract unigrams, bigrams, trigrams
    ngrams = set(extract_ngrams(tokens, 1, 3))
    
    found_skills = set()
    
    # Match against taxonomy
    for skill in ALL_TAXONOMY_SKILLS:
        # Match whole phrase/word
        if skill in ngrams or re.search(r'\b' + re.escape(skill) + r'\b', norm_text):
            found_skills.add(skill.lower())
            
    return found_skills


def extract_education(text: str) -> dict:
    """Extract education level and details from text."""
    if not text:
        return {"level": "None", "details": []}
        
    norm_text = normalize_text(text)
    found_levels = []
    found_details = []
    
    for level, keywords in EDUCATION_KEYWORDS.items():
        for kw in keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, norm_text):
                if level not in found_levels:
                    found_levels.append(level)
                found_details.append(kw)
                
    # Highest degree mapping
    level_hierarchy = ["Doctorate", "Master", "Bachelor", "Associate"]
    highest_level = "High School / None"
    for h in level_hierarchy:
        if h in found_levels:
            highest_level = h
            break
            
    return {
        "level": highest_level,
        "matched_keywords": list(set(found_details))
    }


def extract_experience_years(text: str) -> float:
    """
    Extract total numeric years of experience mentioned in text.
    Handles '5+ years', '3 to 5 yrs', '2018 - 2023', etc.
    """
    if not text:
        return 0.0
        
    norm_text = normalize_text(text)
    years = []
    
    # Pattern 1: "5+ years", "3-5 years", "4 yrs"
    pattern_yrs = r'(\d+(?:\.\d+)?)\s*(?:\+|to|-)?\s*(?:\d+(?:\.\d+)?)?\s*(?:years?|yrs?|yr\b)'
    matches = re.findall(pattern_yrs, norm_text)
    for m in matches:
        try:
            years.append(float(m))
        except ValueError:
            pass
            
    # Pattern 2: Year ranges like 2018 - 2024 or 2020 to present
    current_year = 2026
    pattern_range = r'\b(20\d{2}|19\d{2})\s*(?:-|to)\s*(20\d{2}|19\d{2}|present|current)\b'
    range_matches = re.findall(pattern_range, norm_text)
    for start, end in range_matches:
        try:
            start_yr = int(start)
            end_yr = current_year if end in ['present', 'current'] else int(end)
            diff = max(0, end_yr - start_yr)
            if 0 < diff <= 40:
                years.append(float(diff))
        except ValueError:
            pass
            
    if not years:
        return 0.0
        
    # Return maximum plausible experience found
    return max(years)


def extract_certifications(text: str) -> list:
    """Extract certification names or matches in text."""
    if not text:
        return []
        
    norm_text = normalize_text(text)
    found_certs = []
    
    for cert_kw in CERTIFICATION_KEYWORDS:
        pattern = r'\b' + re.escape(cert_kw) + r'\b'
        if re.search(pattern, norm_text):
            found_certs.append(cert_kw.title())
            
    # Also look for lines containing "Certification" or "Certified"
    lines = text.split('\n')
    for line in lines:
        clean_l = line.strip()
        if re.search(r'\b(?:certified|certification|certificate)\b', clean_l, re.IGNORECASE):
            if len(clean_l) < 80 and clean_l not in found_certs:
                found_certs.append(clean_l)
                
    # Deduplicate
    unique_certs = list(dict.fromkeys(found_certs))
    return unique_certs[:5]


def parse_job_description(jd_text: str) -> dict:
    """
    Parse a Job Description string and extract structured requirements.
    """
    norm_jd = normalize_text(jd_text)
    skills = extract_skills(norm_jd)
    education = extract_education(norm_jd)
    exp_years = extract_experience_years(norm_jd)
    certifications = extract_certifications(norm_jd)
    
    # Extract key domain terms (tokens excluding stop words)
    tokens = remove_stopwords(tokenize(norm_jd))
    keywords = set(tokens)
    
    return {
        "raw_text": jd_text,
        "skills": skills,
        "education": education,
        "required_experience_years": exp_years,
        "certifications": certifications,
        "keywords": keywords
    }


def parse_resume(resume_text: str, candidate_id: int = 1) -> dict:
    """
    Parse a candidate resume string and extract structured candidate profile.
    """
    name = extract_candidate_name(resume_text)
    if name == "Candidate" or name == "Unknown Candidate":
        name = f"Candidate {candidate_id}"
        
    norm_resume = normalize_text(resume_text)
    skills = extract_skills(norm_resume)
    education = extract_education(norm_resume)
    exp_years = extract_experience_years(norm_resume)
    certifications = extract_certifications(norm_resume)
    
    tokens = remove_stopwords(tokenize(norm_resume))
    keywords = set(tokens)
    
    return {
        "candidate_id": candidate_id,
        "name": name,
        "raw_text": resume_text,
        "skills": skills,
        "education": education,
        "experience_years": exp_years,
        "certifications": certifications,
        "keywords": keywords
    }
