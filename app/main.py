from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import auth, problems, progress, curriculum
from app.db.base import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["Authentication"]
)

app.include_router(
    problems.router,
    prefix=f"{settings.API_V1_STR}/problems",
    tags=["Problems"]
)

app.include_router(
    progress.router,
    prefix=f"{settings.API_V1_STR}/progress",
    tags=["Progress"]
)

app.include_router(
    curriculum.router,
    prefix=f"{settings.API_V1_STR}/curriculum",
    tags=["Curriculum"]
)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Math Tutor API"}

# For debugging purposes, include a file for running the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)