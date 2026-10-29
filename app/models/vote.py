from dataclasses import dataclass


@dataclass
class Vote:
    id: str
    election_id: str
    voter_id: str
    candidate_id: str
