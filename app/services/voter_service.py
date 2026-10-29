from uuid import uuid4

from app.models.voter import Voter
from app.repositories.voter_repository import VoterRepository
from app.services.errors import ConflictError, NotFoundError


class VoterService:
    def __init__(self, repository: VoterRepository) -> None:
        self._repository = repository

    def register(self, name: str, email: str) -> Voter:
        if self._repository.get_by_email(email):
            raise ConflictError("Email pemilih sudah terdaftar.")
        voter = Voter(str(uuid4()), name.strip(), email, False)
        return self._repository.add(voter)

    def get(self, voter_id: str) -> Voter:
        voter = self._repository.get(voter_id)
        if voter is None:
            raise NotFoundError("Pemilih tidak ditemukan.")
        return voter

    def list_all(self) -> list[Voter]:
        return self._repository.list_all()

    def validate(self, voter_id: str) -> Voter:
        voter = self.get(voter_id)
        voter.is_validated = True
        return voter
