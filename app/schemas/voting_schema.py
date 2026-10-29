from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.election import ElectionStatus


class VoterCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr


class VoterRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    email: EmailStr
    is_validated: bool


class ElectionCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)


class CandidateCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str = Field(default="", max_length=500)


class CandidateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    election_id: str
    name: str
    description: str


class ElectionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    status: ElectionStatus
    candidates: list[CandidateRead]


class VoteCreate(BaseModel):
    voter_id: str = Field(min_length=1)
    candidate_id: str = Field(min_length=1)


class VoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    election_id: str
    voter_id: str
    candidate_id: str


class CandidateResult(BaseModel):
    candidate_id: str
    candidate_name: str
    vote_count: int


class ElectionResult(BaseModel):
    election_id: str
    election_title: str
    total_votes: int
    results: list[CandidateResult]
