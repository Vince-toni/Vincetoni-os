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
                "repo": {"type": "string", "description": "The repository name"}
            },
            "required": ["owner", "repo"]
        }
    }
}
]

# Backward-compatible alias for older code paths.
TOOL_DEFINITION = TOOL_DEFINITIONS