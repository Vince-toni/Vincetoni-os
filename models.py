AVAILABLE_MODELS = {
    "default": "meta-llama/llama-3.3-70b-instruct",
    "coding": "qwen/qwen-2.5-coder-32b-instruct",
    "fast": "meta-llama/llama-3.1-8b-instruct",
}

def get_model(key: str = "default") -> str:
    return AVAILABLE_MODELS.get(key, AVAILABLE_MODELS["default"])