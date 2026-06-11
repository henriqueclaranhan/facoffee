from datetime import datetime
from app.domain.repositories.quota_repository import QuotaRepository
from app.application.dtos.quota import UpdateParticipationQuotaRequest, ParticipationQuotaResponse
from app.domain.exceptions.quota import QuotaNotFoundException
from app.domain.models.quota import ParticipationQuotaStatus

class UpdateQuotaUseCase:
    def __init__(self, repository: QuotaRepository):
        self.repository = repository

    def execute(self, quota_id: str, request: UpdateParticipationQuotaRequest) -> ParticipationQuotaResponse:
        quota = self.repository.find_by_id(quota_id)
        if not quota:
            raise QuotaNotFoundException("Cota não encontrada.")
        
        if request.description is not None:
            quota.description = request.description
        if request.condition is not None:
            quota.condition = request.condition
        if request.items is not None:
            quota.items = request.items
        if request.amount is not None:
            quota.amount = request.amount
        if request.active is not None:
            quota.status = ParticipationQuotaStatus.ACTIVE if request.active else ParticipationQuotaStatus.INACTIVE
            
        quota.updatedAt = datetime.utcnow()
        
        updated_quota = self.repository.save(quota)
        return ParticipationQuotaResponse.from_domain(updated_quota)
