import uuid
import json
from datetime import datetime
from app.domain.models.quota import ParticipationQuota
from app.domain.models.participation import Participation
from app.domain.models.outbox import OutboxEvent
from app.domain.repositories.outbox_repository import OutboxRepository

class EventPublisher:
    @staticmethod
    def _create_base_event(event_type: str, source: str) -> dict:
        return {
            "eventId": str(uuid.uuid4()),
            "eventType": event_type,
            "source": source,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    @staticmethod
    def publish_quota_created(quota: ParticipationQuota, outbox_repository: OutboxRepository):
        event_data = EventPublisher._create_base_event("QuotaCreated", "participation-service")
        event_data["payload"] = {
            "quotaId": quota.id,
            "name": quota.name,
            "amount": quota.amount,
            "status": quota.status.value
        }
        outbox_event = OutboxEvent(
            event_type="quota.created",
            payload=json.dumps(event_data)
        )
        outbox_repository.save(outbox_event)

    @staticmethod
    def publish_quota_updated(quota: ParticipationQuota, outbox_repository: OutboxRepository):
        event_data = EventPublisher._create_base_event("QuotaUpdated", "participation-service")
        event_data["payload"] = {
            "quotaId": quota.id,
            "status": quota.status.value
        }
        outbox_event = OutboxEvent(
            event_type="quota.updated",
            payload=json.dumps(event_data)
        )
        outbox_repository.save(outbox_event)

    @staticmethod
    def publish_participation_created(participation: Participation, outbox_repository: OutboxRepository):
        event_data = EventPublisher._create_base_event("ParticipationCreated", "participation-service")
        event_data["payload"] = {
            "participationId": participation.id,
            "userId": participation.userId,
            "quotaId": participation.quotaId,
            "type": "MONTHLY_PARTICIPATION",
            "status": participation.status.value
        }
        outbox_event = OutboxEvent(
            event_type="participation.created",
            payload=json.dumps(event_data)
        )
        outbox_repository.save(outbox_event)

    @staticmethod
    def publish_participation_cancelled(participation: Participation, outbox_repository: OutboxRepository):
        event_data = EventPublisher._create_base_event("ParticipationCancelled", "participation-service")
        event_data["payload"] = {
            "participationId": participation.id,
            "userId": participation.userId,
            "quotaId": participation.quotaId,
            "status": participation.status.value
        }
        outbox_event = OutboxEvent(
            event_type="participation.cancelled",
            payload=json.dumps(event_data)
        )
        outbox_repository.save(outbox_event)
