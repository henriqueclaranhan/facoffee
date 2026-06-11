from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from app.domain.models.quota import ParticipationQuota

class QuotaRepository(ABC):
    @abstractmethod
    def save(self, quota: ParticipationQuota) -> ParticipationQuota:
        pass

    @abstractmethod
    def find_all(self, offset: int, limit: int, active: Optional[bool] = None, condition: Optional[str] = None, items: Optional[str] = None) -> Tuple[List[ParticipationQuota], int]:
        pass

    @abstractmethod
    def find_by_id(self, quota_id: str) -> Optional[ParticipationQuota]:
        pass
