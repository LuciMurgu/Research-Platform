"""FastAPI application entry point.

This module creates the FastAPI app instance. No routes are registered yet
beyond the root metadata endpoint. No compute, storage, or agent logic here.
"""

from fastapi import FastAPI

from workbench.api.routes_health import router as health_router

app = FastAPI(
    title="Research Workbench",
    description="Local-first scientific visual research platform",
    version="0.0.1",
)

app.include_router(health_router)


@app.get("/")
async def root() -> dict:
    """Return application metadata."""
    return {
        "name": "Research Workbench",
        "version": "0.0.1",
        "status": "skeleton",
    }
