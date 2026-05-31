from enum import Enum
from datetime import datetime
from typing import Optional
import uuid

from app.domain.exceptions.quota import InvalidQuotaDataException

class QuotaCondition(str, Enum):
    DAILY = "DAILY"
    SPORADIC = "SPORADIC"

class QuotaItems(str, Enum):
    ALL = "ALL"
    COFFEE = "COFFEE"
    COOKIES = "COOKIES"

class ParticipationQuotaStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class ParticipationQuota:
    def __init__(
        self,
        id: str,
        name: str,
        condition: QuotaCondition,
        items: QuotaItems,
        amount: float,
        status: ParticipationQuotaStatus,
        createdBy: str,
        createdAt: datetime,
        description: Optional[str] = None,
        updatedAt: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.condition = condition
        self.items = items
        self.amount = amount
        self.status = status
        self.createdBy = createdBy
        self.createdAt = createdAt
        self.description = description
        self.updatedAt = updatedAt
        self.validate()

    def validate(self):
        if not self.name or len(self.name.strip()) < 3:
            raise InvalidQuotaDataException("Quota name must be at least 3 characters long.")
        if self.amount < 0:
            raise InvalidQuotaDataException("Quota amount cannot be negative.")
        if not isinstance(self.condition, QuotaCondition):
            raise InvalidQuotaDataException("Invalid quota condition.")
        if not isinstance(self.items, QuotaItems):
            raise InvalidQuotaDataException("Invalid quota items.")
        if not isinstance(self.status, ParticipationQuotaStatus):
            raise InvalidQuotaDataException("Invalid quota status.")
        if not self.createdBy:
            raise InvalidQuotaDataException("Quota creator identifier must be provided.")

    @classmethod
    def create(
        cls,
        name: str,
        condition: QuotaCondition,
        items: QuotaItems,
        amount: float,
        createdBy: str,
        description: Optional[str] = None,
        active: bool = True
    ) -> "ParticipationQuota":
        quota_id = f"quota_{uuid.uuid4().hex[:8]}"
        status = ParticipationQuotaStatus.ACTIVE if active else ParticipationQuotaStatus.INACTIVE
        now = datetime.utcnow()
        
        return cls(
            id=quota_id,
            name=name,
            condition=condition,
            items=items,
            amount=amount,
            status=status,
            createdBy=createdBy,
            createdAt=now,
            description=description
        )
