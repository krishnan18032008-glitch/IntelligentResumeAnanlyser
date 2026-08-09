# Intelligent Resume Analyzer 🚀

> **A 100% Rule-Based, Transparent, and Explainable Candidate Resume Screening System Built Entirely with Standard Library Python & Native Web APIs (Zero External Dependencies).**

---

## 📌 Problem Statement

Organizations receive hundreds of candidate resumes for open positions. Manually evaluating each resume against a Job Description (JD) is labor-intensive, time-consuming, and susceptible to human oversight.

Existing commercial resume screening platforms are often costly, rely on third-party cloud AI APIs, lack scoring transparency, and compromise candidate privacy by requiring internet connectivity.

The **Intelligent Resume Analyzer** solves this problem by providing a fast, reliable, explainable, and 100% offline candidate resume matching system that runs locally with **zero external packages or libraries**.

---

## 🔒 Strict Rule Compliance Audit

This repository strictly complies with all official constraints:

- ✅ **No External Packages or Libraries:** Built strictly using Python's standard library (`re`, `math`, `json`, `http.server`, `unittest`) and standard browser ES6 APIs.
- ✅ **No External AI APIs or Cloud Models:** Zero dependency on OpenAI, Gemini, Claude, Hugging Face, spaCy, NLTK, or scikit-learn.
- ✅ **100% Offline Local Operation:** Completely self-contained; requires no internet connection.
- ✅ **Explainable Rule-Based Logic:** Scores are computed dynamically from actual matching algorithms—never hard-coded or random.
- ✅ **Full Source Code & Test Suite:** Contains complete application logic, CLI runner, web server, frontend dashboard, sample data, and unit tests.

---

## 🏗️ System Architecture & Workflow

```
                     +-----------------------+
                     |    Job Description    |
                     +-----------+-----------+
                                 |
                                 v
                     +-----------------------+
                     |  Requirement Parser   |
                     |  (Skills, Edu, Exp)   |
                     +-----------+-----------+
                                 |
     +---------------------------+---------------------------+
     |                           |                           |
     v                           v                           v
+----+----+                 +----+----+                 +----+----+
| Resume 1|                 | Resume 2|                 | Resume N|
+----+----+                 +----+----+                 +----+----+
     |                           |                           |
     v                           v                           v
+----+---------------------------+---------------------------+----+
|                     Text Normalizer & Tokenizer                  |
|                (N-gram Extractor & TF-IDF Vectorizer)            |
+--------------------------------+--------------------------------+
                                 |
                                 v
+--------------------------------+--------------------------------+
|                        Comparison Engine                        |
|   - Technical Skill Alignment (Matched vs Missing)              |
|   - Education Qualification Hierarchy                           |
|   - Experience Years Differential                               |
|   - Certification Relevance                                     |
|   - Term Frequency Cosine Similarity                            |
+--------------------------------+--------------------------------+
                                 |
                                 v
+--------------------------------+--------------------------------+
|                     Weighted Scoring Engine                     |
| Skill (40%) + Education (20%) + Exp (20%) + KW (10%) + Cert(10%)|
+--------------------------------+--------------------------------+
                                 |
                                 v
+--------------------------------+--------------------------------+
|                 Dynamic Candidate Leaderboard                   |
|                & Itemized Explainability Report                 |
+-----------------------------------------------------------------+
```

---

## 🎯 Scoring & Evaluation Methodology

Scores are dynamically calculated out of **100 points** based on five transparent weighted components (weights can be customized in the UI):

1. **Technical Skill Match (40%):** Matches candidate skills against a taxonomy of programming languages, frameworks, cloud, databases, and engineering practices. Identifies exact matched and missing skills.
2. **Education Alignment (20%):** Evaluates academic level (Doctorate, Master, Bachelor, Associate) against JD requirements.
3. **Experience Relevance (20%):** Compares candidate's total years of experience against the JD threshold.
4. **Keyword Relevance (10%):** Calculates TF-IDF cosine similarity between the raw resume text and the JD.
5. **Certifications (10%):** Detects industry certifications (e.g. AWS, PMP, Scrum Master).

### Recommendation Tiers:
- **90% – 100%:** 🌟 *Excellent Match*
- **75% – 89%:** ⚡ *Strong Match*
- **60% – 74%:** 🔹 *Moderate Match*
- **Below 60%:** ⚠️ *Low Match*

---

## 📂 Project Structure

```
intelligent-resume-analyzer/
│
├── app/
│   ├── __init__.py      # Package marker
│   ├── main.py          # Terminal CLI interface
│   ├── analyzer.py      # Core orchestrator and ranking pipeline
│   ├── parser.py        # Entity extractor (Skills, Edu, Exp, Certs)
│   ├── matcher.py       # Comparison engine
│   ├── scorer.py        # Weighted scorer and explainability engine
│   └── utils.py         # Stdlib NLP utilities (N-grams, TF-IDF, Cosine Sim)
│
├── frontend/
│   ├── index.html       # Single-page Glassmorphism web dashboard
│   ├── style.css        # Premium dark-theme stylesheet
│   └── script.js        # Dashboard controller
│
├── data/
│   ├── sample_jd/       # Sample Job Descriptions (.txt)
│   └── sample_resumes/  # 5 distinct candidate resumes (.txt)
│
├── tests/
│   ├── test_parser.py   # Unit tests for entity parser
│   ├── test_matcher.py  # Unit tests for comparison engine
│   ├── test_scorer.py   # Unit tests for scoring logic
│   └── test_analyzer.py # End-to-end unit tests
│
├── server.py            # Zero-dependency Python HTTP server & REST API
├── README.md            # Complete documentation
└── .gitignore           # Git ignore configuration
```

---

## 🚀 Quick Start Guide

### Option A: Launch Web Dashboard (Recommended)

1. Open your terminal in the project directory.
2. Run the zero-dependency Python web server:
   ```bash
   py server.py
   ```
3. Open your browser to:
   ```
   http://localhost:8000
   ```
4. Click **⚡ 1-Click Load 5 Sample Resumes** and hit **🔍 Analyze & Rank Candidates**.

---

### Option B: Run Command Line Interface (CLI)

Run batch analysis directly in your terminal:
```bash
py -m app.main
```

---

## 🧪 Running Unit Tests

Verify test coverage and system stability using Python's standard `unittest`:
```bash
py -m unittest discover -s tests
```

---

## 📹 Video Demo Walkthrough

When recording a demo video, follow this recommended sequence:

1. **Launch App:** Start `py server.py` and navigate to `http://localhost:8000`.
2. **Select Job Description:** Load the pre-configured *Senior Software Engineer* sample JD.
3. **Load Candidates:** Click *1-Click Load 5 Sample Resumes* to load Alex Dev, Beatrice Data, Charlie Junior, Diana Miller, and Ethan Taylor.
4. **Run Analysis:** Click *Analyze & Rank Candidates*.
5. **Inspect Rankings:** Show how candidates are dynamically ranked (Alex Dev at #1 with 100%, down to Charlie Junior).
6. **Show Explainability:** Open Alex Dev's detail modal to view itemized score progress bars, matched skills, missing skills, and dynamic explanation text.
7. **Side-by-Side Comparison:** Open the comparative matrix to compare candidates side-by-side.
8. **Adjust Weights:** Expand *Customize Scoring Weights*, adjust slider values, and re-analyze to show dynamic recalculation.

---

## 📝 License

This project is licensed under the MIT License - open for educational and evaluation use.
