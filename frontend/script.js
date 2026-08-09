/**
 * Intelligent Resume Analyzer Multi-Step Controller
 * Built strictly with pure Vanilla JavaScript (Zero external dependencies).
 */

const SAMPLE_JOB_DESCRIPTION = `Job Title: Software Engineer - Full Stack & Systems

Role Summary:
We are seeking a Software Engineer to design, develop, and deploy scalable software systems and databases.

Target Requirements:
- Required Skills (8): Python, Java, SQL, Machine Learning, Data Structures, Git, REST API, Problem Solving.
- Education Requirement: Bachelor's Degree in Computer Science, Information Technology, or Engineering.
- Experience Requirement: Minimum 2 years of hands-on software development experience.

Key Responsibilities:
- Build REST API backend microservices using Python and Java.
- Write optimized SQL database queries and analyze data structures.
- Implement Machine Learning algorithms and apply analytical Problem Solving.
- Use Git version control for collaborative Agile codebase maintenance.`;

const SAMPLE_CANDIDATE_RESUMES = [
    {
        id: 1,
        name: "Candidate A (8/8 Skills - Top Match)",
        resumeText: `Candidate A
Email: candidateA@example.com | Phone: (555) 019-2831

PROFESSIONAL SUMMARY:
Experienced Software Engineer with 3 years of hands-on experience engineering scalable software solutions.

TECHNICAL SKILLS:
- Languages & Tools: Python, Java, SQL, Machine Learning, Data Structures, Git, REST API, Problem Solving

EDUCATION:
- Bachelor of Technology (B.Tech) in Computer Science & Engineering (2019 - 2023)

WORK EXPERIENCE:
Software Engineer | Enterprise Systems (2023 - Present, 3 years)
- Built REST API microservices using Python, Java, and SQL databases.
- Applied Machine Learning models and Data Structures for algorithmic optimization.
- Used Git for team development and applied analytical Problem Solving.`
    },
    {
        id: 2,
        name: "Candidate B (6/8 Skills - Strong Match)",
        resumeText: `Candidate B
Email: candidateB@example.com | Phone: (555) 014-9921

PROFESSIONAL SUMMARY:
Software Developer with 2 years of software engineering experience focusing on backend APIs and database queries.

TECHNICAL SKILLS:
- Programming: Python, Java, SQL, Git, REST API, Problem Solving

EDUCATION:
- Bachelor of Science (B.Sc) in Information Technology (2020 - 2024)

WORK EXPERIENCE:
Software Developer | TechCorp (2024 - Present, 2 years)
- Developed REST API web services using Python, Java, and SQL databases.
- Managed codebase version control using Git.`
    },
    {
        id: 3,
        name: "Candidate C (4/8 Skills - Moderate Match)",
        resumeText: `Candidate C
Email: candidateC@example.com | Phone: (555) 012-7741

SUMMARY:
Junior Developer with 1 year of software experience building web components and writing SQL scripts.

TECHNICAL SKILLS:
- Skills: Python, SQL, Git, Problem Solving

EDUCATION:
- Bachelor of Computer Applications (BCA) (2021 - 2024)

WORK EXPERIENCE:
Junior Developer | Web Studio (2024 - Present, 1 year)
- Wrote basic Python utility scripts and executed SQL queries. Worked with Git.`
    },
    {
        id: 4,
        name: "Candidate D (2/8 Skills - Low Match)",
        resumeText: `Candidate D
Email: candidateD@example.com | Phone: (555) 018-4432

SUMMARY:
Entry-level enthusiast seeking web development opportunities.

SKILLS:
- HTML, CSS, basic Python, Photoshop

EDUCATION:
- High School Diploma (2022)

EXPERIENCE:
Intern | Local Media Shop (2024 - Present, 1 year)
- Created basic web pages using HTML and CSS.`
    }
];

// Global Application State Object
const state = {
    currentStep: 1,
    jobTitle: "Software Engineer",
    jdText: "",
    customWeights: { skill: 40, education: 20, experience: 20, keyword: 10, certification: 10 },
    rankings: []
};

