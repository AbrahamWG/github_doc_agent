from .code_analyzer import CodeAnalyzerAgent
from .context_gatherer import ContextGathererAgent
from .doc_generator import DocGeneratorAgent
from ..mcp_servers.github_mcp import GitHubMCP
from typing import Dict, Optional
import logging
import asyncio


class AgentOrchestrator:
    """
    Coordinates all three agents and MCP servers

    CRITICAL: This is the "brain" that shows system design thinking
    """

    def __init__(self, gemini_api_key: str, github_token: Optional[str] = None):
        self.logger = logging.getLogger(__name__)

        # Initialize MCP servers
        self.github_mcp = GitHubMCP(github_token)

        # Initialize agents
        self.code_analyzer = CodeAnalyzerAgent(gemini_api_key)
        self.context_gatherer = ContextGathererAgent(gemini_api_key)
        self.doc_generator = DocGeneratorAgent(gemini_api_key)

    async def generate_documentation(self, repo_url: str) -> Dict:
        """
        Main orchestration flow

        DESIGN PRINCIPLE: Sequential dependencies, parallel where possible

        Flow:
        1. Fetch repo data (must be first)
        2. Analyze code (depends on #1)
        3. Gather context (depends on #2)
        4. Generate docs (depends on #2 and #3)

        PITFALL: Sequential execution is slow
        SOLUTION: Steps 2 & 3 can run in parallel after step 1
        """

        try:
            self.logger.info(f"Starting documentation generation for {repo_url}")

            # Step 1: Fetch repository data
            self.logger.info("Fetching repository structure...")
            repo_data = await self.github_mcp.fetch_repo_structure(repo_url)

            # Step 2 & 3: Analyze and gather context in parallel
            self.logger.info("Analyzing code and gathering context...")
            analysis, initial_context = await asyncio.gather(
                self.code_analyzer.analyze_codebase(repo_data),
                self.context_gatherer.gather_context(repo_data, {}),
            )

            # Update context with full analysis
            context = await self.context_gatherer.gather_context(repo_data, analysis)

            # Step 4: Generate documentation
            self.logger.info("Generating multi-level documentation...")
            documentation = await self.doc_generator.generate_documentation(
                repo_data, analysis, context
            )

            self.logger.info("Documentation generation complete!")

            return {
                "success": True,
                "repo_name": repo_data.get("name"),
                "documentation": documentation,
                "metadata": {
                    "analysis": analysis,
                    "rate_limit_remaining": repo_data.get("rate_limit_remaining"),
                },
            }

        except Exception as e:
            self.logger.error(f"Error in documentation generation: {str(e)}")
            return {"success": False, "error": str(e), "documentation": None}
