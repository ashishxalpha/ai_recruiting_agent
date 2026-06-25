from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.presentation.api.v1.api_router import api_router
from src.observability.logging import setup_logging
from src.observability.tracing import setup_tracing
from src.observability.metrics import setup_metrics

import logging
logger = logging.getLogger(__name__)

# Initialize observability
setup_logging()
setup_tracing()
setup_metrics()

app = FastAPI(
    title="AI Recruiting Copilot API",
    description="API for Resume Ingestion and AI Candidate Extraction",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
