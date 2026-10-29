import pytest

from app.repositories.election_repository import InMemoryElectionRepository
from app.repositories.vote_repository import InMemoryVoteRepository
from app.repositories.voter_repository import InMemoryVoterRepository
from app.services.election_service import ElectionService
from app.services.errors import ConflictError, NotFoundError, RuleViolationError
from app.services.voter_service import VoterService
from app.services.voting_service import VotingService


@pytest.fixture
def setup_voting():
    voter_repo, election_repo, vote_repo = (InMemoryVoterRepository(), InMemoryElectionRepository(),
                                            InMemoryVoteRepository())
    voter_service = VoterService(voter_repo)
    election_service = ElectionService(election_repo)
    voting_service = VotingService(voter_repo, election_repo, vote_repo)
    voter = voter_service.register("Ayu", "ayu@example.com")
    election = election_service.create("Ketua Kelas")
    candidate = election_service.add_candidate(election.id, "Ayu")
    election_service.add_candidate(election.id, "Budi")
    election_service.open(election.id)
    voter_service.validate(voter.id)
    return voter_service, election_service, voting_service, voter, election, candidate


def test_validated_voter_can_vote_once(setup_voting):
    _, _, voting, voter, election, candidate = setup_voting
    vote = voting.cast_vote(election.id, voter.id, candidate.id)
    assert vote.voter_id == voter.id and vote.candidate_id == candidate.id


def test_unvalidated_voter_cannot_vote(setup_voting):
    voters, _, voting, _, election, candidate = setup_voting
    unvalidated = voters.register("Budi", "budi@example.com")
    with pytest.raises(RuleViolationError):
        voting.cast_vote(election.id, unvalidated.id, candidate.id)


def test_duplicate_vote_is_rejected(setup_voting):
    _, _, voting, voter, election, candidate = setup_voting
    voting.cast_vote(election.id, voter.id, candidate.id)
    with pytest.raises(ConflictError):
        voting.cast_vote(election.id, voter.id, candidate.id)


def test_vote_rejected_for_closed_election(setup_voting):
    _, elections, voting, voter, election, candidate = setup_voting
    elections.close(election.id)
    with pytest.raises(RuleViolationError):
        voting.cast_vote(election.id, voter.id, candidate.id)


def test_candidate_must_belong_to_election(setup_voting):
    _, elections, voting, voter, election, _ = setup_voting
    other = elections.create("Pemilihan lain")
    foreign = elections.add_candidate(other.id, "Lain")
    with pytest.raises(NotFoundError):
        voting.cast_vote(election.id, voter.id, foreign.id)


def test_results_count_votes_and_require_closed_election(setup_voting):
    _, elections, voting, voter, election, candidate = setup_voting
    with pytest.raises(RuleViolationError):
        voting.results(election.id)
    voting.cast_vote(election.id, voter.id, candidate.id)
    elections.close(election.id)
    result = voting.results(election.id)
    assert result.total_votes == 1
    assert result.results[0].candidate_id == candidate.id
    assert result.results[0].vote_count == 1
    assert result.results[1].vote_count == 0
