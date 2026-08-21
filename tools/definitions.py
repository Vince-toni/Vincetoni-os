TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time in UTC. Use this whenever the user asks what time or date it is right now.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_date",
            "description": "Get the current date in UTC format. Use this when the user asks for today's date.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_app_status",
            "description": "Return the app's status and current UTC timestamp. Use this when the user asks whether the bot is online or asks for app info.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a numeric expression safely (supports +, -, *, /, **, %, // and unary +/-).",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "A numeric expression to evaluate (e.g. '2+2*3')"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Perform a lightweight web search (stub) and return a small list of results. Uses DuckDuckGo instant-answer as a safe first-pass.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "max_results": {"type": "integer", "description": "Maximum number of results to return", "default": 3}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file under the repository root (read-only, path restricted). Returns file content up to a size limit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file (absolute or relative to repo root)"},
                    "max_bytes": {"type": "integer", "description": "Maximum number of bytes to return", "default": 10000}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List contents of a directory under the repository root (read-only).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path (absolute or relative to repo root)", "default": "."},
                    "max_items": {"type": "integer", "description": "Maximum number of entries to return", "default": 200}
                },
                "required": []
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "list_repo_issues",
        "description": "List open issues in a GitHub repository. Use this when the user asks about open issues, bugs, or tasks in a specific repo.",
        "parameters": {
            "type": "object",
            "properties": {
                    "owner": {"type": "string", "description": "The GitHub username or organization that owns the repo"},
                    "repo": {"type": "string", "description": "The repository name"},
                    "state": {"type": "string", "enum": ["open", "closed", "all"], "default": "open"},
                    "labels": {"type": "string", "description": "Comma-separated label names"},
                    "assignee": {"type": "string", "description": "Assignee login, or 'none' for unassigned"},
                    "sort": {"type": "string", "enum": ["created", "updated", "comments"], "default": "created"},
                    "direction": {"type": "string", "enum": ["asc", "desc"], "default": "desc"},
                    "per_page": {"type": "integer", "minimum": 1, "maximum": 100, "default": 30},
                    "page": {"type": "integer", "minimum": 1, "default": 1}
            },
            "required": ["owner", "repo"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "list_repositories",
        "description": "List all GitHub repositories this token has access to, including private ones. Use this when the user asks what repositories exist, or when a repository lookup by name fails and you need to check the exact available repo names.",
        "parameters": {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Optional GitHub username or organization filter"},
                "affiliation": {"type": "string", "enum": ["owner", "collaborator", "organization_member"], "default": "owner"},
                "sort": {"type": "string", "enum": ["created", "updated", "pushed", "full_name"], "default": "updated"},
                "per_page": {"type": "integer", "minimum": 1, "maximum": 100, "default": 30},
                "page": {"type": "integer", "minimum": 1, "default": 1}
            },
            "required": []
        }
    }
}
]

