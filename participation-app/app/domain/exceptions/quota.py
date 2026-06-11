class DomainException(Exception):
    pass

class InvalidQuotaDataException(DomainException):
    pass

class QuotaNotFoundError(DomainException):
    pass

class InvalidQuotaStateError(DomainException):
    pass
