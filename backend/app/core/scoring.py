from typing import List, Tuple


# Very simple target skill sets for roles
TARGET_SKILLS = {
    "data scientist": [
        "Python",
        "Pandas",
        "NumPy",
        "Scikit-Learn",
        "Machine Learning",
        "SQL",
    ],
    "ml engineer": [
        "Python",
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "MLOps",
    ],
    "backend engineer": [
        "Python",
        "FastAPI",
        "Django",
        "SQL",
        "Docker",
    ],
}


def compute_readiness_score_from_skills(
    skills: List[Tuple[str, int]], target_role: str
) -> int:
    """
    skills: list of (name, level)
    target_role: e.g. "Data Scientist"
    """
    role_key = target_role.lower()
    target_list = TARGET_SKILLS.get(role_key, [])

    if not target_list:
        # Unknown role: just average levels
        if not skills:
            return 10
        avg_level = sum(level for _, level in skills) / len(skills)
        return int(min(100, avg_level * 15))

    # Score based on how many target skills you have and their level
    score = 0
    max_score = len(target_list) * 10  # each skill up to 10 points

    for target in target_list:
        for name, level in skills:
            if target.lower() == name.lower():
                # level 1-5 maps to 4-10 points
                score += 4 + (level - 1) * 1.5  # rough heuristic

    if max_score == 0:
        return 10

    normalized = int((score / max_score) * 100)
    normalized = max(5, min(100, normalized))
    return normalized