// Independent Candidates Array State
let candidatesList = [
    { id: 1, name: SAMPLE_CANDIDATE_RESUMES[0].name, resumeText: SAMPLE_CANDIDATE_RESUMES[0].resumeText },
    { id: 2, name: SAMPLE_CANDIDATE_RESUMES[1].name, resumeText: SAMPLE_CANDIDATE_RESUMES[1].resumeText },
    { id: 3, name: SAMPLE_CANDIDATE_RESUMES[2].name, resumeText: SAMPLE_CANDIDATE_RESUMES[2].resumeText }
];

let candidateCounter = 3;

document.addEventListener("DOMContentLoaded", () => {
    // 1. Mobile Menu Navigation Toggle
    const mobileToggle = document.getElementById("mobileToggle");
    const navMenu = document.getElementById("navMenu");
    if (mobileToggle && navMenu) {
        mobileToggle.addEventListener("click", () => {
            navMenu.classList.toggle("mobile-open");
        });
    }

    // 2. Visual Non-Functional Sign In Button Listener (DOES NOTHING)
    document.getElementById("navSignInBtn")?.addEventListener("click", (e) => {
        e.preventDefault();
        // Visual button only — no modal, no popup, no login action
    });

    // 3. Direct Navigation Buttons (Get Started, Start Analyzing, Live Analyzer)
    document.getElementById("navGetStartedBtn")?.addEventListener("click", (e) => {
        e.preventDefault();
        goToStep(1);
    });
    document.getElementById("heroStartAnalyzingBtn")?.addEventListener("click", (e) => {
        e.preventDefault();
        goToStep(1);
    });
    document.getElementById("finalStartAnalyzingBtn")?.addEventListener("click", (e) => {
        e.preventDefault();
        goToStep(1);
    });
    document.getElementById("navLiveAnalyzerLink")?.addEventListener("click", (e) => {
        e.preventDefault();
        goToStep(1);
    });

    // 4. Smooth Scrolling for Anchor Links
    setupSmoothScrolling();

    // 5. Scroll Reveal & Navbar Shadow
    const navbar = document.getElementById("navbar");
    window.addEventListener("scroll", () => {
        if (window.scrollY > 20) {
            navbar.style.boxShadow = "0 4px 20px rgba(0, 0, 0, 0.08)";
        } else {
            navbar.style.boxShadow = "none";
        }
        revealOnScroll();
        highlightActiveNavLink();
    });

    revealOnScroll();

    // 6. Step 1 Initial Form Setup & Sample Loader
    const jdInput = document.getElementById("jdInput");
    if (jdInput) jdInput.value = SAMPLE_JOB_DESCRIPTION;

    document.getElementById("btnLoadJdDev")?.addEventListener("click", () => {
        jdInput.value = SAMPLE_JOB_DESCRIPTION;
        document.getElementById("jobTitleInput").value = "Software Engineer";
    });

    // Weight Slider Listeners
    ['Skill', 'Edu', 'Exp', 'Kw', 'Cert'].forEach((key) => {
        const input = document.getElementById(`weight${key}`);
        const display = document.getElementById(`val${key}`);
        if (input && display) {
            input.addEventListener("input", () => {
                display.textContent = input.value;
            });
        }
    });

    document.getElementById("toggleWeightsBtn")?.addEventListener("click", () => {
        document.getElementById("weightsPanel")?.classList.toggle("hidden");
    });

    // Step 1 Next Action
    document.getElementById("step1NextBtn")?.addEventListener("click", () => {
        const text = jdInput.value.trim();
        if (!text) {
            alert("Please enter a Job Description.");
            return;
        }
        state.jdText = text;
        state.jobTitle = document.getElementById("jobTitleInput")?.value.trim() || "Target Position";
        goToStep(2);
    });

    // Step 2 Controls & Dynamic Candidate Cards
    renderCandidateCards();

    document.getElementById("addResumeBtn")?.addEventListener("click", () => addCandidateCard());

    document.getElementById("loadSamplesBtn")?.addEventListener("click", () => {
        candidatesList = SAMPLE_CANDIDATE_RESUMES.map((c, i) => ({
            id: i + 1,
            name: c.name,
            resumeText: c.resumeText
        }));
        candidateCounter = 4;
        renderCandidateCards();
    });

    document.getElementById("fileUploadInput")?.addEventListener("change", (e) => {
        const files = e.target.files;
        if (!files || files.length === 0) return;
        Array.from(files).forEach((file) => {
            const reader = new FileReader();
            reader.onload = (event) => {
                const name = file.name.replace(/\.[^/.]+$/, "").replace(/_/g, " ");
                candidateCounter++;
                candidatesList.push({
                    id: candidateCounter,
                    name: name,
                    resumeText: event.target.result
                });
                renderCandidateCards();
            };
            reader.readAsText(file);
        });
    });

    document.getElementById("step2BackBtn")?.addEventListener("click", () => goToStep(1));

    document.getElementById("step2NextBtn")?.addEventListener("click", () => {
        if (candidatesList.length === 0) {
            alert("Please add at least one candidate resume.");
            return;
        }

        const hasEmpty = candidatesList.some(c => !c.name.trim() || !c.resumeText.trim());
        if (hasEmpty) {
            alert("Please provide name and resume content for all candidates.");
            return;
        }

        state.customWeights = {
            skill: parseFloat(document.getElementById("weightSkill").value),
            education: parseFloat(document.getElementById("weightEdu").value),
            experience: parseFloat(document.getElementById("weightExp").value),
            keyword: parseFloat(document.getElementById("weightKw").value),
            certification: parseFloat(document.getElementById("weightCert").value)
        };

        goToStep(3);
        executeAnalysisPipeline();
    });

    // Step 4 Actions
    document.getElementById("step4BackBtn")?.addEventListener("click", () => goToStep(2));
    document.getElementById("step4NewBtn")?.addEventListener("click", () => goToStep(1));

    // Step 5 Actions
    document.getElementById("step5BackBtn")?.addEventListener("click", () => goToStep(4));
    document.getElementById("step5FooterBackBtn")?.addEventListener("click", () => goToStep(4));

    // Modals
    document.getElementById("closeCompareBtn")?.addEventListener("click", () => {
        document.getElementById("compareModal")?.classList.add("hidden");
    });
    document.getElementById("openCompareBtn")?.addEventListener("click", renderComparisonModal);
    document.getElementById("exportPdfBtn")?.addEventListener("click", () => window.print());
});

