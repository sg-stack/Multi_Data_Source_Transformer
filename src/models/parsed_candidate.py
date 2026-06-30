from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ParsedCandidate:
    source: str
    candidate_id: Optional[str]=None
    full_name: Optional[str] = None
    emails: List[str] = field(default_factory=list)
    phones: List[str] = field(default_factory=list)
    location: Dict[str, Optional[str]] = field(
    default_factory=lambda: {
        "city": None,
        "region": None,
        "country": None
    }
)
    headline: Optional[str] = None
    years_experience:Optional[int]=0
    skills: List[str] = field(default_factory=list)
    experience: List[Dict[str, Any]] = field(default_factory=list)
    education: List[Dict[str, Any]] = field(default_factory=list)
    projects: List[Dict[str, Any]] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    links: List[Dict[str,str]]=field(default_factory=list)
    Achievements: List[str]=field(default_factory=list)