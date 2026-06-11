from datetime import datetime
from app.domain.repositories.participation_repository import ParticipationRepository
from app.application.dtos.participation import CancelParticipationRequest, ParticipationResponse
from app.domain.exceptions.participation import ParticipationNotFoundException, InvalidParticipationDataException
from app.domain.models.participation import ParticipationStatus

class CancelParticipationUseCase:
    def __init__(self, repository: ParticipationRepository):
        self.repository = repository

    def execute(self, participation_id: str, request: CancelParticipationRequest) -> ParticipationResponse:
        participation = self.repository.find_by_id(participation_id)
        if not participation:
            raise ParticipationNotFoundException("Participação não encontrada")
            
        if participation.status == ParticipationStatus.CANCELLED:
            raise InvalidParticipationDataException("Participação já está cancelada")
            
        participation.status = ParticipationStatus.CANCELLED
        participation.endCycle = request.effectiveCycle
        participation.cancelledAt = datetime.utcnow()
        saved = self.repository.save(participation)
        return ParticipationResponse.from_domain(saved)
