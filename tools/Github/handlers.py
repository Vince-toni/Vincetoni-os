import os
import httpx

GITHUB_API = "https://api.github.com"


def _headers():
    token = os.getenv("GITHUB_TOKEN")
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }


async def list_repo_issues(owner: str, repo: str, **kwargs):
    """List open issues for a repository."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/issues",
            headers=_headers(),
            params={"state": "open"},
        )

    if response.status_code != 200:
        return {"error": f"GitHub API error: {response.status_code}"}

    issues = response.json()
    return {
        "issues": [
            {"number": i["number"], "title": i["title"], "url": i["html_url"]}
            for i in issues
            if "pull_request" not in i  # GitHub's API mixes PRs into issues, filter them out
        ]
    }