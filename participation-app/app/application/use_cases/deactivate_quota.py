from datetime import datetime
from app.domain.repositories.quota_repository import QuotaRepository
from app.domain.repositories.outbox_repository import OutboxRepository
from app.domain.exceptions.quota import QuotaNotFoundError, InvalidQuotaStateError
from app.domain.models.quota import ParticipationQuota, ParticipationQuotaStatus

class DeactivateQuotaUseCase:
    def __init__(self, quota_repository: QuotaRepository, outbox_repository: OutboxRepository):
        self.quota_repository = quota_repository
        self.outbox_repository = outbox_repository

    def execute(self, quota_id: str) -> ParticipationQuota:
        quota = self.quota_repository.find_by_id(quota_id)
        if not quota:
            raise QuotaNotFoundError(f"Quota with id {quota_id} not found")
            
        if quota.status == ParticipationQuotaStatus.INACTIVE:
            raise InvalidQuotaStateError(f"Quota {quota_id} is already inactive")
            
        # TODO: Check if there are active memberships before deactivating (business rule to be decided)
        
        quota.status = ParticipationQuotaStatus.INACTIVE
        quota.updatedAt = datetime.utcnow()
        
        saved_quota = self.quota_repository.save(quota)
        
        from app.infrastructure.messaging.event_publisher import EventPublisher
        EventPublisher.publish_quota_updated(saved_quota, self.outbox_repository)
        
        return saved_quota
