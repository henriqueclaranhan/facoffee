from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.infrastructure.database.database import get_db
from app.infrastructure.database.repositories.sqlalchemy_quota_repository import SQLAlchemyQuotaRepository
from app.infrastructure.database.repositories.sqlalchemy_outbox_repository import SQLAlchemyOutboxRepository
from app.application.use_cases.create_quota import CreateQuotaUseCase
from app.application.use_cases.list_quotas import ListQuotasUseCase
from app.application.dtos.quota import (
    CreateParticipationQuotaRequest,
    ParticipationQuotaResponse,
    ParticipationQuotaPageResponse
)
from app.core.security import RoleChecker, AuthenticatedUser, get_current_user, require_manager
from app.domain.exceptions.quota import InvalidQuotaDataException

router = APIRouter(prefix="/api/participation", tags=["Participation"])

@router.post(
    "/createquota",
    response_model=ParticipationQuotaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar cota de participação",
    description="Permite que gestores cadastrem uma cota de participação."
)
def create_quota(
    request: CreateParticipationQuotaRequest,
    db: Session = Depends(get_db),
    manager: AuthenticatedUser = Depends(require_manager)
):
    repository = SQLAlchemyQuotaRepository(db)
    outbox_repo = SQLAlchemyOutboxRepository(db)
    use_case = CreateQuotaUseCase(repository, outbox_repo)
    
    try:
        return use_case.execute(request, manager_id=manager.id)
    except InvalidQuotaDataException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/quotaslist",
    response_model=ParticipationQuotaPageResponse,
    status_code=status.HTTP_200_OK,
    summary="Listar cotas de participação",
    description="Lista cotas de participação com paginação e filtro por status."
)
def list_quotas(
    page: int = Query(0, ge=0, description="Número da página (inicia em 0)"),
    size: int = Query(20, ge=1, le=100, description="Quantidade de itens por página"),
    status: str = Query(None, description="Filtrar por status da cota (ex: ACTIVE, INACTIVE)"),
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    repository = SQLAlchemyQuotaRepository(db)
    use_case = ListQuotasUseCase(repository)
    return use_case.execute(page=page, size=size, status=status)
from app.application.use_cases.get_quota import GetQuotaUseCase
from app.application.use_cases.update_quota import UpdateQuotaUseCase
from app.application.use_cases.deactivate_quota import DeactivateQuotaUseCase
from app.application.dtos.quota import UpdateParticipationQuotaRequest
from app.domain.exceptions.quota import QuotaNotFoundError, InvalidQuotaStateError

@router.get(
    "/quotas/{quota_id}",
    response_model=ParticipationQuotaResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar cota por ID"
)
def get_quota_by_id(
    quota_id: str,
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    repository = SQLAlchemyQuotaRepository(db)
    use_case = GetQuotaUseCase(repository)
    
    try:
        quota = use_case.execute(quota_id)
        return ParticipationQuotaResponse.from_domain(quota)
    except QuotaNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put(
    "/quotas/{quota_id}",
    response_model=ParticipationQuotaResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualizar dados de cota"
)
def update_quota(
    quota_id: str,
    request: UpdateParticipationQuotaRequest,
    db: Session = Depends(get_db),
    manager: AuthenticatedUser = Depends(require_manager)
):
    repository = SQLAlchemyQuotaRepository(db)
    outbox_repo = SQLAlchemyOutboxRepository(db)
    use_case = UpdateQuotaUseCase(repository, outbox_repo)
    
    try:
        quota = use_case.execute(quota_id, request)
        return ParticipationQuotaResponse.from_domain(quota)
    except QuotaNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.patch(
    "/quotas/{quota_id}/deactivate",
    response_model=ParticipationQuotaResponse,
    status_code=status.HTTP_200_OK,
    summary="Inativar cota"
)
def deactivate_quota(
    quota_id: str,
    db: Session = Depends(get_db),
    manager: AuthenticatedUser = Depends(require_manager)
):
    repository = SQLAlchemyQuotaRepository(db)
    outbox_repo = SQLAlchemyOutboxRepository(db)
    use_case = DeactivateQuotaUseCase(repository, outbox_repo)
    
    try:
        quota = use_case.execute(quota_id)
        return ParticipationQuotaResponse.from_domain(quota)
    except QuotaNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidQuotaStateError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
