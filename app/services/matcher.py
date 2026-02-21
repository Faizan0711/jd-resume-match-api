import re
from typing import Set, List, Tuple
from .skills_catalog import SKILLS


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def contains_alias(text: str, alias: str) -> bool:
    pattern = r"\b" + re.escape(alias.lower()) + r"\b"
    return re.search(pattern, text) is not None


def extract_skills(text: str) -> Set[str]:
    t = normalize(text)
    found: Set[str] = set()

    for canonical, aliases in SKILLS.items():
        for alias in aliases:
            if contains_alias(t, alias):
                found.add(canonical)
                break

    return found


def compare_skills(jd_text: str, resume_text: str) -> Tuple[List[str], List[str]]:
    jd_skills = extract_skills(jd_text)
    resume_skills = extract_skills(resume_text)

    matched = sorted(jd_skills & resume_skills)
    missing = sorted(jd_skills - resume_skills)

    return matched, missing
def compute_score(
    jd_text: str,
    resume_text: str,
    must_have_skills: List[str] | None = None,
) -> int:
    """
    Explainable score from 0..100.

    - 70 points: overlap of JD skills found in resume
    - 30 points: must-have coverage (if provided)
    - If no must-haves: small bonus for having core skills (SQL/Python)
    """
    jd_skills = extract_skills(jd_text)
    resume_skills = extract_skills(resume_text)

    matched = jd_skills & resume_skills
    overlap_ratio = len(matched) / max(len(jd_skills), 1)
    score = 70 * overlap_ratio

    if must_have_skills:
        must_have_norm = {m.strip().lower() for m in must_have_skills if m.strip()}
        # map must-haves to canonical names if user types "PowerBI" etc (basic normalize)
        # simplest: check them directly against canonical skills
        hits = len([m for m in must_have_norm if m in resume_skills])
        total = max(len(must_have_norm), 1)
        score += 30 * (hits / total)
    else:
        core = {"sql", "python"}
        score += 10 * len(core & resume_skills)  # 0, 10, or 20

    return int(round(min(max(score, 0), 100)))