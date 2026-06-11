from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from app.domain.models.participation import Participation, ParticipationStatus
from app.domain.repositories.participation_repository import ParticipationRepository
from app.infrastructure.database.models import ParticipationModel

class SQLAlchemyParticipationRepository(ParticipationRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: ParticipationModel) -> Participation:
        return Participation(
            id=model.id,
            userId=model.user_id,
            quotaId=model.quota_id,
            status=ParticipationStatus(model.status),
            joinedAt=model.joined_at,
            cancelledAt=model.cancelled_at
        )

    def _to_model(self, domain: Participation) -> ParticipationModel:
        return ParticipationModel(
            id=domain.id,
            user_id=domain.userId,
            quota_id=domain.quotaId,
            status=domain.status.value,
            joined_at=domain.joinedAt,
            cancelled_at=domain.cancelledAt
        )

    def save(self, participation: Participation) -> Participation:
        existing_model = self.db.query(ParticipationModel).filter(ParticipationModel.id == participation.id).first()
        
        model = self._to_model(participation)
        if existing_model:
            existing_model.status = model.status
            existing_model.cancelled_at = model.cancelled_at
            db_model = existing_model
        else:
            self.db.add(model)
            db_model = model
            
        self.db.flush()
        return self._to_domain(db_model)

    def find_all(self, offset: int, limit: int) -> Tuple[List[Participation], int]:
        query = self.db.query(ParticipationModel)
        total_elements = query.count()
        models = query.offset(offset).limit(limit).all()
        return [self._to_domain(m) for m in models], total_elements

    def find_by_id(self, participation_id: str) -> Optional[Participation]:
        model = self.db.query(ParticipationModel).filter(ParticipationModel.id == participation_id).first()
        if not model:
            return None
        return self._to_domain(model)

    def find_active_by_user(self, user_id: str) -> List[Participation]:
        models = self.db.query(ParticipationModel).filter(
            ParticipationModel.user_id == user_id,
            ParticipationModel.status == ParticipationStatus.ACTIVE.value
        ).all()
        return [self._to_domain(m) for m in models]
