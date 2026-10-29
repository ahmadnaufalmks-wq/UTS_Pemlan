from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.repositories.election_repository import InMemoryElectionRepository
from app.repositories.vote_repository import InMemoryVoteRepository
from app.repositories.voter_repository import InMemoryVoterRepository
from app.routes import election_routes, voter_routes, voting_routes
from app.services.election_service import ElectionService
from app.services.errors import ConflictError, NotFoundError, RuleViolationError
from app.services.voter_service import VoterService
from app.services.voting_service import VotingService


def create_app() -> FastAPI:
    app = FastAPI(title="Digital Voting API", version="1.0.0",
                  description="API pemilihan dengan penyimpanan sementara di memori.")
    voters = InMemoryVoterRepository()
    elections = InMemoryElectionRepository()
    votes = InMemoryVoteRepository()
    app.state.voter_service = VoterService(voters)
    app.state.election_service = ElectionService(elections)
    app.state.voting_service = VotingService(voters, elections, votes)

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(ConflictError)
    async def conflict_handler(request: Request, exc: ConflictError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(RuleViolationError)
    async def rule_violation_handler(request: Request, exc: RuleViolationError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    app.include_router(voter_routes.router)
    app.include_router(election_routes.router)
    app.include_router(voting_routes.router)

    @app.get("/health", tags=["Sistem"])
    def health_check():
        return {"status": "ok"}

    return app


app = create_app()
