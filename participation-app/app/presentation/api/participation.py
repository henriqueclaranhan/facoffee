from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.infrastructure.database.database import get_db
from app.infrastructure.database.repositories.sqlalchemy_participation_repository import SQLAlchemyParticipationRepository
from app.infrastructure.database.repositories.sqlalchemy_quota_repository import SQLAlchemyQuotaRepository
from app.infrastructure.database.repositories.sqlalchemy_outbox_repository import SQLAlchemyOutboxRepository

from app.application.use_cases.join_quota import JoinQuotaUseCase
from app.application.use_cases.list_participations import ListParticipationsUseCase
from app.application.use_cases.get_participation import GetParticipationUseCase
from app.application.use_cases.cancel_participation import CancelParticipationUseCase

from app.application.dtos.participation import (
    JoinParticipationQuotaRequest,
    CancelParticipationRequest,
    ParticipationResponse,
    ParticipationPageResponse
)
from app.core.security import AuthenticatedUser, get_current_user
from app.domain.exceptions.participation import ActiveParticipationExistsError, QuotaNotActiveError, ParticipationNotFoundError, InvalidParticipationStateError, ParticipationAuthorizationError
from app.domain.exceptions.quota import QuotaNotFoundError

router = APIRouter(prefix="/api/participation", tags=["Participation"])

@router.post(
    "/participations",
    response_model=ParticipationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Aderir a uma cota de participação"
)
def join_quota(
    request: JoinParticipationQuotaRequest,
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    participation_repo = SQLAlchemyParticipationRepository(db)
    quota_repo = SQLAlchemyQuotaRepository(db)
    outbox_repo = SQLAlchemyOutboxRepository(db)
    use_case = JoinQuotaUseCase(participation_repo, quota_repo, outbox_repo)
    
    try:
        participation = use_case.execute(user_id=current_user.id, quota_id=request.quotaId)
        return ParticipationResponse.from_domain(participation)
    except QuotaNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (QuotaNotActiveError, ActiveParticipationExistsError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get(
    "/participations",
    response_model=ParticipationPageResponse,
    status_code=status.HTTP_200_OK,
    summary="Listar adesões"
)
def list_participations(
    page: int = Query(0, ge=0),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    repo = SQLAlchemyParticipationRepository(db)
    use_case = ListParticipationsUseCase(repo)
    
    return use_case.execute(page=page, size=size)

@router.get(
    "/participations/{participation_id}",
    response_model=ParticipationResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar adesão por ID"
)
def get_participation_by_id(
    participation_id: str,
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    repo = SQLAlchemyParticipationRepository(db)
    use_case = GetParticipationUseCase(repo)
    
    try:
        participation = use_case.execute(participation_id)
        return ParticipationResponse.from_domain(participation)
    except ParticipationNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.patch(
    "/participations/{participation_id}/cancel",
    response_model=ParticipationResponse,
    status_code=status.HTTP_200_OK,
    summary="Cancelar adesão"
)
def cancel_participation(
    participation_id: str,
    request: CancelParticipationRequest,
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    repo = SQLAlchemyParticipationRepository(db)
    outbox_repo = SQLAlchemyOutboxRepository(db)
    use_case = CancelParticipationUseCase(repo, outbox_repo)
    
    try:
        is_manager = "MANAGER" in current_user.roles
        participation = use_case.execute(participation_id, request, current_user.id, is_manager)
        return ParticipationResponse.from_domain(participation)
    except ParticipationNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidParticipationStateError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ParticipationAuthorizationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
