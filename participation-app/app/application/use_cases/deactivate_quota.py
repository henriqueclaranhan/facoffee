from datetime import datetime
from app.domain.repositories.quota_repository import QuotaRepository
from app.application.dtos.quota import ParticipationQuotaResponse
from app.domain.exceptions.quota import QuotaNotFoundException, QuotaConflictException
from app.domain.models.quota import ParticipationQuotaStatus

class DeactivateQuotaUseCase:
    def __init__(self, repository: QuotaRepository):
        self.repository = repository

    def execute(self, quota_id: str) -> ParticipationQuotaResponse:
        quota = self.repository.find_by_id(quota_id)
        if not quota:
            raise QuotaNotFoundException("Cota não encontrada.")
        
        # Here we should check if there are active participations
        # For now, assuming no participations for this test, but we will add logic when participation is done.
        
        quota.status = ParticipationQuotaStatus.INACTIVE
        quota.updatedAt = datetime.utcnow()
        
        updated_quota = self.repository.save(quota)
        return ParticipationQuotaResponse.from_domain(updated_quota)
