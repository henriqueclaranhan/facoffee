from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.infrastructure.database.database import get_db
from app.infrastructure.database.repositories.sqlalchemy_quota_repository import SQLAlchemyQuotaRepository
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
    page: int = Query(0, ge=0, description="Número da página (inicia em 0)"),
    size: int = Query(20, ge=1, le=100, description="Quantidade de itens por página"),
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    repository = SQLAlchemyQuotaRepository(db)
    use_case = ListQuotasUseCase(repository)
    
    return use_case.execute(page=page, size=size)
