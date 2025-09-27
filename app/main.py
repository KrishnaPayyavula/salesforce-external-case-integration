"""Main FastAPI application for Salesforce External Case Integration."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import uvicorn
from contextlib import asynccontextmanager

from app.config import settings
from app.api import salesforce, mock


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")
    yield
    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    Salesforce External Case Integration API
    
    This API provides endpoints for:
    - Creating cases in Salesforce using OAuth 2.0 authentication
    - Retrieving case details from Salesforce
    - Mock external service for product information
    
    ## Authentication
    The API uses OAuth 2.0 Client Credentials flow to authenticate with Salesforce.
    Configure your credentials in the .env file.
    
    ## Case Management
    Create and retrieve cases in Salesforce with support for custom fields and standard properties.
    
    ## Mock Product Service
    Simulates an external service that provides detailed product information based on case details.
    """,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "detail": str(exc) if settings.debug else "Internal server error"
        }
    )


# Include API routers
app.include_router(salesforce.router)
app.include_router(mock.router)


@app.get("/")
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        Dict: Basic API information and available endpoints
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "salesforce": "/api/salesforce",
            "mock": "/api/mock",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """
    Global health check endpoint.
    
    Returns:
        Dict: Overall API health status
    """
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "message": "API is running correctly"
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
