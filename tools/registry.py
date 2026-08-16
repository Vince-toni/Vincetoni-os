from tools.handlers import get_app_status, get_current_date, get_current_time

TOOL_REGISTRY = {
    "get_current_time": get_current_time,
    "get_current_date": get_current_date,
    "get_app_status": get_app_status,
}