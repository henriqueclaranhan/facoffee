import pytest
from datetime import datetime
from app.domain.models.participation import Participation, ParticipationStatus
from app.domain.exceptions.participation import InvalidParticipationDataException

def test_create_valid_participation():
    participation = Participation(
        id="part_1",
        userId="user_1",
        quotaId="quota_1",
        startCycle="2026-05",
        status=ParticipationStatus.ACTIVE,
        createdAt=datetime.utcnow(),
        quotaSnapshot={"name": "Test Quota", "amount": 50.0}
    )
    assert participation.id == "part_1"
    assert participation.status == ParticipationStatus.ACTIVE
