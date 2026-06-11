from app.domain.repositories.participation_repository import ParticipationRepository
from app.domain.exceptions.participation import ParticipationNotFoundError
from app.domain.models.participation import Participation

class GetParticipationUseCase:
    def __init__(self, participation_repository: ParticipationRepository):
        self.participation_repository = participation_repository

    def execute(self, participation_id: str) -> Participation:
        participation = self.participation_repository.find_by_id(participation_id)
        if not participation:
            raise ParticipationNotFoundError(f"Participation with id {participation_id} not found")
        return participation
