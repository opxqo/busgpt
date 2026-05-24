import logging
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import text

from app.config import settings
from app.routers import admin, analytics, auth, users, rides, orders
from app.database import async_engine, init_db

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("busgpt.startup")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("BusGPT backend startup begins")
        logger.info("Deployment diagnostics: %s", settings.deployment_diagnostics())
        logger.info("Validating security settings")
        settings.validate_security_settings()
        logger.info("Security settings validated")
        logger.info("Running database initialization on startup")
        init_db()
        logger.info("Database initialization completed")
    except Exception:
        logger.exception("BusGPT backend failed during startup")
        raise

    try:
        yield
    finally:
        logger.info("BusGPT backend shutdown begins")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception):
    logging.exception("Unhandled API error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "服务器开小差了，请稍后再试"})

# Register routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(rides.router, prefix=settings.API_V1_STR)
app.include_router(orders.router, prefix=settings.API_V1_STR)
app.include_router(analytics.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to BusGPT API", "docs_url": "/docs"}


@app.get(f"{settings.API_V1_STR}/health")
async def health():
    return {
        "status": "ok",
        "project": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
    }


@app.get(f"{settings.API_V1_STR}/health/ready")
async def readiness():
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as exc:
        logger.exception("Readiness check failed")
        return JSONResponse(
            status_code=503,
            content={
                "status": "error",
                "detail": "database_unavailable",
                "error": exc.__class__.__name__,
            },
        )

    return {"status": "ok", "database": "available"}
