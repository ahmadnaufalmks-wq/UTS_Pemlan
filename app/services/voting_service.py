from uuid import uuid4

from app.models.election import ElectionStatus
from app.models.vote import Vote
from app.repositories.election_repository import ElectionRepository
from app.repositories.vote_repository import VoteRepository
from app.repositories.voter_repository import VoterRepository
from app.schemas.voting_schema import CandidateResult, ElectionResult
from app.services.errors import ConflictError, NotFoundError, RuleViolationError


class VotingService:
    def __init__(self, voters: VoterRepository, elections: ElectionRepository, votes: VoteRepository) -> None:
        self._voters = voters
        self._elections = elections
        self._votes = votes

    def cast_vote(self, election_id: str, voter_id: str, candidate_id: str) -> Vote:
        election = self._elections.get(election_id)
        if election is None:
            raise NotFoundError("Pemilihan tidak ditemukan.")
        voter = self._voters.get(voter_id)
        if voter is None:
            raise NotFoundError("Pemilih tidak ditemukan.")
        if election.status != ElectionStatus.OPEN:
            raise RuleViolationError("Pemilihan belum dibuka atau sudah ditutup.")
        if not voter.is_validated:
            raise RuleViolationError("Pemilih belum divalidasi.")
        if not any(candidate.id == candidate_id for candidate in election.candidates):
            raise NotFoundError("Kandidat tidak ditemukan pada pemilihan ini.")
        if self._votes.has_voted(election_id, voter_id):
            raise ConflictError("Pemilih sudah memberikan suara pada pemilihan ini.")
        vote = Vote(str(uuid4()), election_id, voter_id, candidate_id)
        return self._votes.add(vote)

    def results(self, election_id: str) -> ElectionResult:
        election = self._elections.get(election_id)
        if election is None:
            raise NotFoundError("Pemilihan tidak ditemukan.")
        if election.status != ElectionStatus.CLOSED:
            raise RuleViolationError("Hasil hanya tersedia setelah pemilihan ditutup.")
        votes = self._votes.list_for_election(election_id)
        counts = {candidate.id: 0 for candidate in election.candidates}
        for vote in votes:
            counts[vote.candidate_id] += 1
        rows = [CandidateResult(candidate_id=c.id, candidate_name=c.name, vote_count=counts[c.id])
                for c in election.candidates]
        return ElectionResult(election_id=election.id, election_title=election.title,
                              total_votes=len(votes), results=rows)
