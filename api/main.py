"""
Main API Entry Point
--------------------
Initializes the FastAPI application, configures CORS, and registers 
all versioned route routers.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from api.core.config import settings
from api.routes import router as movies_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

def create_app() -> FastAPI:
    """
    Application factory for the Movie Analytics Platform.

    This function initializes the FastAPI instance, configures global 
    middlewares (CORS), and attaches the versioned API routers.

    Returns:
        FastAPI: A fully configured FastAPI application instance.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="A professional Movie Analytics Platform REST API",
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS Configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include Routers
    app.include_router(movies_router, prefix=settings.API_V1_STR)

    @app.get("/", tags=["Health"])
    def health_check():
        """
        Public health check endpoint to verify API availability.

        Returns:
            dict: JSON object containing status and version information.
        """
        return {
            "status": "online",
            "message": f"{settings.PROJECT_NAME} API is running",
            "version": settings.VERSION
        }

    return app

app = create_app()