import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.metrics import router as metrics_router
from app.api.router import api_router
from app.api.websocket import router as ws_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.database import close_db, get_db
from app.services.activity import seed_demo_activity
from app.services.event_bus import subscribe
from app.services.metrics import request_latency
from app.services.scheduler import start_scheduler, stop_scheduler
from app.services.ws_manager import manager

setup_logging(settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_db()
    await seed_demo_activity()
    subscribe(manager.handle_event)
    # Load plugins
    from app.plugins.loader import load_plugins
    load_plugins()
    # Setup OpenTelemetry if enabled
    from app.core.telemetry import setup_telemetry
    setup_telemetry(app)
    await start_scheduler(interval=settings.scan_interval)
    yield
    await stop_scheduler()
    await close_db()


app = FastAPI(
    title=settings.app_name,
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.middleware("http")
async def track_request_latency(request: Request, call_next):
    """Record request latency for Prometheus."""
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    # Skip metrics endpoint to avoid recursion
    if request.url.path != "/metrics":
        endpoint = request.url.path.split("?")[0]
        request_latency.labels(
            method=request.method,
            endpoint=endpoint,
            status_code=str(response.status_code),
        ).observe(duration)
    return response


app.include_router(api_router)
app.include_router(metrics_router)
app.include_router(ws_router)
