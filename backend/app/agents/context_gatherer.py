import google.generativeai as genai
from typing import Dict, List
import logging


class ContextGathererAgent:
    """
    Agent 2: Gathers external context about the project
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        self.logger = logging.getLogger(__name__)

    async def gather_context(self, repo_data: Dict, analysis: Dict) -> Dict:
        """
        Gather relevant context from external sources

        PITFALL: External APIs may be slow or unavailable
        SOLUTION: Set timeouts and have fallback content
        """

        context = {
            "documentation_standards": await self._get_doc_standards(analysis),
            "best_practices": await self._get_best_practices(repo_data, analysis),
        }

        return context

    async def _get_doc_standards(self, analysis: Dict) -> Dict:
        """
        Get documentation standards for detected framework/language

        PITFALL: Hard-coding standards quickly becomes outdated
        SOLUTION: Use LLM to generate current best practices
        """
        framework = analysis.get("structure", {}).get("detected_framework", "Unknown")

        prompt = f"""
What are the current documentation best practices for {framework} projects?

Include:
1. Standard sections (Installation, Usage, API Reference, etc.)
2. Common formatting conventions
3. Beginner-friendly explanation approaches

Keep response concise (under 500 words).
"""

        try:
            response = await self.model.generate_content_async(prompt)
            return {"standards": response.text}
        except Exception as e:
            self.logger.error(f"Error getting doc standards: {str(e)}")
            return {"standards": f"Using default standards due to error: {str(e)}"}

    async def _get_best_practices(self, repo_data: Dict, analysis: Dict) -> Dict:
        """
        Get language-specific best practices

        PITFALL: Generic advice isn't helpful
        SOLUTION: Tailor to specific project characteristics
        """
        language = repo_data.get("language", "Unknown")
        project_type = analysis.get("structure", {}).get("project_type", "Unknown")

        prompt = f"""
For a {project_type} written in {language}, what should documentation emphasize?

Consider:
- Common pain points for users
- Setup complexity
- Integration patterns

Provide 3-5 specific suggestions.
"""

        try:
            response = await self.model.generate_content_async(prompt)
            return {"best_practices": response.text}
        except Exception as e:
            self.logger.error(f"Error getting best practices: {str(e)}")
            return {"best_practices": "Default best practices"}
