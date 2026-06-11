from app.domain.repositories.quota_repository import QuotaRepository
from app.domain.exceptions.quota import QuotaNotFoundError
from app.domain.models.quota import ParticipationQuota

class GetQuotaUseCase:
    def __init__(self, quota_repository: QuotaRepository):
        self.quota_repository = quota_repository

    def execute(self, quota_id: str) -> ParticipationQuota:
        quota = self.quota_repository.find_by_id(quota_id)
        if not quota:
            raise QuotaNotFoundError(f"Quota with id {quota_id} not found")
        return quota