// ==========================================================
// DYNAMIC CANDIDATE CARDS MANAGEMENT
// ==========================================================

function renderCandidateCards() {
    const container = document.getElementById("resumeListContainer");
    if (!container) return;
    container.innerHTML = "";

    candidatesList.forEach((c, index) => {
        const card = document.createElement("div");
        card.className = "candidate-card-box";
        card.id = `cand_box_${c.id}`;

        card.innerHTML = `
            <div class="card-head">
                <span class="cand-num-badge">Candidate ${index + 1}</span>
                <input type="text" class="card-name-input" data-id="${c.id}" value="${c.name}" placeholder="Candidate Name">
                <button class="btn-remove-card" onclick="removeCandidateCard(${c.id})" title="Remove Candidate">&times; Remove Candidate</button>
            </div>
            <div class="card-body margin-top-xs">
                <textarea class="card-text-input" data-id="${c.id}" rows="4" placeholder="Paste candidate resume text...">${c.resumeText}</textarea>
            </div>
        `;

        container.appendChild(card);
    });

    // Input event listeners for data persistence
    container.querySelectorAll(".card-name-input").forEach(inp => {
        inp.addEventListener("input", (e) => {
            const id = e.target.getAttribute("data-id");
            const item = candidatesList.find(c => c.id == id);
            if (item) item.name = e.target.value;
        });
    });

    container.querySelectorAll(".card-text-input").forEach(txt => {
        txt.addEventListener("input", (e) => {
            const id = e.target.getAttribute("data-id");
            const item = candidatesList.find(c => c.id == id);
            if (item) item.resumeText = e.target.value;
        });
    });
}

