"""Map the many ways CVs name their sections onto canonical keys."""
from __future__ import annotations

import re

SECTION_ALIASES = {
    "summary": ["summary", "profile", "professional summary", "about", "about me",
                "overview", "objective", "career objective", "professional profile", "tl;dr"],
    "experience": ["experience", "work experience", "professional experience", "employment",
                   "employment history", "career history", "work history", "relevant experience"],
    "skills": ["skills", "technical skills", "core skills", "key skills", "top skills",
               "technologies", "tools", "tools & technologies", "competencies", "expertise",
               "skills & tools", "tech stack"],
    "education": ["education", "academic background", "education & training"],
    "certifications": ["certifications", "certificates", "licenses & certifications",
                       "licenses and certifications", "courses", "training"],
    "projects": ["projects", "selected projects", "side projects", "personal projects",
                 "open source"],
    "languages": ["languages"],
    "awards": ["awards", "honors", "honours", "achievements", "awards & honors"],
    "volunteering": ["volunteering", "volunteer", "volunteer experience", "community"],
    "publications": ["publications", "talks", "publications & talks"],
    "military": ["military service", "military", "army service", "national service"],
    "interests": ["interests", "hobbies"],
}

_LOOKUP = {alias: key for key, aliases in SECTION_ALIASES.items() for alias in aliases}


def canonical_section(text: str) -> str | None:
    clean = re.sub(r"[^a-z&;/ ]", "", text.lower()).strip()
    clean = re.sub(r"\s+", " ", clean)
    return _LOOKUP.get(clean)
