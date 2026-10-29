from uuid import uuid4

from app.models.candidate import Candidate
from app.models.election import Election, ElectionStatus
from app.repositories.election_repository import ElectionRepository
from app.services.errors import NotFoundError, RuleViolationError


class ElectionService:
    def __init__(self, repository: ElectionRepository) -> None:
        self._repository = repository

    def create(self, title: str) -> Election:
        return self._repository.add(Election(str(uuid4()), title.strip()))

    def get(self, election_id: str) -> Election:
        election = self._repository.get(election_id)
        if election is None:
            raise NotFoundError("Pemilihan tidak ditemukan.")
        return election

    def list_all(self) -> list[Election]:
        return self._repository.list_all()

    def add_candidate(self, election_id: str, name: str, description: str = "") -> Candidate:
        election = self.get(election_id)
        if election.status != ElectionStatus.DRAFT:
            raise RuleViolationError("Kandidat hanya dapat ditambahkan saat pemilihan berstatus draft.")
        candidate = Candidate(str(uuid4()), election_id, name.strip(), description.strip())
        return self._repository.add_candidate(candidate)

    def open(self, election_id: str) -> Election:
        election = self.get(election_id)
        if election.status != ElectionStatus.DRAFT:
            raise RuleViolationError("Hanya pemilihan berstatus draft yang dapat dibuka.")
        if not election.candidates:
            raise RuleViolationError("Tambahkan setidaknya satu kandidat sebelum membuka pemilihan.")
        election.status = ElectionStatus.OPEN
        return election

    def close(self, election_id: str) -> Election:
        election = self.get(election_id)
        if election.status != ElectionStatus.OPEN:
            raise RuleViolationError("Hanya pemilihan berstatus open yang dapat ditutup.")
        election.status = ElectionStatus.CLOSED
        return election
