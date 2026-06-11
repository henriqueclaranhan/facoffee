from sqlalchemy import Column, String, Float, DateTime, Boolean
from datetime import datetime
from app.infrastructure.database.database import Base

class QuotaModel(Base):
    __tablename__ = "participation_quotas"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    condition = Column(String, nullable=False)
    items = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    created_by = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, nullable=True)

class ParticipationModel(Base):
    __tablename__ = "participations"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    quota_id = Column(String, nullable=False, index=True)
    start_cycle = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    quota_snapshot = Column(String, nullable=False)
    effective_cycle = Column(String, nullable=True)
    updated_at = Column(DateTime, nullable=True)
