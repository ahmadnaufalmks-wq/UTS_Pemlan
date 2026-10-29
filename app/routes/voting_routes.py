from fastapi import APIRouter, Depends, Request

from app.schemas.voting_schema import VoteCreate, VoteRead
from app.services.voting_service import VotingService

router = APIRouter(prefix="/elections", tags=["Voting"])


def get_voting_service(request: Request) -> VotingService:
    return request.app.state.voting_service


@router.post("/{election_id}/votes", response_model=VoteRead, status_code=201)
def cast_vote(election_id: str, payload: VoteCreate,
              service: VotingService = Depends(get_voting_service)):
    return service.cast_vote(election_id, payload.voter_id, payload.candidate_id)
