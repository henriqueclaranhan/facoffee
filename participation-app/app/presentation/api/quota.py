from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.infrastructure.database.database import get_db
from app.infrastructure.database.repositories.sqlalchemy_quota_repository import SQLAlchemyQuotaRepository
from app.application.use_cases.create_quota import CreateQuotaUseCase
from app.application.use_cases.list_quotas import ListQuotasUseCase
from app.application.use_cases.get_quota import GetQuotaUseCase
from app.application.use_cases.update_quota import UpdateQuotaUseCase
from app.application.use_cases.deactivate_quota import DeactivateQuotaUseCase
from app.application.dtos.quota import (
    CreateParticipationQuotaRequest,
    UpdateParticipationQuotaRequest,
    ParticipationQuotaResponse,
    ParticipationQuotaPageResponse
)
from app.core.security import RoleChecker, AuthenticatedUser, get_current_user, require_manager
from app.domain.exceptions.quota import InvalidQuotaDataException, QuotaNotFoundException, QuotaConflictException

router = APIRouter(prefix="/api/participation", tags=["Participation"])

@router.post(
    "/quotas",
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
    use_case = CreateQuotaUseCase(repository)
    
    try:
        return use_case.execute(request, manager_id=manager.id)
    except InvalidQuotaDataException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/quotas",
    response_model=ParticipationQuotaPageResponse,
    status_code=status.HTTP_200_OK,
    summary="Listar cotas de participação",
    description="Lista cotas de participação com paginação. Sem filtros por enquanto."
)
def list_quotas(
    active: Optional[bool] = Query(None),
    condition: Optional[str] = Query(None),
    items: Optional[str] = Query(None),
    page: int = Query(0, ge=0, description="Número da página (inicia em 0)"),
    size: int = Query(20, ge=1, le=100, description="Quantidade de itens por página"),
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    repository = SQLAlchemyQuotaRepository(db)
    use_case = ListQuotasUseCase(repository)
    
    return use_case.execute(page=page, size=size, active=active, condition=condition, items=items)

@router.get(
    "/quotas/{quotaId}",
    response_model=ParticipationQuotaResponse,
    status_code=status.HTTP_200_OK,
    summary="Obter cota de participação por identificador",
    description="Retorna os dados completos de uma cota de participação pelo identificador."
)
def get_quota(
    quotaId: str,
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    repository = SQLAlchemyQuotaRepository(db)
    use_case = GetQuotaUseCase(repository)
    return use_case.execute(quotaId)

@router.patch(
    "/quotas/{quotaId}",
    response_model=ParticipationQuotaResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualizar cota de participação"
)
def update_quota(
    quotaId: str,
    request: UpdateParticipationQuotaRequest,
    db: Session = Depends(get_db),
    manager: AuthenticatedUser = Depends(require_manager)
):
    repository = SQLAlchemyQuotaRepository(db)
    use_case = UpdateQuotaUseCase(repository)
    return use_case.execute(quotaId, request)

@router.delete(
    "/quotas/{quotaId}",
    response_model=ParticipationQuotaResponse,
    status_code=status.HTTP_200_OK,
    summary="Desativar cota de participação (soft delete)"
)
def deactivate_quota(
    quotaId: str,
    db: Session = Depends(get_db),
    manager: AuthenticatedUser = Depends(require_manager)
):
    repository = SQLAlchemyQuotaRepository(db)
    use_case = DeactivateQuotaUseCase(repository)
    return use_case.execute(quotaId)