function addCandidateCard() {
    candidateCounter++;
    candidatesList.push({
        id: candidateCounter,
        name: `Candidate ${candidatesList.length + 1}`,
        resumeText: ""
    });
    renderCandidateCards();
}

function removeCandidateCard(id) {
    candidatesList = candidatesList.filter(c => c.id != id);
    renderCandidateCards();
}

// ==========================================================
// MULTI-STEP WIZARD ENGINE & BACKEND INTEGRATION
// ==========================================================

function goToStep(stepNum) {
    state.currentStep = stepNum;

    // Update Progress Indicator Nodes
    for (let i = 1; i <= 4; i++) {
        const pNode = document.getElementById(`pStep${i}`);
        const pConn = document.getElementById(`conn${i}`);

        if (pNode) {
            pNode.className = "step-node";
            if (i < stepNum) pNode.classList.add("step-done");
            else if (i === stepNum || (stepNum === 5 && i === 4)) pNode.classList.add("step-active");
        }

        if (pConn) {
            if (i < stepNum) pConn.classList.add("conn-active");
            else pConn.classList.remove("conn-active");
        }
    }

    // Hide all step screen views
    for (let i = 1; i <= 5; i++) {
        document.getElementById(`step${i}Screen`)?.classList.add("hidden");
    }

    // Un-hide current step screen view
    const currentScreen = document.getElementById(`step${stepNum}Screen`);
    if (currentScreen) {
        currentScreen.classList.remove("hidden");
    }

    // Smooth scroll to analyzer workspace
    const appElem = document.getElementById("analyzer-app");
    if (appElem) {
        const navbarHeight = document.getElementById("navbar")?.offsetHeight || 80;
        const targetPos = appElem.getBoundingClientRect().top + window.pageYOffset - navbarHeight - 10;
        window.scrollTo({ top: targetPos, behavior: "smooth" });
    }
}

async function executeAnalysisPipeline() {
    const pBar = document.getElementById("analysisProgressBar");

    if (pBar) pBar.style.width = "50%";

    try {
        const formattedResumes = candidatesList.map(c => ({
            name: c.name,
            text: c.resumeText
        }));

        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                job_description: state.jdText,
                resumes: formattedResumes,
                custom_weights: state.customWeights
            })
        });

        if (pBar) pBar.style.width = "85%";

        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                if (pBar) pBar.style.width = "100%";
                state.rankings = data.rankings;

                setTimeout(() => {
                    renderStep4Results(data);
                    goToStep(4);
                }, 500);
                return;
            }
        }
        alert("Unable to connect to the local analyzer server.");
        goToStep(2);
    } catch (err) {
        console.warn("Backend API error", err);
        alert("Unable to connect to the local analyzer server.");
        goToStep(2);
    }
}

function renderStep4Results(data) {
    const rankings = data.rankings;
    document.getElementById("statTotal").textContent = rankings.length;

    if (rankings.length > 0) {
        document.getElementById("statTopRec").textContent = `${rankings[0].name} (${rankings[0].total_score}%)`;
        const avg = (rankings.reduce((acc, c) => acc + c.total_score, 0) / rankings.length).toFixed(1);
        document.getElementById("statAvgScore").textContent = `${avg}%`;
    }

    const tbody = document.getElementById("leaderboardTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    rankings.forEach((cand) => {
        const tr = document.createElement("tr");
        const badgeClass = getRecBadgeClass(cand.recommendation);
        const skillMatch = cand.comparison.skill_match;
        const eduStatus = cand.comparison.education_match.status;
        const expStatus = cand.comparison.experience_match.status;

        tr.innerHTML = `
            <td><span class="cand-rank-circle ${cand.rank === 1 ? 'rank-1-circle' : ''}">#${cand.rank}</span></td>
            <td>
                <strong>${cand.name}</strong>
                <div style="font-size:0.78rem; color:var(--text-muted);">
                    Degree: ${cand.candidate_info.education.level} | Exp: ${cand.candidate_info.experience_years} yrs
                </div>
            </td>
            <td><strong>${skillMatch.matched_count} / ${skillMatch.total_required}</strong></td>
            <td><span class="badge-status" style="font-size:0.75rem;">${eduStatus}</span></td>
            <td><span class="badge-status" style="font-size:0.75rem;">${expStatus}</span></td>
            <td><strong style="font-size:1.05rem; color:var(--text-dark);">${cand.total_score}%</strong></td>
            <td><span class="badge-rec ${badgeClass}">${cand.recommendation}</span></td>
            <td style="text-align:right;">
                <button class="btn btn-secondary-sm" onclick="showStep5CandidateDetails(${cand.rank})">View Details &rarr;</button>
            </td>
        `;

        tbody.appendChild(tr);
    });
}

