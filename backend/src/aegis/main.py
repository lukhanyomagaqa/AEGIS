import logging
import re
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from aegis.api.routes.health import router as health_router
from aegis.config import get_settings
from aegis.logging import configure_logging, request_id_context

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger("aegis.http")

app = FastAPI(
    title="AEGIS API",
    description="AEGIS platform foundation API",
    version="1.0.0",
    openapi_url=f"{settings.api_prefix}/openapi.json",
    docs_url=f"{settings.api_prefix}/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["Content-Type", "X-Request-ID"],
    expose_headers=["X-Request-ID"],
)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    supplied_id = request.headers.get("X-Request-ID", "")
    request_id = (
        supplied_id
        if re.fullmatch(r"[A-Za-z0-9._-]{1,64}", supplied_id)
        else str(uuid.uuid4())
    )
    token = request_id_context.set(request_id)
    started = time.perf_counter()
    response = None
    try:
        response = await call_next(request)
        return response
    except Exception:
        logger.exception("request_unhandled_error")
        raise
    finally:
        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        logger.info(
            "request_completed",
            extra={
                "method": request.method,
                "status_code": response.status_code if response is not None else 500,
                "duration_ms": duration_ms,
            },
        )
        request_id_context.reset(token)
        if response is not None:
            response.headers["X-Request-ID"] = request_id


app.include_router(health_router, prefix=settings.api_prefix)
