from dataclasses import dataclass, field
from enum import Enum

from app.models.candidate import Candidate


class ElectionStatus(str, Enum):
    DRAFT = "draft"
    OPEN = "open"
    CLOSED = "closed"


@dataclass
class Election:
    id: str
    title: str
    status: ElectionStatus = ElectionStatus.DRAFT
    candidates: list[Candidate] = field(default_factory=list)
