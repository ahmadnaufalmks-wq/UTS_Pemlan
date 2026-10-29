import pytest

from app.repositories.voter_repository import InMemoryVoterRepository
from app.services.errors import ConflictError, NotFoundError
from app.services.voter_service import VoterService


@pytest.fixture
def service():
    return VoterService(InMemoryVoterRepository())


def test_register_voter_starts_unvalidated(service):
    voter = service.register("Ayu", "ayu@example.com")
    assert voter.id and voter.name == "Ayu"
    assert voter.is_validated is False
    assert service.get(voter.id) == voter


def test_email_is_unique_case_insensitively(service):
    service.register("Ayu", "ayu@example.com")
    with pytest.raises(ConflictError):
        service.register("Budi", "AYU@example.com")


def test_validate_voter(service):
    voter = service.register("Ayu", "ayu@example.com")
    assert service.validate(voter.id).is_validated is True


def test_missing_voter_raises_not_found(service):
    with pytest.raises(NotFoundError):
        service.get("missing")
