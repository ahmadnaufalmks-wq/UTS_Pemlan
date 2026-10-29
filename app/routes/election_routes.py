from fastapi import APIRouter, Depends, Request

from app.schemas.voting_schema import CandidateCreate, CandidateRead, ElectionCreate, ElectionRead, ElectionResult
from app.services.election_service import ElectionService
from app.services.voting_service import VotingService

router = APIRouter(prefix="/elections", tags=["Pemilihan"])


def get_election_service(request: Request) -> ElectionService:
    return request.app.state.election_service


def get_voting_service(request: Request) -> VotingService:
    return request.app.state.voting_service


@router.post("", response_model=ElectionRead, status_code=201)
def create_election(payload: ElectionCreate, service: ElectionService = Depends(get_election_service)):
    return service.create(payload.title)


@router.get("", response_model=list[ElectionRead])
def list_elections(service: ElectionService = Depends(get_election_service)):
    return service.list_all()


@router.get("/{election_id}", response_model=ElectionRead)
def get_election(election_id: str, service: ElectionService = Depends(get_election_service)):
    return service.get(election_id)


@router.post("/{election_id}/candidates", response_model=CandidateRead, status_code=201)
def add_candidate(election_id: str, payload: CandidateCreate,
                  service: ElectionService = Depends(get_election_service)):
    return service.add_candidate(election_id, payload.name, payload.description)


@router.post("/{election_id}/open", response_model=ElectionRead)
def open_election(election_id: str, service: ElectionService = Depends(get_election_service)):
    return service.open(election_id)


@router.post("/{election_id}/close", response_model=ElectionRead)
def close_election(election_id: str, service: ElectionService = Depends(get_election_service)):
    return service.close(election_id)


@router.get("/{election_id}/results", response_model=ElectionResult)
def election_results(election_id: str, service: VotingService = Depends(get_voting_service)):
    return service.results(election_id)
