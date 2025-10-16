import google.generativeai as genai
from typing import Dict
import json
import logging


class DocGeneratorAgent:
    """
    Agent 3: Generates multi-level documentation
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        self.logger = logging.getLogger(__name__)

    async def generate_documentation(
        self, repo_data: Dict, analysis: Dict, context: Dict
    ) -> Dict:
        """
        Generate three levels of documentation

        PITFALL: All three levels sound the same
        SOLUTION: Use distinct prompting strategies for each level
        """

        # Generate all three levels in parallel for speed
        import asyncio

        beginner_task = self._generate_beginner_docs(repo_data, analysis, context)
        intermediate_task = self._generate_intermediate_docs(
            repo_data, analysis, context
        )
        advanced_task = self._generate_advanced_docs(repo_data, analysis, context)

        beginner, intermediate, advanced = await asyncio.gather(
            beginner_task, intermediate_task, advanced_task
        )

        return {
            "beginner": beginner,
            "intermediate": intermediate,
            "advanced": advanced,
        }

    async def _generate_beginner_docs(
        self, repo_data: Dict, analysis: Dict, context: Dict
    ) -> str:
        """
        Beginner-level documentation

        TARGET AUDIENCE: Someone who just discovered this project
        TONE: Friendly, explanatory, assumes minimal background
        STRUCTURE: What/Why/How with lots of examples
        """

        stats = json.dumps(analysis.get("statistics", {}), indent=2)
        insights = "\n".join(analysis.get("key_insights", []))

        prompt = f"""
Create beginner-friendly documentation for this project:

PROJECT INFO:
- Name: {repo_data.get('name')}
- Description: {repo_data.get('description', 'No description provided')}
- Language: {repo_data.get('language')}
- Stars: {repo_data.get('stars', 0)}

PROJECT ANALYSIS:
{stats}

KEY INSIGHTS:
{insights}

REQUIREMENTS FOR BEGINNER DOCS:
1. Start with a clear, simple explanation of what this project does (in 2-3 sentences)
2. Explain WHO would use this and WHY (real-world use cases)
3. Break down installation into numbered steps
4. Provide a "Quick Start" example that works copy-paste
5. Explain key concepts without assuming prior knowledge
6. Use analogies and simple language
7. Include troubleshooting for common issues

TONE: Friendly and encouraging, like explaining to a friend

FORMAT: Use Markdown with clear headers

LENGTH: 500-800 words

IMPORTANT: Avoid jargon. If technical terms are necessary, define them in simple language.
"""

        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            self.logger.error(f"Error generating beginner docs: {str(e)}")
            return f"# Error Generating Beginner Documentation\n\nError: {str(e)}"

    async def _generate_intermediate_docs(
        self, repo_data: Dict, analysis: Dict, context: Dict
    ) -> str:
        """
        Intermediate-level documentation

        TARGET AUDIENCE: Developer with some experience in this domain
        TONE: Professional but accessible
        STRUCTURE: Architecture overview, integration patterns, configuration
        """

        structure = json.dumps(analysis.get("structure", {}), indent=2)

        prompt = f"""
Create intermediate-level documentation for this project:

PROJECT INFO:
- Name: {repo_data.get('name')}
- Language: {repo_data.get('language')}
- Framework: {analysis.get('structure', {}).get('detected_framework', 'Unknown')}

PROJECT STRUCTURE:
{structure}

REQUIREMENTS FOR INTERMEDIATE DOCS:
1. Architecture Overview (how components interact)
2. Key Features and their implementation approach
3. Configuration options and their effects
4. Integration guide (how to use in larger systems)
5. Common workflows and patterns
6. Performance considerations
7. Testing approach

TONE: Professional, assumes familiarity with {repo_data.get('language')}

FORMAT: Use Markdown with code examples

LENGTH: 700-1000 words

IMPORTANT: Focus on "how" and "why", not just "what"
"""

        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            self.logger.error(f"Error generating intermediate docs: {str(e)}")
            return f"# Error Generating Intermediate Documentation\n\nError: {str(e)}"

    async def _generate_advanced_docs(
        self, repo_data: Dict, analysis: Dict, context: Dict
    ) -> str:
        """
        Advanced-level documentation

        TARGET AUDIENCE: Experienced developer or contributor
        TONE: Concise, technical, assumes deep knowledge
        STRUCTURE: Technical reference, edge cases, internals
        """

        complexity = json.dumps(analysis.get("complexity", {}), indent=2)

        prompt = f"""
Create advanced-level technical documentation for this project:

PROJECT INFO:
- Name: {repo_data.get('name')}
- Language: {repo_data.get('language')}

COMPLEXITY ANALYSIS:
{complexity}

REQUIREMENTS FOR ADVANCED DOCS:
1. Technical architecture deep-dive
2. Design decisions and trade-offs
3. Performance optimization opportunities
4. Edge cases and limitations
5. Extension points and customization
6. Contributing guidelines (code structure, testing requirements)
7. Roadmap and known issues

TONE: Concise and technical, assumes expert-level knowledge

FORMAT: Markdown with code examples, avoid excessive explanation

LENGTH: 600-900 words

IMPORTANT: Be precise and technical. Skip basic concepts.
"""

        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            self.logger.error(f"Error generating advanced docs: {str(e)}")
            return f"# Error Generating Advanced Documentation\n\nError: {str(e)}"
