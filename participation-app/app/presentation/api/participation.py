from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from app.infrastructure.database.database import get_db
from app.infrastructure.database.repositories.sqlalchemy_participation_repository import SQLAlchemyParticipationRepository
from app.infrastructure.database.repositories.sqlalchemy_quota_repository import SQLAlchemyQuotaRepository
from app.application.use_cases.join_participation import JoinParticipationUseCase
from app.application.use_cases.list_participations import ListParticipationsUseCase
from app.application.use_cases.get_participation import GetParticipationUseCase
from app.application.use_cases.cancel_participation import CancelParticipationUseCase
from app.application.dtos.participation import (
    JoinParticipationQuotaRequest,
    CancelParticipationRequest,
    ParticipationResponse,
    ParticipationPageResponse
)
from app.core.security import AuthenticatedUser, get_current_user, require_participant

router = APIRouter(prefix="/api/participation", tags=["Participation"])


@router.post(
    "/participations",
    response_model=ParticipationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Aderir a uma cota de participação"
)
def join_participation(
    request: JoinParticipationQuotaRequest,
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(require_participant)
):
    part_repo = SQLAlchemyParticipationRepository(db)
    quota_repo = SQLAlchemyQuotaRepository(db)
    use_case = JoinParticipationUseCase(part_repo, quota_repo)
    return use_case.execute(request)


@router.get(
    "/participations",
    response_model=ParticipationPageResponse,
    status_code=status.HTTP_200_OK,
    summary="Listar participações"
)
def list_participations(
    userId: Optional[str] = Query(None),
    quotaId: Optional[str] = Query(None),
    participation_status: Optional[str] = Query(None, alias="status"),
    cycle: Optional[str] = Query(None),
    page: int = Query(0, ge=0),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    repository = SQLAlchemyParticipationRepository(db)
    use_case = ListParticipationsUseCase(repository)
    return use_case.execute(page=page, size=size, user_id=userId, quota_id=quotaId, status=participation_status, cycle=cycle)


@router.get(
    "/participations/{participationId}",
    response_model=ParticipationResponse,
    status_code=status.HTTP_200_OK,
    summary="Obter participação por identificador"
)
def get_participation(
    participationId: str,
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    repository = SQLAlchemyParticipationRepository(db)
    use_case = GetParticipationUseCase(repository)
    return use_case.execute(participationId)


@router.patch(
    "/participations/{participationId}",
    response_model=ParticipationResponse,
    status_code=status.HTTP_200_OK,
    summary="Cancelar participação"
)
def cancel_participation(
    participationId: str,
    request: CancelParticipationRequest,
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    repository = SQLAlchemyParticipationRepository(db)
    use_case = CancelParticipationUseCase(repository)
    return use_case.execute(participationId, request)
