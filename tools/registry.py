from tools.handlers import get_app_status, get_current_date, get_current_time
from tools.calculator import calculate
from tools.web_search import web_search
from tools.filesystem import read_file, list_directory

try:
    from tools.Github.handlers import list_repo_issues
except ModuleNotFoundError:  # pragma: no cover - fallback for non-package execution
    from Github.handlers import list_repo_issues

TOOL_REGISTRY = {
    "get_current_time": get_current_time,
    "get_current_date": get_current_date,
    "get_app_status": get_app_status,
    "calculate": calculate,
    "web_search": web_search,
    "read_file": read_file,
    "list_directory": list_directory,
    "list_repo_issues": list_repo_issues,
}