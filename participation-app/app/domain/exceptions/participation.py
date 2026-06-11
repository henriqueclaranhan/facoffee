class DomainException(Exception):
    pass

class ParticipationNotFoundError(DomainException):
    pass

class ActiveParticipationExistsError(DomainException):
    pass

class QuotaNotActiveError(DomainException):
    pass

class InvalidParticipationStateError(DomainException):
    pass

class ParticipationAuthorizationError(DomainException):
    pass
