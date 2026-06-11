from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ParticipationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"

class Participation(BaseModel):
    id: str
    userId: str
    quotaId: str
    status: ParticipationStatus
    joinedAt: datetime
    cancelledAt: Optional[datetime] = None
