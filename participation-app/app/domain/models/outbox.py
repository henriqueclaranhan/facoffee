from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class OutboxEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    payload: str
    status: str = "PENDING"
    created_at: datetime = Field(default_factory=datetime.utcnow)
