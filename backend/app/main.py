from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import documentation
from .config import get_settings
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="Smart Documentation Agent API",
    description="Multi-agent system for generating adaptive documentation",
    version="1.0.0",
)

settings = get_settings()

# CORS configuration (CRITICAL for local development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documentation.router)


@app.get("/")
async def root():
    return {
        "message": "Smart Documentation Agent API",
        "docs_url": "/docs",
        "health_check": "/api/v1/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.backend_port)
