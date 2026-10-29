from dataclasses import dataclass


@dataclass
class Candidate:
    id: str
    election_id: str
    name: str
    description: str = ""
