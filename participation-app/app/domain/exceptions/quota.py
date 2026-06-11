class DomainException(Exception):
    pass

class InvalidQuotaDataException(DomainException):
    pass

class QuotaNotFoundException(DomainException):
    pass

class QuotaConflictException(DomainException):
    pass
