from dataclasses import dataclass


@dataclass
class Voter:
    id: str
    name: str
    email: str
    is_validated: bool = False
