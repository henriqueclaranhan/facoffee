from datetime import datetime
from app.domain.repositories.quota_repository import QuotaRepository
from app.domain.exceptions.quota import QuotaNotFoundError
from app.domain.models.quota import ParticipationQuota
from app.application.dtos.quota import UpdateParticipationQuotaRequest
from app.domain.repositories.outbox_repository import OutboxRepository

class UpdateQuotaUseCase:
    def __init__(self, quota_repository: QuotaRepository, outbox_repository: OutboxRepository):
        self.quota_repository = quota_repository
        self.outbox_repository = outbox_repository

    def execute(self, quota_id: str, request: UpdateParticipationQuotaRequest) -> ParticipationQuota:
        quota = self.quota_repository.find_by_id(quota_id)
        if not quota:
            raise QuotaNotFoundError(f"Quota with id {quota_id} not found")
        
        # Update fields if provided
        if request.name is not None:
            quota.name = request.name
        if request.description is not None:
            quota.description = request.description
        if request.condition is not None:
            quota.condition = request.condition
        if request.items is not None:
            quota.items = request.items
        if request.amount is not None:
            quota.amount = request.amount
            
        quota.updatedAt = datetime.utcnow()
        
        # Save changes
        saved_quota = self.quota_repository.save(quota)
        
        from app.infrastructure.messaging.event_publisher import EventPublisher
        EventPublisher.publish_quota_updated(saved_quota, self.outbox_repository)
        
        return saved_quota
