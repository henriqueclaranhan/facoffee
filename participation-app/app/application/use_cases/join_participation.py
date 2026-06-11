import uuid
from datetime import datetime
from app.domain.repositories.participation_repository import ParticipationRepository
from app.domain.repositories.quota_repository import QuotaRepository
from app.application.dtos.participation import JoinParticipationQuotaRequest, ParticipationResponse
from app.domain.models.participation import Participation, ParticipationStatus
from app.domain.exceptions.participation import ParticipationConflictException, InvalidParticipationDataException
from app.domain.exceptions.quota import QuotaNotFoundException

class JoinParticipationUseCase:
    def __init__(self, participation_repo: ParticipationRepository, quota_repo: QuotaRepository):
        self.participation_repo = participation_repo
        self.quota_repo = quota_repo

    def execute(self, request: JoinParticipationQuotaRequest) -> ParticipationResponse:
        quota = self.quota_repo.find_by_id(request.quotaId)
        if not quota:
            raise QuotaNotFoundException("Cota não encontrada")
        if quota.status.value != "ACTIVE":
            raise InvalidParticipationDataException("Não é possível aderir a uma cota inativa")
            
        active_participation = self.participation_repo.find_active_by_user(request.userId)
        if active_participation:
            raise ParticipationConflictException("Usuário já possui participação ativa")
            
        part_id = f"part_{uuid.uuid4().hex[:8]}"
        snapshot = {
            "quotaId": quota.id,
            "name": quota.name,
            "condition": quota.condition.value,
            "items": quota.items.value,
            "amount": quota.amount
        }
        
        participation = Participation(
            id=part_id,
            userId=request.userId,
            quotaId=request.quotaId,
            startCycle=request.startCycle,
            status=ParticipationStatus.ACTIVE,
            createdAt=datetime.utcnow(),
            quotaSnapshot=snapshot
        )
        
        saved = self.participation_repo.save(participation)
        return ParticipationResponse.from_domain(saved)
