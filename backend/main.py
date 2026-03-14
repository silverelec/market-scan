import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import get_settings
from backend.api import market_scan, competitor, casestudy

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info(f"Market Intelligence Platform starting on port {settings.backend_port}")
    logger.info(f"Exa enabled: {settings.exa_enabled}")
    yield
    logger.info("Shutting down")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Market Intelligence Platform",
        description="MBB-quality market research for management consultants",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(market_scan.router, prefix="/api")
    app.include_router(competitor.router, prefix="/api")
    app.include_router(casestudy.router, prefix="/api")

    @app.get("/health")
    async def health():
        return {"status": "ok", "exa_enabled": settings.exa_enabled}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "backend.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.backend_reload,
    )
