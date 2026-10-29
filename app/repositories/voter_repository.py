from typing import Protocol

from app.models.voter import Voter


class VoterRepository(Protocol):
    def add(self, voter: Voter) -> Voter: ...
    def get(self, voter_id: str) -> Voter | None: ...
    def get_by_email(self, email: str) -> Voter | None: ...
    def list_all(self) -> list[Voter]: ...


class InMemoryVoterRepository:
    def __init__(self) -> None:
        self._voters: dict[str, Voter] = {}

    def add(self, voter: Voter) -> Voter:
        self._voters[voter.id] = voter
        return voter

    def get(self, voter_id: str) -> Voter | None:
        return self._voters.get(voter_id)

    def get_by_email(self, email: str) -> Voter | None:
        key = email.casefold()
        return next((v for v in self._voters.values() if v.email.casefold() == key), None)

    def list_all(self) -> list[Voter]:
        return list(self._voters.values())
