"""
GitHub Integration Tools for DevPilot
=====================================
A comprehensive set of async GitHub API utilities for project management,
issue tracking, repository operations, and bidirectional sync.

Usage:
    from github_tools import (
        list_repo_issues,
        list_repositories,
        get_repo_details,
        create_issue,
        update_issue,
        get_issue,
        list_pull_requests,
        get_pull_request,
        list_branches,
        get_file_contents,
        create_or_update_file,
        list_labels,
        add_labels_to_issue,
        create_branch,
        create_pull_request,
        get_commits,
        search_repositories,
        search_issues,
        get_rate_limit,
        sync_task_to_issue,
        sync_issue_to_task,
    )

Environment:
    GITHUB_TOKEN — Personal Access Token with repo scope
"""

from __future__ import annotations

import base64
import os
from datetime import datetime
from typing import Any, Literal

import httpx

GITHUB_API = "https://api.github.com"
DEFAULT_PER_PAGE = 30
MAX_PER_PAGE = 100


def _headers() -> dict[str, str]:
    """Build authenticated request headers."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN environment variable is not set")
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _extract_error(response: httpx.Response) -> dict[str, Any]:
    """Extract a clean error message from a GitHub API response."""
    try:
        body = response.json()
        msg = body.get("message", "Unknown error")
        errors = body.get("errors", [])
        if errors:
            msg += f" | Details: {errors}"
    except Exception:
        msg = response.text or f"HTTP {response.status_code}"
    return {"error": msg, "status_code": response.status_code}


# ═══════════════════════════════════════════════════════════════
# Repository Operations
# ═══════════════════════════════════════════════════════════════

async def list_repositories(
    owner: str | None = None,
    affiliation: Literal["owner", "collaborator", "organization_member"] = "owner",
    sort: Literal["created", "updated", "pushed", "full_name"] = "updated",
    per_page: int = DEFAULT_PER_PAGE,
    page: int = 1,
) -> dict[str, Any]:
    """List repositories accessible to this GitHub token.

    Args:
        affiliation: Filter by owner, collaborator, or org member.
        sort: Sort field.
        per_page: Items per page (max 100).
        page: Page number.

    Returns:
        {"repositories": [...]} or {"error": ...}
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/user/repos",
            headers=_headers(),
            params={
                "affiliation": affiliation,
                "sort": sort,
                "per_page": min(per_page, MAX_PER_PAGE),
                "page": page,
            },
        )

    if response.status_code != 200:
        return _extract_error(response)

    repos = response.json()
    if owner:
        repos = [repo for repo in repos if repo["owner"]["login"].lower() == owner.lower()]
    return {
        "repositories": [
            {
                "id": r["id"],
                "full_name": r["full_name"],
                "name": r["name"],
                "owner": r["owner"]["login"],
                "private": r["private"],
                "html_url": r["html_url"],
                "description": r.get("description"),
                "default_branch": r["default_branch"],
                "updated_at": r["updated_at"],
                "language": r.get("language"),
                "open_issues_count": r.get("open_issues_count", 0),
            }
            for r in repos
        ],
        "page": page,
        "per_page": per_page,
    }


