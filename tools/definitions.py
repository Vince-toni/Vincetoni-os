LOCAL_TOOL_DEFINITIONS = [
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
]

# Backward-compatible alias for older code paths.
LOCAL_TOOL_DEFINITION = LOCAL_TOOL_DEFINITIONS