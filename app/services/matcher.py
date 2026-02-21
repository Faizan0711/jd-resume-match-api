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