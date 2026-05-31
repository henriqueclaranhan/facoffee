from app.domain.models.quota import ParticipationQuota
from app.domain.repositories.quota_repository import QuotaRepository
from app.application.dtos.quota import CreateParticipationQuotaRequest, ParticipationQuotaResponse

class CreateQuotaUseCase:
    def __init__(self, quota_repository: QuotaRepository):
        self.quota_repository = quota_repository

    def execute(self, request: CreateParticipationQuotaRequest, manager_id: str) -> ParticipationQuotaResponse:
        quota = ParticipationQuota.create(
            name=request.name,
            condition=request.condition,
            items=request.items,
            amount=request.amount,
            createdBy=manager_id,
            description=request.description,
            active=request.active
        )
        
        saved_quota = self.quota_repository.save(quota)
        
        return ParticipationQuotaResponse.from_domain(saved_quota)
