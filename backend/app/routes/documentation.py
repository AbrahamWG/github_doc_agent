from fastapi import APIRouter, HTTPException
from ..models.request_models import DocumentationRequest
from ..models.response_models import DocumentationResponse
from ..agents.orchestrator import AgentOrchestrator
from ..config import get_settings
import logging

router = APIRouter(prefix="/api/v1", tags=["documentation"])
logger = logging.getLogger(__name__)


@router.post("/generate", response_model=DocumentationResponse)
async def generate_documentation(request: DocumentationRequest):
    """
    Generate documentation for a GitHub repository

    PITFALL: Long-running requests can timeout
    SOLUTION: Return immediately with job ID, process in background

    For MVP: Synchronous processing (simpler)
    For Production: Use background tasks or job queue
    """

    settings = get_settings()

    # Validate GitHub URL
    if not request.repo_url.startswith("https://github.com/"):
        raise HTTPException(status_code=400, detail="Invalid GitHub URL")

    try:
        # Initialize orchestrator
        orchestrator = AgentOrchestrator(
            gemini_api_key=settings.gemini_api_key,
            github_token=settings.github_token if settings.github_token else None,
        )

        # Generate documentation
        result = await orchestrator.generate_documentation(request.repo_url)

        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error"))

        return DocumentationResponse(
            success=True,
            repo_name=result["repo_name"],
            documentation=result["documentation"],
            metadata=result.get("metadata"),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating documentation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "smart-docs-agent"}
