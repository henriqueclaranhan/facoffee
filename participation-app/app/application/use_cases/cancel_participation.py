from datetime import datetime
from app.domain.repositories.participation_repository import ParticipationRepository
from app.domain.exceptions.participation import ParticipationNotFoundError, InvalidParticipationStateError, ParticipationAuthorizationError
from app.domain.models.participation import Participation, ParticipationStatus
from app.application.dtos.participation import CancelParticipationRequest
from app.domain.repositories.outbox_repository import OutboxRepository

class CancelParticipationUseCase:
    def __init__(self, participation_repository: ParticipationRepository, outbox_repository: OutboxRepository):
        self.participation_repository = participation_repository
        self.outbox_repository = outbox_repository

    def execute(self, participation_id: str, request: CancelParticipationRequest, current_user_id: str, is_manager: bool) -> Participation:
        participation = self.participation_repository.find_by_id(participation_id)
        if not participation:
            raise ParticipationNotFoundError(f"Participation with id {participation_id} not found")
            
        if participation.userId != current_user_id and not is_manager:
            raise ParticipationAuthorizationError("User is not authorized to cancel this participation")

        if participation.status == ParticipationStatus.CANCELLED:
            raise InvalidParticipationStateError(f"Participation {participation_id} is already cancelled")
            
        participation.status = ParticipationStatus.CANCELLED
        participation.cancelledAt = datetime.utcnow()
        
        saved_participation = self.participation_repository.save(participation)
        
        from app.infrastructure.messaging.event_publisher import EventPublisher
        EventPublisher.publish_participation_cancelled(saved_participation, self.outbox_repository)
        
        return saved_participation