async def get_repo_details(owner: str, repo: str) -> dict[str, Any]:
    """Get detailed information about a repository.

    Returns:
        Repository metadata including branches, issues count, permissions.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}",
            headers=_headers(),
        )

    if response.status_code != 200:
        return _extract_error(response)

    r = response.json()
    return {
        "id": r["id"],
        "full_name": r["full_name"],
        "name": r["name"],
        "owner": r["owner"]["login"],
        "private": r["private"],
        "html_url": r["html_url"],
        "description": r.get("description"),
        "default_branch": r["default_branch"],
        "created_at": r["created_at"],
        "updated_at": r["updated_at"],
        "pushed_at": r.get("pushed_at"),
        "language": r.get("language"),
        "forks_count": r["forks_count"],
        "stargazers_count": r["stargazers_count"],
        "watchers_count": r["watchers_count"],
        "open_issues_count": r["open_issues_count"],
        "topics": r.get("topics", []),
        "permissions": r.get("permissions", {}),
        "size": r["size"],
    }


async def search_repositories(
    query: str,
    sort: Literal["stars", "forks", "help-wanted-issues", "updated"] | None = None,
    order: Literal["asc", "desc"] = "desc",
    per_page: int = DEFAULT_PER_PAGE,
    page: int = 1,
) -> dict[str, Any]:
    """Search repositories on GitHub.

    Args:
        query: Search query (e.g., "language:python stars:>1000").
        sort: Sort field.
        order: Sort order.
        per_page: Items per page.
        page: Page number.

    Returns:
        {"repositories": [...], "total_count": N} or error dict.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/search/repositories",
            headers=_headers(),
            params={
                "q": query,
                "sort": sort,
                "order": order,
                "per_page": min(per_page, MAX_PER_PAGE),
                "page": page,
            },
        )

    if response.status_code != 200:
        return _extract_error(response)

    data = response.json()
    return {
        "total_count": data["total_count"],
        "repositories": [
            {
                "id": r["id"],
                "full_name": r["full_name"],
                "html_url": r["html_url"],
                "description": r.get("description"),
                "language": r.get("language"),
                "stargazers_count": r["stargazers_count"],
                "open_issues_count": r["open_issues_count"],
            }
            for r in data.get("items", [])
        ],
    }


# ═══════════════════════════════════════════════════════════════
# Issue Operations
# ═══════════════════════════════════════════════════════════════

async def list_repo_issues(
    owner: str,
    repo: str,
    state: Literal["open", "closed", "all"] = "open",
    labels: str | None = None,
    assignee: str | None = None,
    sort: Literal["created", "updated", "comments"] = "created",
    direction: Literal["asc", "desc"] = "desc",
    per_page: int = DEFAULT_PER_PAGE,
    page: int = 1,
) -> dict[str, Any]:
    """List issues for a repository (excludes pull requests).

    Args:
        owner: Repository owner.
        repo: Repository name.
        state: Filter by issue state.
        labels: Comma-separated list of label names.
        assignee: Filter by assignee login (use "none" for unassigned).
        sort: Sort field.
        direction: Sort direction.
        per_page: Items per page.
        page: Page number.

    Returns:
        {"issues": [...], "page": N, "per_page": M} or error dict.
    """
    params: dict[str, Any] = {
        "state": state,
        "sort": sort,
        "direction": direction,
        "per_page": min(per_page, MAX_PER_PAGE),
        "page": page,
    }
    if labels:
        params["labels"] = labels
    if assignee:
        params["assignee"] = assignee

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/issues",
            headers=_headers(),
            params=params,
        )

    if response.status_code != 200:
        return _extract_error(response)

    issues = response.json()
    return {
        "issues": [
            {
                "number": i["number"],
                "title": i["title"],
                "body": i.get("body"),
                "state": i["state"],
                "html_url": i["html_url"],
                "created_at": i["created_at"],
                "updated_at": i["updated_at"],
                "closed_at": i.get("closed_at"),
                "user": {
                    "login": i["user"]["login"],
                    "avatar_url": i["user"]["avatar_url"],
                },
                "labels": [l["name"] for l in i.get("labels", [])],
                "assignees": [a["login"] for a in i.get("assignees", [])],
                "milestone": i["milestone"]["title"] if i.get("milestone") else None,
                "comments": i["comments"],
            }
            for i in issues
            if "pull_request" not in i  # Filter out PRs
        ],
        "page": page,
        "per_page": per_page,
    }


