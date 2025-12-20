from pathlib import Path
from typing import List, Tuple, Dict

import pdfplumber


# A small list of skill keywords to match in resume text
SKILL_KEYWORDS = [
    "python",
    "java",
    "c++",
    "sql",
    "pandas",
    "numpy",
    "scikit-learn",
    "machine learning",
    "deep learning",
    "nlp",
    "fastapi",
    "django",
    "react",
    "javascript",
    "typescript",
    "docker",
    "kubernetes",
]


def extract_text_from_pdf(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    all_text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            all_text += page_text + "\n"

    return all_text


def guess_name_and_headline(lines: List[str]) -> Tuple[str, str]:
    name = ""
    headline = ""

    # Take first 2 non-empty lines as name and headline
    non_empty = [line.strip() for line in lines if line.strip()]
    if non_empty:
        name = non_empty[0]
    if len(non_empty) > 1:
        headline = non_empty[1]

    return name, headline


def extract_skills(text: str) -> List[Tuple[str, int]]:
    text_lower = text.lower()
    found = []
    for skill in SKILL_KEYWORDS:
        if skill in text_lower:
            # simple heuristic: level 3 for now
            found.append((skill.title(), 3))
    return found


def extract_experiences(lines: List[str]) -> List[Dict]:
    """
    Very naive experience extraction:
    - Pick lines containing common role keywords.
    - Assign 1 year by default.
    """
    role_keywords = ["intern", "engineer", "developer", "analyst", "scientist", "consultant"]
    experiences = []

    for line in lines:
        lower = line.lower()
        if any(k in lower for k in role_keywords):
            # Example format we expect: "Data Scientist Intern - Company XYZ"
            title = line.strip()
            company = ""
            if "-" in line:
                parts = line.split("-")
                title = parts[0].strip()
                company = parts[1].strip()

            experiences.append(
                {
                    "title": title,
                    "company": company,
                    "years": 1.0,  # default
                }
            )

    # Deduplicate by title+company
    unique = []
    seen = set()
    for exp in experiences:
        key = (exp["title"], exp["company"])
        if key not in seen:
            seen.add(key)
            unique.append(exp)

    return unique


def parse_resume_pdf(file_path: str) -> Dict:
    """
    High-level function: given a PDF path, return a dict with
    name, headline, skills, experiences.
    """
    text = extract_text_from_pdf(file_path)
    lines = text.splitlines()

    name, headline = guess_name_and_headline(lines)
    skills = extract_skills(text)
    experiences = extract_experiences(lines)

    return {
        "name": name or "Unknown",
        "headline": headline or "No headline found",
        "skills": skills,
        "experiences": experiences,
    }
