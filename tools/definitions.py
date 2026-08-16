TOOL_DEFINITION = [
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
    }
]