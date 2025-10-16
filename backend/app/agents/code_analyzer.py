import google.generativeai as genai
from typing import Dict, List
import logging


class CodeAnalyzerAgent:
    """
    Agent 1: Analyzes code structure, complexity, and patterns
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        self.logger = logging.getLogger(__name__)

    async def analyze_codebase(self, repo_data: Dict) -> Dict:
        """
        Main analysis entry point

        PITFALL: Sending too much code to LLM at once (context limits)
        SOLUTION: Analyze file by file, then synthesize
        """

        # Step 1: Statistical analysis (fast, no LLM needed)
        stats = self._compute_statistics(repo_data)

        # Step 2: Structure analysis
        structure = self._analyze_structure(repo_data)

        # Step 3: Complexity analysis (uses LLM for key files only)
        complexity = await self._analyze_complexity(repo_data)

        # Step 4: Generate insights
        key_insights = await self._generate_insights(stats, structure, complexity)

        return {
            "statistics": stats,
            "structure": structure,
            "complexity": complexity,
            "key_insights": key_insights,
        }

    def _compute_statistics(self, repo_data: Dict) -> Dict:
        """Calculate basic metrics without LLM"""
        total_files = 0
        total_lines = 0
        languages = {}

        def count_recursive(contents):
            nonlocal total_files, total_lines
            for item in contents:
                if item["type"] == "file":
                    total_files += 1
                    # Estimate lines (actual count would require fetching content)
                    total_lines += item.get("size", 0) // 50  # Rough estimate
                    ext = item["name"].split(".")[-1] if "." in item["name"] else "other"
                    languages[ext] = languages.get(ext, 0) + 1
                elif item["type"] == "directory":
                    count_recursive(item.get("children", []))

        count_recursive(repo_data.get("contents", []))

        return {
            "total_files": total_files,
            "estimated_lines": total_lines,
            "languages": languages,
            "primary_language": repo_data.get("language", "Unknown"),
        }

    def _analyze_structure(self, repo_data: Dict) -> Dict:
        """
        Identify project structure patterns

        PITFALL: Assuming all projects follow standard conventions
        SOLUTION: Look for common patterns but don't force categorization
        """
        contents = repo_data.get("contents", [])

        # Common patterns
        has_tests = any(
            "test" in item["name"].lower()
            for item in contents
            if item["type"] == "directory"
        )
        has_docs = any(
            "doc" in item["name"].lower()
            for item in contents
            if item["type"] == "directory"
        )
        has_config = any(
            item["name"]
            in [
                "package.json",
                "requirements.txt",
                "Cargo.toml",
                "go.mod",
                "setup.py",
                "pyproject.toml",
            ]
            for item in contents
            if item["type"] == "file"
        )

        # Identify framework (React, Django, etc.)
        framework = self._detect_framework(contents)

        return {
            "has_tests": has_tests,
            "has_documentation": has_docs,
            "has_config_files": has_config,
            "detected_framework": framework,
            "project_type": self._infer_project_type(contents, framework),
        }

    def _detect_framework(self, contents: List[Dict]) -> str:
        """Detect web framework or project type"""
        filenames = [item["name"] for item in contents if item["type"] == "file"]

        if "package.json" in filenames:
            return "Node.js/JavaScript"
        elif "requirements.txt" in filenames or "setup.py" in filenames:
            return "Python"
        elif "Cargo.toml" in filenames:
            return "Rust"
        elif "go.mod" in filenames:
            return "Go"
        elif "pom.xml" in filenames:
            return "Java/Maven"
        else:
            return "Unknown"

    def _infer_project_type(self, contents: List[Dict], framework: str) -> str:
        """Guess project type (web app, library, CLI tool, etc.)"""
        dir_names = [
            item["name"].lower() for item in contents if item["type"] == "directory"
        ]

        if "src" in dir_names or "app" in dir_names:
            if "public" in dir_names or "static" in dir_names:
                return "Web Application"
            return "Application"
        elif "lib" in dir_names:
            return "Library"
        else:
            return "Unknown"

    async def _analyze_complexity(self, repo_data: Dict) -> Dict:
        """
        Use LLM to assess code complexity

        PITFALL: Gemini has token limits (~30k input tokens for gemini-pro)
        SOLUTION: Sample only key files (README, main entry points)
        """
        readme_content = repo_data.get("readme")

        if readme_content:
            # Truncate to avoid token limits
            truncated_readme = readme_content[:3000]

            prompt = f"""
Analyze this project's README and assess its complexity level:

{truncated_readme}

Provide a JSON response with:
1. complexity_level: "Beginner", "Intermediate", or "Advanced"
2. key_technologies: List of main technologies mentioned
3. main_purpose: Brief description of project purpose
4. target_audience: Who would use this project

Format your response as valid JSON only, no markdown.
"""

            try:
                response = await self.model.generate_content_async(prompt)
                return {"complexity_analysis": response.text}
            except Exception as e:
                self.logger.error(f"Error analyzing complexity: {str(e)}")
                return {"complexity_analysis": f"Error: {str(e)}"}

        return {"complexity_analysis": "Unable to determine - no README found"}

    async def _generate_insights(
        self, stats: Dict, structure: Dict, complexity: Dict
    ) -> List[str]:
        """Synthesize findings into key insights"""
        insights = []

        if stats["total_files"] > 100:
            insights.append(
                "Large codebase - documentation should focus on high-level architecture"
            )
        elif stats["total_files"] < 10:
            insights.append("Small project - documentation can cover all components in detail")

        if not structure["has_tests"]:
            insights.append(
                "No test directory detected - documentation should emphasize testing approach"
            )

        if not structure["has_documentation"]:
            insights.append(
                "No existing docs directory - this will be the primary documentation"
            )

        if structure["detected_framework"] != "Unknown":
            insights.append(
                f"Framework detected: {structure['detected_framework']} - leverage framework conventions"
            )

        return insights
