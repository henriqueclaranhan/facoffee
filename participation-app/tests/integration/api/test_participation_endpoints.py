import pytest
from app.domain.models.quota import ParticipationQuota, QuotaCondition, QuotaItems, ParticipationQuotaStatus
from app.domain.models.participation import Participation, ParticipationStatus
from datetime import datetime

def test_join_quota_success(client, override_user, db_session):
    # Setup Quota
    quota = ParticipationQuota.create(
        name="Test Quota",
        condition=QuotaCondition.DAILY,
        items=QuotaItems.ALL,
        amount=10.0,
        createdBy="manager_1",
        active=True
    )
    
    from app.infrastructure.database.models import QuotaModel
    quota_model = QuotaModel(
        id=quota.id,
        name=quota.name,
        condition=quota.condition.value,
        items=quota.items.value,
        amount=quota.amount,
        status=quota.status.value,
        created_by=quota.createdBy,
        created_at=quota.createdAt
    )
    db_session.add(quota_model)
    db_session.commit()

    # Act
    response = client.post(
        "/api/participation/participations",
        json={"quotaId": quota.id},
        headers={"Authorization": "Bearer mocked"}
    )
    
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["quotaId"] == quota.id
    assert data["status"] == "ACTIVE"
    assert "id" in data

def test_join_quota_already_active(client, override_user, db_session):
    # Setup Quota
    quota = ParticipationQuota.create(
        name="Test Quota 2",
        condition=QuotaCondition.DAILY,
        items=QuotaItems.ALL,
        amount=10.0,
        createdBy="manager_1",
        active=True
    )
    
    from app.infrastructure.database.models import QuotaModel, ParticipationModel
    quota_model = QuotaModel(
        id=quota.id,
        name=quota.name,
        condition=quota.condition.value,
        items=quota.items.value,
        amount=quota.amount,
        status=quota.status.value,
        created_by=quota.createdBy,
        created_at=quota.createdAt
    )
    db_session.add(quota_model)
    
    # Setup active participation
    part_model = ParticipationModel(
        id="part_123",
        user_id="user_1",
        quota_id=quota.id,
        status="ACTIVE",
        joined_at=datetime.utcnow()
    )
    db_session.add(part_model)
    db_session.commit()

    # Act
    response = client.post(
        "/api/participation/participations",
        json={"quotaId": quota.id},
        headers={"Authorization": "Bearer mocked"}
    )
    
    # Assert
    assert response.status_code == 400
    assert "User already has an active participation" in response.json()["message"]

def test_list_quotas_with_filter(client, override_user, db_session):
    from app.infrastructure.database.models import QuotaModel
    q1 = QuotaModel(id="q1", name="Q1", condition="DAILY", items="ALL", amount=10.0, status="ACTIVE", created_by="m1")
    q2 = QuotaModel(id="q2", name="Q2", condition="DAILY", items="ALL", amount=10.0, status="INACTIVE", created_by="m1")
    db_session.add_all([q1, q2])
    db_session.commit()
    
    response = client.get("/api/participation/quotaslist?status=ACTIVE")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == "q1"

def test_cancel_participation_unauthorized(client, override_user, db_session):
    from app.infrastructure.database.models import ParticipationModel, QuotaModel
    q1 = QuotaModel(id="q1", name="Q1", condition="DAILY", items="ALL", amount=10.0, status="ACTIVE", created_by="m1")
    p1 = ParticipationModel(id="p1", user_id="other_user", quota_id="q1", status="ACTIVE")
    db_session.add_all([q1, p1])
    db_session.commit()
    
    response = client.patch("/api/participation/participations/p1/cancel", json={"reason": "test"})
    assert response.status_code == 403
    assert "not authorized" in response.json()["message"]
