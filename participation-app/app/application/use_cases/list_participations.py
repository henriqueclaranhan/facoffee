import math
from typing import Optional
from app.domain.repositories.participation_repository import ParticipationRepository
from app.application.dtos.participation import ParticipationPageResponse, ParticipationResponse
from app.application.dtos.quota import PageMetadataResponse

class ListParticipationsUseCase:
    def __init__(self, repository: ParticipationRepository):
        self.repository = repository

    def execute(self, page: int, size: int, user_id: Optional[str] = None, quota_id: Optional[str] = None, status: Optional[str] = None, cycle: Optional[str] = None) -> ParticipationPageResponse:
        offset = page * size
        participations, total_elements = self.repository.find_all(
            offset=offset, limit=size, user_id=user_id, quota_id=quota_id, status=status, cycle=cycle
        )
        
        total_pages = math.ceil(total_elements / size) if size > 0 else 0
        
        return ParticipationPageResponse(
            items=[ParticipationResponse.from_domain(p) for p in participations],
            page=PageMetadataResponse(
                page=page,
                size=size,
                totalElements=total_elements,
                totalPages=total_pages
            )
        )
