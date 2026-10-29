class VotingError(Exception):
    """Base domain error translated into an HTTP response."""


class NotFoundError(VotingError):
    pass


class ConflictError(VotingError):
    pass


class RuleViolationError(VotingError):
    pass
