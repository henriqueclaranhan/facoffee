import pytest
from datetime import datetime
from app.domain.models.quota import ParticipationQuota, QuotaCondition, QuotaItems, ParticipationQuotaStatus
from app.domain.exceptions.quota import InvalidQuotaDataException

def test_create_valid_quota():
    quota = ParticipationQuota(
        id="quota_1",
        name="Valid Quota",
        condition=QuotaCondition.DAILY,
        items=QuotaItems.ALL,
        amount=50.0,
        status=ParticipationQuotaStatus.ACTIVE,
        createdBy="manager_1",
        createdAt=datetime.utcnow()
    )
    assert quota.id == "quota_1"
    assert quota.amount == 50.0

def test_create_quota_with_negative_amount_should_fail():
    with pytest.raises(InvalidQuotaDataException):
        ParticipationQuota(
            id="quota_2",
            name="Invalid Quota",
            condition=QuotaCondition.DAILY,
            items=QuotaItems.ALL,
            amount=-10.0,
            status=ParticipationQuotaStatus.ACTIVE,
            createdBy="manager_1",
            createdAt=datetime.utcnow()
        )
