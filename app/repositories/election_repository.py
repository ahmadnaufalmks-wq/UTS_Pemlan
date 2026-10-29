from typing import Protocol

from app.models.candidate import Candidate
from app.models.election import Election


class ElectionRepository(Protocol):
    def add(self, election: Election) -> Election: ...
    def get(self, election_id: str) -> Election | None: ...
    def list_all(self) -> list[Election]: ...
    def add_candidate(self, candidate: Candidate) -> Candidate: ...


class InMemoryElectionRepository:
    def __init__(self) -> None:
        self._elections: dict[str, Election] = {}

    def add(self, election: Election) -> Election:
        self._elections[election.id] = election
        return election

    def get(self, election_id: str) -> Election | None:
        return self._elections.get(election_id)

    def list_all(self) -> list[Election]:
        return list(self._elections.values())

    def add_candidate(self, candidate: Candidate) -> Candidate:
        self._elections[candidate.election_id].candidates.append(candidate)
        return candidate
