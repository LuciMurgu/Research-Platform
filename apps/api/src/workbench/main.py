"""FastAPI application entry point.

This module creates the FastAPI app instance. No routes are registered yet
beyond the root metadata endpoint. No compute, storage, or agent logic here.
"""

from fastapi import FastAPI

app = FastAPI(
    title="Research Workbench",
    description="Local-first scientific visual research platform",
    version="0.0.1",
)


@app.get("/")
async def root() -> dict:
    """Return application metadata."""
    return {
        "name": "Research Workbench",
        "version": "0.0.1",
        "status": "skeleton",
    }