async def get_issue(owner: str, repo: str, issue_number: int) -> dict[str, Any]:
    """Get detailed information about a single issue.

    Returns:
        Issue details or error dict.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/issues/{issue_number}",
            headers=_headers(),
        )

    if response.status_code != 200:
        return _extract_error(response)

    i = response.json()
    return {
        "number": i["number"],
        "title": i["title"],
        "body": i.get("body"),
        "state": i["state"],
        "html_url": i["html_url"],
        "created_at": i["created_at"],
        "updated_at": i["updated_at"],
        "closed_at": i.get("closed_at"),
        "user": {
            "login": i["user"]["login"],
            "avatar_url": i["user"]["avatar_url"],
        },
        "labels": [l["name"] for l in i.get("labels", [])],
        "assignees": [a["login"] for a in i.get("assignees", [])],
        "milestone": i["milestone"]["title"] if i.get("milestone") else None,
        "comments": i["comments"],
        "locked": i["locked"],
    }


async def create_issue(
    owner: str,
    repo: str,
    title: str,
    body: str | None = None,
    labels: list[str] | None = None,
    assignees: list[str] | None = None,
    milestone: int | None = None,
) -> dict[str, Any]:
    """Create a new issue in a repository.

    Args:
        owner: Repository owner.
        repo: Repository name.
        title: Issue title.
        body: Issue body (Markdown supported).
        labels: List of label names to apply.
        assignees: List of GitHub usernames to assign.
        milestone: Milestone number to associate.

    Returns:
        Created issue details or error dict.
    """
    payload: dict[str, Any] = {"title": title}
    if body:
        payload["body"] = body
    if labels:
        payload["labels"] = labels
    if assignees:
        payload["assignees"] = assignees
    if milestone:
        payload["milestone"] = milestone

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GITHUB_API}/repos/{owner}/{repo}/issues",
            headers=_headers(),
            json=payload,
        )

    if response.status_code != 201:
        return _extract_error(response)

    i = response.json()
    return {
        "number": i["number"],
        "title": i["title"],
        "html_url": i["html_url"],
        "state": i["state"],
        "created_at": i["created_at"],
        "labels": [l["name"] for l in i.get("labels", [])],
    }


async def update_issue(
    owner: str,
    repo: str,
    issue_number: int,
    title: str | None = None,
    body: str | None = None,
    state: Literal["open", "closed"] | None = None,
    labels: list[str] | None = None,
    assignees: list[str] | None = None,
    milestone: int | None = None,
) -> dict[str, Any]:
    """Update an existing issue.

    Only provided fields are updated.

    Returns:
        Updated issue details or error dict.
    """
    payload: dict[str, Any] = {}
    if title is not None:
        payload["title"] = title
    if body is not None:
        payload["body"] = body
    if state is not None:
        payload["state"] = state
    if labels is not None:
        payload["labels"] = labels
    if assignees is not None:
        payload["assignees"] = assignees
    if milestone is not None:
        payload["milestone"] = milestone

    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{GITHUB_API}/repos/{owner}/{repo}/issues/{issue_number}",
            headers=_headers(),
            json=payload,
        )

    if response.status_code != 200:
        return _extract_error(response)

    i = response.json()
    return {
        "number": i["number"],
        "title": i["title"],
        "state": i["state"],
        "html_url": i["html_url"],
        "updated_at": i["updated_at"],
        "labels": [l["name"] for l in i.get("labels", [])],
    }


async def search_issues(
    query: str,
    sort: Literal["comments", "reactions", "created", "updated"] | None = None,
    order: Literal["asc", "desc"] = "desc",
    per_page: int = DEFAULT_PER_PAGE,
    page: int = 1,
) -> dict[str, Any]:
    """Search issues across GitHub.

    Args:
        query: Search query (e.g., "repo:owner/repo is:open label:bug").
        sort: Sort field.
        order: Sort order.
        per_page: Items per page.
        page: Page number.

    Returns:
        {"issues": [...], "total_count": N} or error dict.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/search/issues",
            headers=_headers(),
            params={
                "q": query,
                "sort": sort,
                "order": order,
                "per_page": min(per_page, MAX_PER_PAGE),
                "page": page,
            },
        )

    if response.status_code != 200:
        return _extract_error(response)

    data = response.json()
    return {
        "total_count": data["total_count"],
        "issues": [
            {
                "number": i["number"],
                "title": i["title"],
                "state": i["state"],
                "html_url": i["html_url"],
                "created_at": i["created_at"],
                "updated_at": i["updated_at"],
                "labels": [l["name"] for l in i.get("labels", [])],
                "repository": i.get("repository_url", "").replace(
                    "https://api.github.com/repos/", ""
                ),
            }
            for i in data.get("items", [])
        ],
    }


# ═══════════════════════════════════════════════════════════════
# Pull Request Operations
# ═══════════════════════════════════════════════════════════════

