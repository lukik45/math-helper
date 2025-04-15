import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from app import __version__
from app.core.config import settings
from app.db.base import init_db
from app.api import auth


# Configure logging
logging.basicConfig(level=logging.INFO)
logger.info(f"Starting AI Math Tutor API v{__version__}")

# Initialize FastAPI app
app = FastAPI(
    title="AI Math Tutor API",
    description="API for AI Math Tutor application connecting problem-solving with curriculum",
    version=__version__,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to AI Math Tutor API",
        "version": __version__,
        "docs_url": "/docs"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": __version__
    }

# Include API routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
# app.include_router(curriculum.router, prefix="/api/curriculum", tags=["Curriculum"])
# app.include_router(problems.router, prefix="/api/problems", tags=["Problems"])
# app.include_router(progress.router, prefix="/api/progress", tags=["Progress"])

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Initializing application...")
    try:
        init_db()
        logger.info("Application startup complete")
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application...")
    # Close any open connections here

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)