class DomainException(Exception):
    pass

class InvalidParticipationDataException(DomainException):
    pass

class ParticipationNotFoundException(DomainException):
    pass

class ParticipationConflictException(DomainException):
    pass
