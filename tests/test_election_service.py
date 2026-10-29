import pytest

from app.models.election import ElectionStatus
from app.repositories.election_repository import InMemoryElectionRepository
from app.services.election_service import ElectionService
from app.services.errors import NotFoundError, RuleViolationError


@pytest.fixture
def service():
    return ElectionService(InMemoryElectionRepository())


def test_create_election_and_add_candidate(service):
    election = service.create("Ketua Kelas")
    candidate = service.add_candidate(election.id, "Ayu", "Kandidat satu")
    assert election.status == ElectionStatus.DRAFT
    assert election.candidates == [candidate]
    assert candidate.election_id == election.id


def test_cannot_open_without_candidates(service):
    election = service.create("Ketua Kelas")
    with pytest.raises(RuleViolationError):
        service.open(election.id)


def test_open_then_close_election(service):
    election = service.create("Ketua Kelas")
    service.add_candidate(election.id, "Ayu")
    assert service.open(election.id).status == ElectionStatus.OPEN
    assert service.close(election.id).status == ElectionStatus.CLOSED


def test_candidate_cannot_be_added_after_open(service):
    election = service.create("Ketua Kelas")
    service.add_candidate(election.id, "Ayu")
    service.open(election.id)
    with pytest.raises(RuleViolationError):
        service.add_candidate(election.id, "Budi")


def test_missing_election_raises_not_found(service):
    with pytest.raises(NotFoundError):
        service.get("missing")