async def list_pull_requests(
    owner: str,
    repo: str,
    state: Literal["open", "closed", "all"] = "open",
    sort: Literal["created", "updated", "popularity", "long-running"] = "created",
    direction: Literal["asc", "desc"] = "desc",
    per_page: int = DEFAULT_PER_PAGE,
    page: int = 1,
) -> dict[str, Any]:
    """List pull requests for a repository.

    Returns:
        {"pull_requests": [...]} or error dict.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/pulls",
            headers=_headers(),
            params={
                "state": state,
                "sort": sort,
                "direction": direction,
                "per_page": min(per_page, MAX_PER_PAGE),
                "page": page,
            },
        )

    if response.status_code != 200:
        return _extract_error(response)

    prs = response.json()
    return {
        "pull_requests": [
            {
                "number": pr["number"],
                "title": pr["title"],
                "body": pr.get("body"),
                "state": pr["state"],
                "html_url": pr["html_url"],
                "created_at": pr["created_at"],
                "updated_at": pr["updated_at"],
                "user": {
                    "login": pr["user"]["login"],
                    "avatar_url": pr["user"]["avatar_url"],
                },
                "head": {
                    "ref": pr["head"]["ref"],
                    "sha": pr["head"]["sha"],
                },
                "base": {
                    "ref": pr["base"]["ref"],
                    "sha": pr["base"]["sha"],
                },
                "draft": pr["draft"],
                "merged": pr.get("merged_at") is not None,
                "mergeable": pr.get("mergeable"),
                "labels": [l["name"] for l in pr.get("labels", [])],
                "comments": pr["comments"],
                "review_comments": pr["review_comments"],
            }
            for pr in prs
        ],
        "page": page,
        "per_page": per_page,
    }


async def get_pull_request(owner: str, repo: str, pr_number: int) -> dict[str, Any]:
    """Get detailed information about a single pull request."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}",
            headers=_headers(),
        )

    if response.status_code != 200:
        return _extract_error(response)

    pr = response.json()
    return {
        "number": pr["number"],
        "title": pr["title"],
        "body": pr.get("body"),
        "state": pr["state"],
        "html_url": pr["html_url"],
        "created_at": pr["created_at"],
        "updated_at": pr["updated_at"],
        "closed_at": pr.get("closed_at"),
        "merged_at": pr.get("merged_at"),
        "user": {
            "login": pr["user"]["login"],
            "avatar_url": pr["user"]["avatar_url"],
        },
        "head": {
            "ref": pr["head"]["ref"],
            "sha": pr["head"]["sha"],
        },
        "base": {
            "ref": pr["base"]["ref"],
            "sha": pr["base"]["sha"],
        },
        "draft": pr["draft"],
        "mergeable": pr.get("mergeable"),
        "mergeable_state": pr.get("mergeable_state"),
        "labels": [l["name"] for l in pr.get("labels", [])],
        "additions": pr.get("additions"),
        "deletions": pr.get("deletions"),
        "changed_files": pr.get("changed_files"),
    }


async def create_pull_request(
    owner: str,
    repo: str,
    title: str,
    head: str,
    base: str,
    body: str | None = None,
    draft: bool = False,
) -> dict[str, Any]:
    """Create a new pull request.

    Args:
        owner: Repository owner.
        repo: Repository name.
        title: PR title.
        head: Branch name containing changes.
        base: Branch to merge into.
        body: PR description (Markdown supported).
        draft: Create as draft PR.

    Returns:
        Created PR details or error dict.
    """
    payload: dict[str, Any] = {
        "title": title,
        "head": head,
        "base": base,
        "draft": draft,
    }
    if body:
        payload["body"] = body

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GITHUB_API}/repos/{owner}/{repo}/pulls",
            headers=_headers(),
            json=payload,
        )

    if response.status_code != 201:
        return _extract_error(response)

    pr = response.json()
    return {
        "number": pr["number"],
        "title": pr["title"],
        "html_url": pr["html_url"],
        "state": pr["state"],
        "head": pr["head"]["ref"],
        "base": pr["base"]["ref"],
        "draft": pr["draft"],
    }


