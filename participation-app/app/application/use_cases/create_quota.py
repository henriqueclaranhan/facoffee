from app.domain.models.quota import ParticipationQuota
from app.domain.repositories.quota_repository import QuotaRepository
from app.application.dtos.quota import CreateParticipationQuotaRequest, ParticipationQuotaResponse
from app.domain.repositories.outbox_repository import OutboxRepository

class CreateQuotaUseCase:
    def __init__(self, quota_repository: QuotaRepository, outbox_repository: OutboxRepository):
        self.quota_repository = quota_repository
        self.outbox_repository = outbox_repository

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
        
        from app.infrastructure.messaging.event_publisher import EventPublisher
        EventPublisher.publish_quota_created(saved_quota, self.outbox_repository)
            
        return ParticipationQuotaResponse.from_domain(saved_quota)