function showStep5CandidateDetails(rank) {
    const cand = state.rankings.find(c => c.rank === rank);
    if (!cand) return;

    document.getElementById("modalCandidateName").textContent = cand.name;
    document.getElementById("modalRankBadge").textContent = `Rank ${cand.rank}`;
    
    const recBadge = document.getElementById("modalRecBadge");
    recBadge.textContent = cand.recommendation;
    recBadge.className = `badge-rec ${getRecBadgeClass(cand.recommendation)}`;

    document.getElementById("modalTotalScore").textContent = `${cand.total_score}%`;

    // Core Requirements Summary Cards
    const sm = cand.comparison.skill_match;
    document.getElementById("cardSkillScore").textContent = `${sm.matched_count} / ${sm.total_required}`;
    
    const matchedContainer = document.getElementById("modalMatchedSkills");
    const missingContainer = document.getElementById("modalMissingSkills");
    matchedContainer.innerHTML = "";
    missingContainer.innerHTML = "";

    const matched = sm.matched_skills || [];
    const missing = sm.missing_skills || [];

    if (matched.length === 0) matchedContainer.innerHTML = "<span class='example-label'>No skills matched</span>";
    else matched.forEach(s => matchedContainer.innerHTML += `<span class="tag-pill-sm pill-green">✓ ${s}</span>`);

    if (missing.length === 0) missingContainer.innerHTML = "<span class='example-label'>All required skills matched!</span>";
    else missing.forEach(s => missingContainer.innerHTML += `<span class="tag-pill-sm pill-red">✗ ${s}</span>`);

    const edu = cand.comparison.education_match;
    document.getElementById("cardEduStatus").textContent = edu.status;
    document.getElementById("cardEduDetail").textContent = `Candidate Level: ${cand.candidate_info.education.level}`;

    const exp = cand.comparison.experience_match;
    document.getElementById("cardExpStatus").textContent = exp.status;
    document.getElementById("cardExpDetail").textContent = `Candidate Experience: ${cand.candidate_info.experience_years} Years`;

    // Itemized Score Breakdown
    const bd = cand.breakdown;
    document.getElementById("modalSkillScore").textContent = `${bd.skill_match.score} / ${bd.skill_match.max_score} pts`;
    document.getElementById("modalEduScore").textContent = `${bd.education_match.score} / ${bd.education_match.max_score} pts`;
    document.getElementById("modalExpScore").textContent = `${bd.experience_match.score} / ${bd.experience_match.max_score} pts`;
    document.getElementById("modalKwScore").textContent = `${bd.keyword_match.score} / ${bd.keyword_match.max_score} pts`;
    document.getElementById("modalCertScore").textContent = `${bd.certification_match.score} / ${bd.certification_match.max_score} pts`;

    document.getElementById("barSkill").style.width = `${(bd.skill_match.score / bd.skill_match.max_score) * 100}%`;
    document.getElementById("barEdu").style.width = `${(bd.education_match.score / bd.education_match.max_score) * 100}%`;
    document.getElementById("barExp").style.width = `${(bd.experience_match.score / bd.experience_match.max_score) * 100}%`;
    document.getElementById("barKw").style.width = `${(bd.keyword_match.score / bd.keyword_match.max_score) * 100}%`;
    document.getElementById("barCert").style.width = `${(bd.certification_match.score / bd.certification_match.max_score) * 100}%`;

    document.getElementById("modalExplanationSummary").textContent = cand.explanation.summary;
    const bulletsList = document.getElementById("modalExplanationBullets");
    bulletsList.innerHTML = "";
    cand.explanation.bullets.forEach(b => bulletsList.innerHTML += `<li>${b}</li>`);

    goToStep(5);
}

