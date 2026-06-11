from pydantic import BaseModel, Field
from typing import List, Optional
from app.domain.models.participation import ParticipationStatus, Participation
from app.application.dtos.quota import PageMetadataResponse

class JoinParticipationQuotaRequest(BaseModel):
    quotaId: str = Field(..., examples=["quota_001"])

class CancelParticipationRequest(BaseModel):
    reason: Optional[str] = Field(None, examples=["Mudança de departamento"])

class ParticipationResponse(BaseModel):
    id: str = Field(..., examples=["part_001"])
    userId: str = Field(..., examples=["usr_001"])
    quotaId: str = Field(..., examples=["quota_001"])
    status: ParticipationStatus
    joinedAt: str = Field(..., examples=["2026-05-01T08:00:00Z"])
    cancelledAt: Optional[str] = Field(None, examples=["2026-05-02T10:00:00Z"])

    @classmethod
    def from_domain(cls, domain: "Participation") -> "ParticipationResponse":
        return cls(
            id=domain.id,
            userId=domain.userId,
            quotaId=domain.quotaId,
            status=domain.status,
            joinedAt=domain.joinedAt.isoformat() + "Z" if not domain.joinedAt.isoformat().endswith("Z") else domain.joinedAt.isoformat(),
            cancelledAt=domain.cancelledAt.isoformat() + "Z" if domain.cancelledAt else None
        )

class ParticipationPageResponse(BaseModel):
    items: List[ParticipationResponse]
    page: PageMetadataResponse
