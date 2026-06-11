from app.domain.repositories.quota_repository import QuotaRepository
from app.application.dtos.quota import ParticipationQuotaResponse
from app.domain.exceptions.quota import QuotaNotFoundException

class GetQuotaUseCase:
    def __init__(self, repository: QuotaRepository):
        self.repository = repository

    def execute(self, quota_id: str) -> ParticipationQuotaResponse:
        quota = self.repository.find_by_id(quota_id)
        if not quota:
            raise QuotaNotFoundException("Cota não encontrada.")
        return ParticipationQuotaResponse.from_domain(quota)
