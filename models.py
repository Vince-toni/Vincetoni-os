import os

PROVIDERS = {
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1/chat/completions",
        "api_key": os.getenv("OPENROUTER_API"),
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1/chat/completions",
        "api_key": os.getenv("GROQ_API_KEY"),
    },
}

AVAILABLE_MODELS = {
    "default": {"model": "meta-llama/llama-3.3-70b-instruct", "provider": "openrouter"},
    "coding": {"model": "meta-llama/llama-3.3-70b-instruct", "provider": "openrouter"},
    "fast": {"model": "llama-3.3-70b-versatile", "provider": "groq"},
}

def get_model(key: str = "default") -> dict:
    choice = AVAILABLE_MODELS.get(key, AVAILABLE_MODELS["default"])
    provider = PROVIDERS[choice["provider"]]
    return {
        "model": choice["model"],
        "base_url": provider["base_url"],
        "api_key": provider["api_key"],
    }