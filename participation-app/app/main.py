from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from datetime import datetime

from app.infrastructure.database.database import engine, Base
from app.infrastructure.database.models import QuotaModel
from app.presentation.api.quota import router as quota_router
from app.presentation.api.participation import router as participation_router
from app.domain.exceptions.quota import InvalidQuotaDataException

Base.metadata.create_all(bind=engine)

from contextlib import asynccontextmanager
import asyncio
from app.infrastructure.messaging.outbox_worker import process_outbox_events

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(process_outbox_events())
    yield
    task.cancel()

app = FastAPI(
    title="FACOFFE Participation Service",
    version="1.0.0",
    description="Serviço de cotas e adesões de participação para o FACOFFE.",
    lifespan=lifespan
)

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(InvalidQuotaDataException)
async def domain_exception_handler(request: Request, exc: InvalidQuotaDataException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": status.HTTP_400_BAD_REQUEST,
            "error": "Bad Request",
            "message": str(exc),
            "path": request.url.path
        }
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    error_name = "Unauthorized" if exc.status_code == 401 else ("Forbidden" if exc.status_code == 403 else ("Not Found" if exc.status_code == 404 else "Bad Request"))
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": exc.status_code,
            "error": error_name,
            "message": exc.detail,
            "path": request.url.path
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    messages = [f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}" for err in errors]
    message_str = " | ".join(messages)
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": status.HTTP_400_BAD_REQUEST,
            "error": "Bad Request",
            "message": f"Erro de validação dos campos: {message_str}",
            "path": request.url.path
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "error": "Internal Server Error",
            "message": str(exc),
            "path": request.url.path
        }
    )

app.include_router(quota_router)
app.include_router(participation_router)

@app.get("/health", tags=["Health"])
@app.get("/api/participation/health", tags=["Health"])
def health():
    return {"status": "UP", "service": "participation"}