TOOL_DEFINITIONS.extend([
    {
        "type": "function",
        "function": {
            "name": "get_repo_details",
            "description": "Get detailed metadata and permissions for a GitHub repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string", "description": "Repository owner"},
                    "repo": {"type": "string", "description": "Repository name"},
                },
                "required": ["owner", "repo"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_repositories",
            "description": "Search GitHub repositories using GitHub search syntax.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "GitHub repository search query"},
                    "sort": {"type": "string", "enum": ["stars", "forks", "help-wanted-issues", "updated"]},
                    "order": {"type": "string", "enum": ["asc", "desc"], "default": "desc"},
                    "per_page": {"type": "integer", "minimum": 1, "maximum": 100, "default": 30},
                    "page": {"type": "integer", "minimum": 1, "default": 1},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_issue",
            "description": "Get details for a GitHub issue.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "issue_number": {"type": "integer", "minimum": 1},
                },
                "required": ["owner", "repo", "issue_number"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_issue",
            "description": "Create an issue in a GitHub repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "title": {"type": "string"},
                    "body": {"type": ["string", "null"]},
                    "labels": {"type": "array", "items": {"type": "string"}},
                    "assignees": {"type": "array", "items": {"type": "string"}},
                    "milestone": {"type": ["integer", "null"]},
                },
                "required": ["owner", "repo", "title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_issue",
            "description": "Update the provided fields of a GitHub issue.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "issue_number": {"type": "integer", "minimum": 1},
                    "title": {"type": "string"},
                    "body": {"type": ["string", "null"]},
                    "state": {"type": "string", "enum": ["open", "closed"]},
                    "labels": {"type": "array", "items": {"type": "string"}},
                    "assignees": {"type": "array", "items": {"type": "string"}},
                    "milestone": {"type": ["integer", "null"]},
                },
                "required": ["owner", "repo", "issue_number"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_issues",
            "description": "Search GitHub issues and pull requests using GitHub search syntax.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "sort": {"type": "string", "enum": ["comments", "reactions", "created", "updated"]},
                    "order": {"type": "string", "enum": ["asc", "desc"], "default": "desc"},
                    "per_page": {"type": "integer", "minimum": 1, "maximum": 100, "default": 30},
                    "page": {"type": "integer", "minimum": 1, "default": 1},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_pull_requests",
            "description": "List pull requests for a GitHub repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "state": {"type": "string", "enum": ["open", "closed", "all"], "default": "open"},
                    "sort": {"type": "string", "enum": ["created", "updated", "popularity", "long-running"], "default": "created"},
                    "direction": {"type": "string", "enum": ["asc", "desc"], "default": "desc"},
                    "per_page": {"type": "integer", "minimum": 1, "maximum": 100, "default": 30},
                    "page": {"type": "integer", "minimum": 1, "default": 1},
                },
                "required": ["owner", "repo"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pull_request",
            "description": "Get detailed information about a GitHub pull request.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "pr_number": {"type": "integer", "minimum": 1},
                },
                "required": ["owner", "repo", "pr_number"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_pull_request",
            "description": "Create a pull request in a GitHub repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "title": {"type": "string"},
                    "head": {"type": "string", "description": "Branch containing changes"},
                    "base": {"type": "string", "description": "Branch to merge into"},
                    "body": {"type": ["string", "null"]},
                    "draft": {"type": "boolean", "default": False},
                },
                "required": ["owner", "repo", "title", "head", "base"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_branches",
            "description": "List branches in a GitHub repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "per_page": {"type": "integer", "minimum": 1, "maximum": 100, "default": 30},
                    "page": {"type": "integer", "minimum": 1, "default": 1},
                },
                "required": ["owner", "repo"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_commits",
            "description": "List commits in a GitHub repository, optionally filtered by branch or path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "sha": {"type": "string"},
                    "path": {"type": "string"},
                    "per_page": {"type": "integer", "minimum": 1, "maximum": 100, "default": 30},
                    "page": {"type": "integer", "minimum": 1, "default": 1},
                },
                "required": ["owner", "repo"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_branch",
            "description": "Create a GitHub branch from an existing branch or the repository default branch.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "branch_name": {"type": "string"},
                    "from_branch": {"type": "string"},
                },
                "required": ["owner", "repo", "branch_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_file_contents",
            "description": "Read a file or directory listing from a GitHub repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "path": {"type": "string"},
                    "ref": {"type": "string", "description": "Branch, tag, or commit SHA"},
                },
                "required": ["owner", "repo", "path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_or_update_file",
            "description": "Create or update a file in a GitHub repository and commit the change.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                    "message": {"type": "string"},
                    "branch": {"type": "string"},
                    "sha": {"type": "string", "description": "Existing file SHA when updating"},
                },
                "required": ["owner", "repo", "path", "content", "message", "branch"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_labels",
            "description": "List labels in a GitHub repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "per_page": {"type": "integer", "minimum": 1, "maximum": 100, "default": 30},
                    "page": {"type": "integer", "minimum": 1, "default": 1},
                },
                "required": ["owner", "repo"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_labels_to_issue",
            "description": "Replace the labels on a GitHub issue with the provided labels.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "issue_number": {"type": "integer", "minimum": 1},
                    "labels": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["owner", "repo", "issue_number", "labels"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_rate_limit",
            "description": "Get the current GitHub API rate limit status.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sync_task_to_issue",
            "description": "Create or update a GitHub issue from a DevPilot task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "task": {"type": "object", "description": "Task object with title and optional metadata"},
                    "existing_issue_number": {"type": ["integer", "null"]},
                },
                "required": ["owner", "repo", "task"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sync_issue_to_task",
            "description": "Fetch a GitHub issue and format it as a DevPilot task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "issue_number": {"type": "integer", "minimum": 1},
                },
                "required": ["owner", "repo", "issue_number"],
            },
        },
    },
])

# Backward-compatible alias for older code paths.
TOOL_DEFINITION = TOOL_DEFINITIONS