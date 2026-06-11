from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.domain.models.participation import ParticipationStatus
from app.application.dtos.quota import ParticipationQuotaResponse, PageMetadataResponse

class JoinParticipationQuotaRequest(BaseModel):
    userId: str
    quotaId: str
    startCycle: str

class CancelParticipationRequest(BaseModel):
    requestedBy: str
    reason: str
    effectiveCycle: str

class ParticipationResponse(BaseModel):
    id: str
    userId: str
    quotaId: str
    status: ParticipationStatus
    startCycle: str
    endCycle: Optional[str] = None
    quotaSnapshot: dict
    createdAt: str
    cancelledAt: Optional[str] = None

    @classmethod
    def from_domain(cls, domain) -> "ParticipationResponse":
        return cls(
            id=domain.id,
            userId=domain.userId,
            quotaId=domain.quotaId,
            status=domain.status,
            startCycle=domain.startCycle,
            endCycle=domain.endCycle,
            quotaSnapshot=domain.quotaSnapshot,
            createdAt=domain.createdAt.isoformat() + "Z" if not domain.createdAt.isoformat().endswith("Z") else domain.createdAt.isoformat(),
            cancelledAt=domain.cancelledAt.isoformat() + "Z" if domain.cancelledAt else None
        )

class ParticipationPageResponse(BaseModel):
    items: List[ParticipationResponse]
    page: PageMetadataResponse
