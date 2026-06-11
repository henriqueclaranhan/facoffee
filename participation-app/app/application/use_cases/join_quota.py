import uuid
from datetime import datetime
from app.domain.repositories.participation_repository import ParticipationRepository
from app.domain.repositories.quota_repository import QuotaRepository
from app.domain.models.participation import Participation, ParticipationStatus
from app.domain.models.quota import ParticipationQuotaStatus
from app.domain.exceptions.participation import ActiveParticipationExistsError, QuotaNotActiveError
from app.domain.exceptions.quota import QuotaNotFoundError
from app.domain.repositories.outbox_repository import OutboxRepository

class JoinQuotaUseCase:
    def __init__(self, participation_repository: ParticipationRepository, quota_repository: QuotaRepository, outbox_repository: OutboxRepository):
        self.participation_repository = participation_repository
        self.quota_repository = quota_repository
        self.outbox_repository = outbox_repository

    def execute(self, user_id: str, quota_id: str) -> Participation:
        quota = self.quota_repository.find_by_id(quota_id)
        if not quota:
            raise QuotaNotFoundError(f"Quota with id {quota_id} not found")
            
        if quota.status != ParticipationQuotaStatus.ACTIVE:
            raise QuotaNotActiveError(f"Quota {quota_id} is not active")
            
        active_participations = self.participation_repository.find_active_by_user(user_id)
        if active_participations:
            raise ActiveParticipationExistsError("User already has an active participation")
            
        participation = Participation(
            id=f"part_{uuid.uuid4().hex[:8]}",
            userId=user_id,
            quotaId=quota_id,
            status=ParticipationStatus.ACTIVE,
            joinedAt=datetime.utcnow()
        )
        
        saved_participation = self.participation_repository.save(participation)
        
        from app.infrastructure.messaging.event_publisher import EventPublisher
        EventPublisher.publish_participation_created(saved_participation, self.outbox_repository)
        
        return saved_participation
