from typing import Protocol

from app.models.vote import Vote


class VoteRepository(Protocol):
    def add(self, vote: Vote) -> Vote: ...
    def has_voted(self, election_id: str, voter_id: str) -> bool: ...
    def list_for_election(self, election_id: str) -> list[Vote]: ...


class InMemoryVoteRepository:
    def __init__(self) -> None:
        self._votes: dict[str, Vote] = {}

    def add(self, vote: Vote) -> Vote:
        self._votes[vote.id] = vote
        return vote

    def has_voted(self, election_id: str, voter_id: str) -> bool:
        return any(v.election_id == election_id and v.voter_id == voter_id for v in self._votes.values())

    def list_for_election(self, election_id: str) -> list[Vote]:
        return [v for v in self._votes.values() if v.election_id == election_id]
