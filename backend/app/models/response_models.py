from pydantic import BaseModel
from typing import Dict, Optional


class DocumentationResponse(BaseModel):
    success: bool
    repo_name: str
    documentation: Dict[str, str]  # {beginner: str, intermediate: str, advanced: str}
    metadata: Optional[Dict] = None
