from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router as movies_router


app = FastAPI(
    title="Movie Analytics Platform",
    description="REST API for movie analytics using Pandas and FastAPI",
    version="1.0.0",
)


# -------------------------------------------------------------------
# CORS Configuration
# -------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------------
# Routers
# -------------------------------------------------------------------

app.include_router(movies_router)


# -------------------------------------------------------------------
# Health Check
# -------------------------------------------------------------------

@app.get("/")
def health_check():
    return {"status": "Movie Analytics API is running"}