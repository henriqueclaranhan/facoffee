from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.domain.models.quota import QuotaCondition, QuotaItems, ParticipationQuotaStatus, ParticipationQuota

class CreateParticipationQuotaRequest(BaseModel):
    name: str = Field(..., min_length=3, examples=["Cota diária completa"])
    description: Optional[str] = Field(None, examples=["Participante diário com acesso a café e bolachas."])
    condition: QuotaCondition
    items: QuotaItems
    amount: float = Field(..., ge=0, description="Valor definido pelo gestor. O serviço não calcula este valor automaticamente.")
    active: bool = Field(True)

class UpdateParticipationQuotaRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=3)
    description: Optional[str] = Field(None)
    condition: Optional[QuotaCondition] = None
    items: Optional[QuotaItems] = None
    amount: Optional[float] = Field(None, ge=0)

class ParticipationQuotaResponse(BaseModel):
    id: str = Field(..., examples=["quota_001"])
    name: str = Field(..., examples=["Cota diária completa"])
    description: Optional[str] = Field(None, examples=["Participante diário com acesso a café e bolachas."])
    condition: QuotaCondition
    items: QuotaItems
    amount: float = Field(..., examples=[40.00])
    status: ParticipationQuotaStatus
    createdBy: str = Field(..., examples=["usr_manager_001"])
    createdAt: str = Field(..., examples=["2026-05-01T08:00:00Z"])
    updatedAt: Optional[str] = Field(None, examples=["2026-05-02T10:00:00Z"])

    @classmethod
    def from_domain(cls, domain: "ParticipationQuota") -> "ParticipationQuotaResponse":
        return cls(
            id=domain.id,
            name=domain.name,
            description=domain.description,
            condition=domain.condition,
            items=domain.items,
            amount=domain.amount,
            status=domain.status,
            createdBy=domain.createdBy,
            createdAt=domain.createdAt.isoformat() + "Z" if not domain.createdAt.isoformat().endswith("Z") else domain.createdAt.isoformat(),
            updatedAt=domain.updatedAt.isoformat() + "Z" if domain.updatedAt else None
        )

class PageMetadataResponse(BaseModel):
    page: int = Field(..., examples=[0])
    size: int = Field(..., examples=[20])
    totalElements: int = Field(..., examples=[42])
    totalPages: int = Field(..., examples=[3])

class ParticipationQuotaPageResponse(BaseModel):
    items: List[ParticipationQuotaResponse]
    page: PageMetadataResponse
