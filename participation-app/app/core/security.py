from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import List, Optional
from pydantic import BaseModel

security = HTTPBearer()

class AuthenticatedUser(BaseModel):
    id: str
    email: Optional[str] = None
    roles: List[str] = []

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> AuthenticatedUser:
        decoded_user = get_authenticated_user(credentials)
        
        has_role = any(role in decoded_user.roles for role in self.allowed_roles)
        if not has_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário autenticado não possui permissão para acessar este recurso."
            )
        return decoded_user

def get_authenticated_user(credentials: HTTPAuthorizationCredentials) -> AuthenticatedUser:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        
        user_id = payload.get("sub") or payload.get("preferred_username") or payload.get("email")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: identificador do usuário ausente."
            )
            
        email = payload.get("email")

        roles = payload.get("roles", [])
        if not roles and "realm_access" in payload:
            roles = payload["realm_access"].get("roles", [])
            
        return AuthenticatedUser(
            id=user_id,
            email=email,
            roles=roles
        )
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido ou expirado: {str(e)}"
        )

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> AuthenticatedUser:
    return get_authenticated_user(credentials)

require_manager = RoleChecker(["MANAGER"])
require_participant = RoleChecker(["PARTICIPANT"])
