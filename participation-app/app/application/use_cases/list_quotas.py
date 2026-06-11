import math
from app.domain.repositories.quota_repository import QuotaRepository
from app.application.dtos.quota import (
    ParticipationQuotaPageResponse,
    ParticipationQuotaResponse,
    PageMetadataResponse
)

class ListQuotasUseCase:
    def __init__(self, quota_repository: QuotaRepository):
        self.quota_repository = quota_repository

    def execute(self, page: int = 0, size: int = 20, status: str | None = None) -> ParticipationQuotaPageResponse:
        if page < 0:
            page = 0
        if size < 1:
            size = 20
        elif size > 100:
            size = 100

        offset = page * size
        limit = size

        quotas, total_elements = self.quota_repository.find_all(offset=offset, limit=limit, status=status)

        total_pages = math.ceil(total_elements / size) if total_elements > 0 else 0

        items_response = [ParticipationQuotaResponse.from_domain(q) for q in quotas]
        metadata = PageMetadataResponse(
            page=page,
            size=size,
            totalElements=total_elements,
            totalPages=total_pages
        )

        return ParticipationQuotaPageResponse(
            items=items_response,
            page=metadata
        )
