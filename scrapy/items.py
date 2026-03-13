from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Company:
    title: str
    location: str
    site: Optional[str] = None
    email: Optional[str] = None


@dataclass
class Vacancy:
    title: str
    keywords: list
    posted_at: datetime
    company: Company
    description: str
    external_id: int
    source: str
    url: str
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    skills: Optional[list] = None
