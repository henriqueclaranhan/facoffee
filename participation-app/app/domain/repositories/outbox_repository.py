from abc import ABC, abstractmethod
from typing import List
from app.domain.models.outbox import OutboxEvent

class OutboxRepository(ABC):
    @abstractmethod
    def save(self, event: OutboxEvent) -> OutboxEvent:
        pass

    @abstractmethod
    def find_pending(self, limit: int = 100) -> List[OutboxEvent]:
        pass
