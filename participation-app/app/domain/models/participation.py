from enum import Enum
from datetime import datetime
from typing import Optional

class ParticipationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"

class Participation:
    def __init__(
        self,
        id: str,
        userId: str,
        quotaId: str,
        startCycle: str,
        status: ParticipationStatus,
        createdAt: datetime,
        quotaSnapshot: dict,
        endCycle: Optional[str] = None,
        cancelledAt: Optional[datetime] = None
    ):
        self.id = id
        self.userId = userId
        self.quotaId = quotaId
        self.startCycle = startCycle
        self.status = status
        self.createdAt = createdAt
        self.quotaSnapshot = quotaSnapshot
        self.endCycle = endCycle
        self.cancelledAt = cancelledAt