# ═══════════════════════════════════════════════════════════════
# Branch & Commit Operations
# ═══════════════════════════════════════════════════════════════

async def list_branches(
    owner: str,
    repo: str,
    per_page: int = DEFAULT_PER_PAGE,
    page: int = 1,
) -> dict[str, Any]:
    """List branches in a repository."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/branches",
            headers=_headers(),
            params={
                "per_page": min(per_page, MAX_PER_PAGE),
                "page": page,
            },
        )

    if response.status_code != 200:
        return _extract_error(response)

    branches = response.json()
    return {
        "branches": [
            {
                "name": b["name"],
                "commit_sha": b["commit"]["sha"],
                "protected": b["protected"],
            }
            for b in branches
        ],
        "page": page,
        "per_page": per_page,
    }


async def get_commits(
    owner: str,
    repo: str,
    sha: str | None = None,
    path: str | None = None,
    per_page: int = DEFAULT_PER_PAGE,
    page: int = 1,
) -> dict[str, Any]:
    """List commits in a repository.

    Args:
        sha: Branch name or commit SHA to start from.
        path: Filter commits affecting this file path.
        per_page: Items per page.
        page: Page number.

    Returns:
        {"commits": [...]} or error dict.
    """
    params: dict[str, Any] = {
        "per_page": min(per_page, MAX_PER_PAGE),
        "page": page,
    }
    if sha:
        params["sha"] = sha
    if path:
        params["path"] = path

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/commits",
            headers=_headers(),
            params=params,
        )

    if response.status_code != 200:
        return _extract_error(response)

    commits = response.json()
    return {
        "commits": [
            {
                "sha": c["sha"],
                "message": c["commit"]["message"],
                "author_name": c["commit"]["author"]["name"],
                "author_email": c["commit"]["author"]["email"],
                "author_login": c["author"]["login"] if c.get("author") else None,
                "date": c["commit"]["author"]["date"],
                "html_url": c["html_url"],
            }
            for c in commits
        ],
        "page": page,
        "per_page": per_page,
    }


async def create_branch(
    owner: str,
    repo: str,
    branch_name: str,
    from_branch: str | None = None,
) -> dict[str, Any]:
    """Create a new branch from an existing branch or default branch.

    Args:
        owner: Repository owner.
        repo: Repository name.
        branch_name: Name for the new branch.
        from_branch: Base branch (defaults to repo's default branch).

    Returns:
        Created branch details or error dict.
    """
    # First, get the SHA of the base branch
    base = from_branch or (await get_repo_details(owner, repo)).get("default_branch", "main")

    async with httpx.AsyncClient() as client:
        ref_response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/git/ref/heads/{base}",
            headers=_headers(),
        )

    if ref_response.status_code != 200:
        return _extract_error(ref_response)

    base_sha = ref_response.json()["object"]["sha"]

    # Create the new branch ref
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GITHUB_API}/repos/{owner}/{repo}/git/refs",
            headers=_headers(),
            json={
                "ref": f"refs/heads/{branch_name}",
                "sha": base_sha,
            },
        )

    if response.status_code != 201:
        return _extract_error(response)

    ref = response.json()
    return {
        "name": branch_name,
        "sha": ref["object"]["sha"],
        "ref": ref["ref"],
        "base_branch": base,
    }


# ═══════════════════════════════════════════════════════════════
# File Operations
# ═══════════════════════════════════════════════════════════════

async def get_file_contents(
    owner: str,
    repo: str,
    path: str,
    ref: str | None = None,
) -> dict[str, Any]:
    """Get contents of a file or directory in a repository.

    Args:
        owner: Repository owner.
        repo: Repository name.
        path: File or directory path.
        ref: Branch, tag, or commit SHA.

    Returns:
        File contents (decoded) or directory listing, or error dict.
    """
    params: dict[str, Any] = {}
    if ref:
        params["ref"] = ref

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}",
            headers=_headers(),
            params=params,
        )

    if response.status_code != 200:
        return _extract_error(response)

    data = response.json()

    # Directory listing
    if isinstance(data, list):
        return {
            "type": "directory",
            "path": path,
            "contents": [
                {
                    "name": item["name"],
                    "type": item["type"],
                    "path": item["path"],
                    "size": item.get("size"),
                    "sha": item["sha"],
                }
                for item in data
            ],
        }

    # Single file
    content = base64.b64decode(data["content"]).decode("utf-8") if data.get("content") else None
    return {
        "type": "file",
        "name": data["name"],
        "path": data["path"],
        "sha": data["sha"],
        "size": data["size"],
        "content": content,
        "html_url": data["html_url"],
        "download_url": data.get("download_url"),
    }


async def create_or_update_file(
    owner: str,
    repo: str,
    path: str,
    content: str,
    message: str,
    branch: str,
    sha: str | None = None,
) -> dict[str, Any]:
    """Create or update a file in a repository.

    Args:
        owner: Repository owner.
        repo: Repository name.
        path: File path.
        content: File content (plain text, will be base64 encoded).
        message: Commit message.
        branch: Target branch.
        sha: Existing file SHA (required for updates, omit for creation).

    Returns:
        Commit details or error dict.
    """
    payload: dict[str, Any] = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha

    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}",
            headers=_headers(),
            json=payload,
        )

    if response.status_code not in (200, 201):
        return _extract_error(response)

    data = response.json()
    return {
        "commit_sha": data["commit"]["sha"],
        "commit_url": data["commit"]["html_url"],
        "content_sha": data["content"]["sha"],
        "path": data["content"]["path"],
        "branch": branch,
    }


# ═══════════════════════════════════════════════════════════════
# Label Operations
# ═══════════════════════════════════════════════════════════════

async def list_labels(
    owner: str,
    repo: str,
    per_page: int = DEFAULT_PER_PAGE,
    page: int = 1,
) -> dict[str, Any]:
    """List labels in a repository."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/labels",
            headers=_headers(),
            params={
                "per_page": min(per_page, MAX_PER_PAGE),
                "page": page,
            },
        )

    if response.status_code != 200:
        return _extract_error(response)

    labels = response.json()
    return {
        "labels": [
            {
                "name": l["name"],
                "color": l["color"],
                "description": l.get("description"),
            }
            for l in labels
        ],
        "page": page,
        "per_page": per_page,
    }


