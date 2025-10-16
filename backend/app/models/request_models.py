from pydantic import BaseModel, Field


class DocumentationRequest(BaseModel):
    repo_url: str = Field(..., description="GitHub repository URL")

    class Config:
        json_schema_extra = {
            "example": {"repo_url": "https://github.com/username/repo-name"}
        }
