AVAILABLE_MODELS = {
    "default": "meta-llama/llama-3.3-70b-instruct",
    "coding": "google/gemma-4-31b-it:free",
    "fast": "meta-llama/llama-3.1-8b-instruct",
}

def get_model(key: str = "default") -> str:
    return AVAILABLE_MODELS.get(key, AVAILABLE_MODELS["default"])