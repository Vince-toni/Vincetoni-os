from tools.handlers import get_app_status, get_current_date, get_current_time
from tools.calculator import calculate
from tools.web_search import web_search


LOCAL_TOOL_REGISTRY = {
    "get_current_time": get_current_time,
    "get_current_date": get_current_date,
    "get_app_status": get_app_status,
    "calculate": calculate,
    "web_search": web_search,
}