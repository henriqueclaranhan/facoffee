from app.domain.repositories.participation_repository import ParticipationRepository
from app.application.dtos.participation import ParticipationPageResponse, ParticipationResponse
from app.application.dtos.quota import PageMetadataResponse
import math

class ListParticipationsUseCase:
    def __init__(self, participation_repository: ParticipationRepository):
        self.participation_repository = participation_repository

    def execute(self, page: int, size: int) -> ParticipationPageResponse:
        offset = page * size
        participations, total_elements = self.participation_repository.find_all(offset=offset, limit=size)
        
        total_pages = math.ceil(total_elements / size) if size > 0 else 0
        
        page_metadata = PageMetadataResponse(
            page=page,
            size=size,
            totalElements=total_elements,
            totalPages=total_pages
        )
        
        items = [ParticipationResponse.from_domain(p) for p in participations]
        
        return ParticipationPageResponse(items=items, page=page_metadata)
