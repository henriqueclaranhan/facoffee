from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from app.domain.models.participation import Participation

class ParticipationRepository(ABC):
    @abstractmethod
    def save(self, participation: Participation) -> Participation:
        pass

    @abstractmethod
    def find_all(self, offset: int, limit: int) -> Tuple[List[Participation], int]:
        pass

    @abstractmethod
    def find_by_id(self, participation_id: str) -> Optional[Participation]:
        pass

    @abstractmethod
    def find_active_by_user(self, user_id: str) -> List[Participation]:
        pass