function getRecBadgeClass(rec) {
    if (rec.includes("Excellent")) return "badge-excellent";
    if (rec.includes("Strong")) return "badge-strong";
    if (rec.includes("Moderate")) return "badge-mod";
    return "badge-low";
}

function renderComparisonModal() {
    if (!state.rankings || state.rankings.length === 0) {
        alert("Please complete candidate analysis first to view comparative matrix.");
        return;
    }

    const container = document.getElementById("compareTableContainer");
    let html = `
        <table class="compare-matrix">
            <thead>
                <tr>
                    <th>Metric</th>
                    ${state.rankings.map(c => `<th>${c.name} (Rank ${c.rank})</th>`).join("")}
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Overall Match Score</strong></td>
                    ${state.rankings.map(c => `<td><strong>${c.total_score}%</strong> (${c.recommendation})</td>`).join("")}
                </tr>
                <tr>
                    <td><strong>Required Skills (8)</strong></td>
                    ${state.rankings.map(c => `<td>${c.comparison.skill_match.matched_count} / 8 matched</td>`).join("")}
                </tr>
                <tr>
                    <td><strong>Education Level</strong></td>
                    ${state.rankings.map(c => `<td>${c.candidate_info.education.level} (${c.comparison.education_match.status})</td>`).join("")}
                </tr>
                <tr>
                    <td><strong>Experience (2 Yrs Req)</strong></td>
                    ${state.rankings.map(c => `<td>${c.candidate_info.experience_years} yrs (${c.comparison.experience_match.status})</td>`).join("")}
                </tr>
                <tr>
                    <td><strong>Missing Skills</strong></td>
                    ${state.rankings.map(c => `<td>${c.comparison.skill_match.missing_skills.join(", ") || "None"}</td>`).join("")}
                </tr>
            </tbody>
        </table>
    `;

    container.innerHTML = html;
    document.getElementById("compareModal")?.classList.remove("hidden");
}

function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener("click", function (e) {
            const href = this.getAttribute("href");
            if (href === "#") return;

            e.preventDefault();
            const targetElement = document.querySelector(href);
            if (targetElement) {
                const navbarHeight = document.getElementById("navbar")?.offsetHeight || 80;
                const elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
                const offsetPosition = elementPosition - navbarHeight - 10;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth"
                });

                if (href === "#analyzer-app" && state.currentStep !== 4 && state.currentStep !== 5) {
                    goToStep(1);
                }

                const navMenu = document.getElementById("navMenu");
                if (navMenu) navMenu.classList.remove("mobile-open");
            }
        });
    });
}

function highlightActiveNavLink() {
    const sections = document.querySelectorAll("section[id]");
    const scrollPos = window.pageYOffset + 120;

    sections.forEach((sec) => {
        const top = sec.offsetTop;
        const height = sec.offsetHeight;
        const id = sec.getAttribute("id");

        if (scrollPos >= top && scrollPos < top + height) {
            document.querySelectorAll(".nav-link").forEach((link) => {
                link.classList.remove("active");
                if (link.getAttribute("href") === `#${id}`) {
                    link.classList.add("active");
                }
            });
        }
    });
}

function revealOnScroll() {
    const reveals = document.querySelectorAll(".reveal");
    const windowHeight = window.innerHeight;
    reveals.forEach((el) => {
        const top = el.getBoundingClientRect().top;
        if (top < windowHeight - 60) {
            el.classList.add("active");
            el.style.opacity = "1";
            el.style.transform = "translateY(0)";
        }
    });
}
