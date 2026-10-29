from fastapi import APIRouter, Depends, Request

from app.schemas.voting_schema import VoterCreate, VoterRead
from app.services.voter_service import VoterService

router = APIRouter(prefix="/voters", tags=["Pemilih"])


def get_voter_service(request: Request) -> VoterService:
    return request.app.state.voter_service


@router.post("", response_model=VoterRead, status_code=201)
def register_voter(payload: VoterCreate, service: VoterService = Depends(get_voter_service)):
    return service.register(payload.name, str(payload.email))


@router.get("", response_model=list[VoterRead])
def list_voters(service: VoterService = Depends(get_voter_service)):
    return service.list_all()


@router.get("/{voter_id}", response_model=VoterRead)
def get_voter(voter_id: str, service: VoterService = Depends(get_voter_service)):
    return service.get(voter_id)


@router.patch("/{voter_id}/validate", response_model=VoterRead)
def validate_voter(voter_id: str, service: VoterService = Depends(get_voter_service)):
    return service.validate(voter_id)
