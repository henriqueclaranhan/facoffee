from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from app.domain.models.quota import (
    ParticipationQuota,
    QuotaCondition,
    QuotaItems,
    ParticipationQuotaStatus
)
from app.domain.repositories.quota_repository import QuotaRepository
from app.infrastructure.database.models import QuotaModel

class SQLAlchemyQuotaRepository(QuotaRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: QuotaModel) -> ParticipationQuota:
        return ParticipationQuota(
            id=model.id,
            name=model.name,
            condition=QuotaCondition(model.condition),
            items=QuotaItems(model.items),
            amount=model.amount,
            status=ParticipationQuotaStatus(model.status),
            createdBy=model.created_by,
            createdAt=model.created_at,
            description=model.description,
            updatedAt=model.updated_at
        )

    def _to_model(self, domain: ParticipationQuota) -> QuotaModel:
        return QuotaModel(
            id=domain.id,
            name=domain.name,
            description=domain.description,
            condition=domain.condition.value,
            items=domain.items.value,
            amount=domain.amount,
            status=domain.status.value,
            created_by=domain.createdBy,
            created_at=domain.createdAt,
            updated_at=domain.updatedAt
        )

    def save(self, quota: ParticipationQuota) -> ParticipationQuota:
        existing_model = self.db.query(QuotaModel).filter(QuotaModel.id == quota.id).first()
        
        model = self._to_model(quota)
        if existing_model:
            existing_model.name = model.name
            existing_model.description = model.description
            existing_model.condition = model.condition
            existing_model.items = model.items
            existing_model.amount = model.amount
            existing_model.status = model.status
            existing_model.updated_at = model.updated_at
            db_model = existing_model
        else:
            self.db.add(model)
            db_model = model
            
        self.db.commit()
        self.db.refresh(db_model)
        return self._to_domain(db_model)

    def find_all(self, offset: int, limit: int, active: Optional[bool] = None, condition: Optional[str] = None, items: Optional[str] = None) -> Tuple[List[ParticipationQuota], int]:
        query = self.db.query(QuotaModel)
        if active is not None:
            status_val = "ACTIVE" if active else "INACTIVE"
            query = query.filter(QuotaModel.status == status_val)
        if condition:
            query = query.filter(QuotaModel.condition == condition)
        if items:
            query = query.filter(QuotaModel.items == items)
            
        total_elements = query.count()
        models = query.offset(offset).limit(limit).all()
        return [self._to_domain(m) for m in models], total_elements

    def find_by_id(self, quota_id: str) -> Optional[ParticipationQuota]:
        model = self.db.query(QuotaModel).filter(QuotaModel.id == quota_id).first()
        if not model:
            return None
        return self._to_domain(model)
