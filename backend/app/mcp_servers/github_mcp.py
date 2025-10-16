from github import Github, RateLimitExceededException
from typing import Dict, List, Optional
import logging
import aiohttp


class GitHubMCP:
    """MCP Server for GitHub API interactions"""

    def __init__(self, token: Optional[str] = None):
        self.github = Github(token) if token else Github()
        self.logger = logging.getLogger(__name__)

    async def fetch_repo_structure(self, repo_url: str) -> Dict:
        """
        Fetch repository structure with error handling

        PITFALL: GitHub API rate limits (60/hour without auth, 5000/hour with auth)
        SOLUTION: Implement caching and selective file fetching
        """
        try:
            # Extract owner/repo from URL
            parts = repo_url.rstrip("/").split("/")
            owner, repo_name = parts[-2], parts[-1]

            repo = self.github.get_repo(f"{owner}/{repo_name}")

            # Check rate limit before proceeding
            rate_limit = self.github.get_rate_limit()
            if rate_limit.core.remaining < 10:
                raise Exception(
                    f"GitHub API rate limit low: {rate_limit.core.remaining} remaining"
                )

            # Fetch file tree (limit depth to avoid huge repos)
            contents = self._get_tree_recursive(repo, max_depth=3)

            # Fetch README content if available
            readme_content = await self._fetch_readme(repo)

            return {
                "name": repo.name,
                "description": repo.description or "No description available",
                "language": repo.language or "Unknown",
                "stars": repo.stargazers_count,
                "contents": contents,
                "readme": readme_content,
                "rate_limit_remaining": rate_limit.core.remaining,
            }

        except RateLimitExceededException:
            self.logger.error("GitHub API rate limit exceeded")
            raise Exception(
                "GitHub API rate limit exceeded. Please try again later or add a GitHub token."
            )
        except Exception as e:
            self.logger.error(f"Error fetching repo: {str(e)}")
            raise

    def _get_tree_recursive(
        self, repo, path="", max_depth=3, current_depth=0
    ) -> List[Dict]:
        """
        Recursively get file tree with depth limit

        PITFALL: Large repos can cause timeouts
        SOLUTION: Limit depth and skip binary/large files
        """
        if current_depth >= max_depth:
            return []

        files = []
        try:
            contents = repo.get_contents(path)
            for content in contents:
                if content.type == "dir":
                    files.append(
                        {
                            "name": content.name,
                            "path": content.path,
                            "type": "directory",
                            "children": self._get_tree_recursive(
                                repo, content.path, max_depth, current_depth + 1
                            ),
                        }
                    )
                else:
                    # Skip non-code files and large files
                    if self._is_code_file(content.name) and content.size < 1_000_000:
                        files.append(
                            {
                                "name": content.name,
                                "path": content.path,
                                "type": "file",
                                "size": content.size,
                                "download_url": content.download_url,
                            }
                        )
        except Exception as e:
            self.logger.warning(f"Error accessing path {path}: {str(e)}")

        return files

    def _is_code_file(self, filename: str) -> bool:
        """Filter for code files only"""
        code_extensions = {
            ".py",
            ".js",
            ".jsx",
            ".ts",
            ".tsx",
            ".java",
            ".cpp",
            ".c",
            ".h",
            ".go",
            ".rs",
            ".rb",
            ".php",
            ".swift",
            ".kt",
            ".md",
            ".json",
            ".yaml",
            ".yml",
            ".toml",
        }
        return any(filename.endswith(ext) for ext in code_extensions)

    async def _fetch_readme(self, repo) -> Optional[str]:
        """Fetch README content if it exists"""
        try:
            readme = repo.get_readme()
            # Decode content (it's base64 encoded)
            return readme.decoded_content.decode("utf-8")
        except Exception as e:
            self.logger.info(f"No README found or error fetching: {str(e)}")
            return None

    async def fetch_file_content(self, download_url: str) -> str:
        """
        Fetch individual file content

        PITFALL: Binary files or extremely large files
        SOLUTION: Check content type and size before fetching
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(download_url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    raise Exception(f"Failed to fetch file: {response.status}")
