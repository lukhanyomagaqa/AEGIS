from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import psycopg
import redis

from aegis.config import Settings, get_settings

router = APIRouter(tags=["health"])


@router.get("/health/live", summary="Check API process liveness")
def liveness() -> dict[str, str]:
    return {"status": "alive"}


@router.get("/health/ready", summary="Check required dependency readiness")
def readiness(settings: Settings = Depends(get_settings)) -> JSONResponse:
    timeout = settings.dependency_timeout_seconds
    database_status = "available"
    try:
        with psycopg.connect(
            settings.database_url,
            connect_timeout=max(1, int(timeout)),
        ) as connection:
            connection.execute("SELECT 1")
    except psycopg.Error:
        database_status = "unavailable"

    redis_status = "available"
    redis_client = None
    try:
        redis_client = redis.Redis.from_url(
            settings.redis_url,
            socket_connect_timeout=timeout,
            socket_timeout=timeout,
            decode_responses=True,
        )
        redis_client.ping()
    except (redis.RedisError, ValueError):
        redis_status = "unavailable"
    finally:
        if redis_client is not None:
            redis_client.close()

    ready = database_status == "available" and (
        redis_status == "available" or not settings.redis_required
    )
    return JSONResponse(
        status_code=200 if ready else 503,
        content={
            "status": "ready" if ready else "not_ready",
            "dependencies": {
                "database": database_status,
                "redis": redis_status,
            },
        },
    )
