from typing import List, Tuple, Optional
import json
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
            startCycle=model.start_cycle,
            status=ParticipationStatus(model.status),
            createdAt=model.created_at,
            quotaSnapshot=json.loads(model.quota_snapshot),
            endCycle=model.effective_cycle,
            cancelledAt=model.updated_at
        )

    def _to_model(self, domain: Participation) -> ParticipationModel:
        return ParticipationModel(
            id=domain.id,
            user_id=domain.userId,
            quota_id=domain.quotaId,
            start_cycle=domain.startCycle,
            status=domain.status.value,
            created_at=domain.createdAt,
            quota_snapshot=json.dumps(domain.quotaSnapshot),
            effective_cycle=domain.endCycle,
            updated_at=domain.cancelledAt
        )

    def save(self, participation: Participation) -> Participation:
        existing_model = self.db.query(ParticipationModel).filter(ParticipationModel.id == participation.id).first()
        model = self._to_model(participation)
        if existing_model:
            existing_model.status = model.status
            existing_model.effective_cycle = model.effective_cycle
            existing_model.updated_at = model.updated_at
            db_model = existing_model
        else:
            self.db.add(model)
            db_model = model
            
        self.db.commit()
        self.db.refresh(db_model)
        return self._to_domain(db_model)

    def find_all(self, offset: int, limit: int, user_id: Optional[str] = None, quota_id: Optional[str] = None, status: Optional[str] = None, cycle: Optional[str] = None) -> Tuple[List[Participation], int]:
        query = self.db.query(ParticipationModel)
        if user_id:
            query = query.filter(ParticipationModel.user_id == user_id)
        if quota_id:
            query = query.filter(ParticipationModel.quota_id == quota_id)
        if status:
            query = query.filter(ParticipationModel.status == status)
        if cycle:
            query = query.filter(ParticipationModel.start_cycle <= cycle)
            
        total_elements = query.count()
        models = query.offset(offset).limit(limit).all()
        return [self._to_domain(m) for m in models], total_elements

    def find_by_id(self, participation_id: str) -> Optional[Participation]:
        model = self.db.query(ParticipationModel).filter(ParticipationModel.id == participation_id).first()
        if not model:
            return None
        return self._to_domain(model)

    def find_active_by_user(self, user_id: str) -> Optional[Participation]:
        model = self.db.query(ParticipationModel).filter(
            ParticipationModel.user_id == user_id,
            ParticipationModel.status == ParticipationStatus.ACTIVE.value
        ).first()
        if not model:
            return None
        return self._to_domain(model)
