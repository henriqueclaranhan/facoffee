from app.domain.repositories.participation_repository import ParticipationRepository
from app.application.dtos.participation import ParticipationResponse
from app.domain.exceptions.participation import ParticipationNotFoundException

class GetParticipationUseCase:
    def __init__(self, repository: ParticipationRepository):
        self.repository = repository

    def execute(self, participation_id: str) -> ParticipationResponse:
        participation = self.repository.find_by_id(participation_id)
        if not participation:
            raise ParticipationNotFoundException("Participação não encontrada")
        return ParticipationResponse.from_domain(participation)
