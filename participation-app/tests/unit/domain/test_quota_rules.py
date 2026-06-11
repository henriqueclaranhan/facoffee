import pytest
from app.domain.models.quota import ParticipationQuota, QuotaCondition, QuotaItems, ParticipationQuotaStatus
from app.domain.exceptions.quota import InvalidQuotaDataException
from datetime import datetime

def test_create_valid_quota():
    # Should not raise exception
    quota = ParticipationQuota(
        id="q_123",
        name="Valid Quota",
        condition=QuotaCondition.DAILY,
        items=QuotaItems.ALL,
        amount=50.0,
        status=ParticipationQuotaStatus.ACTIVE,
        createdBy="manager_1",
        createdAt=datetime.utcnow()
    )
    assert quota.amount == 50.0

def test_quota_invalid_amount():
    with pytest.raises(InvalidQuotaDataException) as excinfo:
        ParticipationQuota(
            id="q_123",
            name="Invalid Quota",
            condition=QuotaCondition.DAILY,
            items=QuotaItems.ALL,
            amount=-10.0,
            status=ParticipationQuotaStatus.ACTIVE,
            createdBy="manager_1",
            createdAt=datetime.utcnow()
        )
    assert "Quota amount cannot be negative." in str(excinfo.value)
