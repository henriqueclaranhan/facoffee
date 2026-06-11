from typing import List
from sqlalchemy.orm import Session
from app.domain.models.outbox import OutboxEvent
from app.domain.repositories.outbox_repository import OutboxRepository
from app.infrastructure.database.models import OutboxEventModel

class SQLAlchemyOutboxRepository(OutboxRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, event: OutboxEvent) -> OutboxEvent:
        existing = self.db.query(OutboxEventModel).filter(OutboxEventModel.id == event.id).first()
        if existing:
            existing.status = event.status
            db_model = existing
        else:
            db_model = OutboxEventModel(
                id=event.id,
                event_type=event.event_type,
                payload=event.payload,
                status=event.status,
                created_at=event.created_at
            )
            self.db.add(db_model)
        
        self.db.flush()
        return event

    def find_pending(self, limit: int = 100) -> List[OutboxEvent]:
        models = self.db.query(OutboxEventModel).filter(OutboxEventModel.status == "PENDING").limit(limit).all()
        return [
            OutboxEvent(
                id=m.id,
                event_type=m.event_type,
                payload=m.payload,
                status=m.status,
                created_at=m.created_at
            )
            for m in models
        ]