async def add_labels_to_issue(
    owner: str,
    repo: str,
    issue_number: int,
    labels: list[str],
) -> dict[str, Any]:
    """Add labels to an issue (replaces all existing labels).

    Args:
        owner: Repository owner.
        repo: Repository name.
        issue_number: Issue number.
        labels: List of label names.

    Returns:
        Updated labels or error dict.
    """
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{GITHUB_API}/repos/{owner}/{repo}/issues/{issue_number}/labels",
            headers=_headers(),
            json={"labels": labels},
        )

    if response.status_code != 200:
        return _extract_error(response)

    result = response.json()
    return {
        "labels": [l["name"] for l in result],
        "issue_number": issue_number,
    }


# ═══════════════════════════════════════════════════════════════
# Rate Limit & Health
# ═══════════════════════════════════════════════════════════════

async def get_rate_limit() -> dict[str, Any]:
    """Get current GitHub API rate limit status.

    Returns:
        Rate limit info for all resource categories.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/rate_limit",
            headers=_headers(),
        )

    if response.status_code != 200:
        return _extract_error(response)

    data = response.json()
    resources = data.get("resources", {})
    return {
        "core": {
            "limit": resources.get("core", {}).get("limit"),
            "used": resources.get("core", {}).get("used"),
            "remaining": resources.get("core", {}).get("remaining"),
            "reset_at": datetime.fromtimestamp(
                resources.get("core", {}).get("reset", 0)
            ).isoformat(),
        },
        "search": {
            "limit": resources.get("search", {}).get("limit"),
            "used": resources.get("search", {}).get("used"),
            "remaining": resources.get("search", {}).get("remaining"),
            "reset_at": datetime.fromtimestamp(
                resources.get("search", {}).get("reset", 0)
            ).isoformat(),
        },
        "graphql": {
            "limit": resources.get("graphql", {}).get("limit"),
            "used": resources.get("graphql", {}).get("used"),
            "remaining": resources.get("graphql", {}).get("remaining"),
            "reset_at": datetime.fromtimestamp(
                resources.get("graphql", {}).get("reset", 0)
            ).isoformat(),
        },
    }


# ═══════════════════════════════════════════════════════════════
# DevPilot Sync Helpers
# ═══════════════════════════════════════════════════════════════

async def sync_task_to_issue(
    owner: str,
    repo: str,
    task: dict[str, Any],
    existing_issue_number: int | None = None,
) -> dict[str, Any]:
    """Sync a DevPilot task to a GitHub issue.

    Creates a new issue or updates an existing one based on task data.

    Args:
        owner: Repository owner.
        repo: Repository name.
        task: DevPilot task dict with keys: title, description, status,
              labels, assignees, priority.
        existing_issue_number: If provided, updates this issue instead of creating.

    Returns:
        Sync result with issue_number and html_url.
    """
    # Map DevPilot status to GitHub issue state
    status = task.get("status", "todo")
    state = "closed" if status in ("done", "completed", "closed") else "open"

    # Build body with DevPilot metadata footer
    body_parts = [task.get("description", "")]
    if task.get("priority"):
        body_parts.append(f"\n\n---\n**Priority:** {task['priority']}")
    if task.get("due_date"):
        body_parts.append(f"**Due:** {task['due_date']}")
    body_parts.append("\n*Synced from DevPilot*")
    body = "\n".join(body_parts)

    labels = task.get("labels", [])
    # Add priority as label if not already present
    if task.get("priority") and f"priority:{task['priority']}" not in labels:
        labels = [*labels, f"priority:{task['priority']}"]

    assignees = task.get("assignees", [])

    if existing_issue_number:
        result = await update_issue(
            owner=owner,
            repo=repo,
            issue_number=existing_issue_number,
            title=task["title"],
            body=body,
            state=state,
            labels=labels,
            assignees=assignees,
        )
        if "error" in result:
            return result
        return {
            "action": "updated",
            "issue_number": result["number"],
            "html_url": result["html_url"],
            "state": result["state"],
        }
    else:
        result = await create_issue(
            owner=owner,
            repo=repo,
            title=task["title"],
            body=body,
            labels=labels,
            assignees=assignees,
        )
        if "error" in result:
            return result
        return {
            "action": "created",
            "issue_number": result["number"],
            "html_url": result["html_url"],
            "state": result["state"],
        }


async def sync_issue_to_task(
    owner: str,
    repo: str,
    issue_number: int,
) -> dict[str, Any]:
    """Fetch a GitHub issue and format it as a DevPilot task.

    Args:
        owner: Repository owner.
        repo: Repository name.
        issue_number: Issue number to sync.

    Returns:
        Task-compatible dict or error dict.
    """
    issue = await get_issue(owner, repo, issue_number)
    if "error" in issue:
        return issue

    # Extract priority from labels
    priority = None
    labels = []
    for label in issue.get("labels", []):
        if label.startswith("priority:"):
            priority = label.replace("priority:", "")
        else:
            labels.append(label)

    # Map GitHub state to DevPilot status
    status_map = {
        "open": "todo",
        "closed": "done",
    }

    return {
        "title": issue["title"],
        "description": issue.get("body", ""),
        "status": status_map.get(issue["state"], "todo"),
        "labels": labels,
        "priority": priority,
        "assignees": issue.get("assignees", []),
        "github_issue_number": issue["number"],
        "github_html_url": issue["html_url"],
        "github_updated_at": issue["updated_at"],
        "source": "github",
    }


# ═══════════════════════════════════════════════════════════════
# Webhook Verification (for incoming GitHub webhooks)
# ═══════════════════════════════════════════════════════════════

import hmac
import hashlib


def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify a GitHub webhook signature.

    Args:
        payload: Raw request body bytes.
        signature: X-Hub-Signature-256 header value (e.g., "sha256=abc123...").
        secret: Webhook secret configured in GitHub.

    Returns:
        True if signature is valid.
    """
    if not signature.startswith("sha256="):
        return False
    expected = hmac.new(
        secret.encode("utf-8"),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(signature[7:], expected)