import os


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _resolve_path(path: str) -> str:
    if os.path.isabs(path):
        abs_path = os.path.abspath(path)
    else:
        abs_path = os.path.abspath(os.path.join(REPO_ROOT, path))
    return abs_path


def _is_within_repo(abs_path: str) -> bool:
    # Normalize trailing separators
    repo = os.path.join(REPO_ROOT, "")
    target = os.path.join(abs_path, "")
    return target.startswith(repo)


def read_file(path: str, max_bytes: int = 10000, **kwargs):
    """Read a file under the repository root. Returns an error if the path is outside the repo or not a file."""
    abs_path = _resolve_path(path)
    if not _is_within_repo(abs_path):
        return {"error": "Access denied: path is outside the repository root"}

    if not os.path.isfile(abs_path):
        return {"error": "Not a file"}

    try:
        with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read(max_bytes)
        return {"path": abs_path, "content": content}
    except Exception as e:
        return {"error": str(e)}


def list_directory(path: str = ".", max_items: int = 200, **kwargs):
    """List directory contents under the repository root."""
    abs_path = _resolve_path(path)
    if not _is_within_repo(abs_path):
        return {"error": "Access denied: path is outside the repository root"}

    if not os.path.isdir(abs_path):
        return {"error": "Not a directory"}

    try:
        entries = sorted(os.listdir(abs_path))[:max_items]
        info = []
        for name in entries:
            p = os.path.join(abs_path, name)
            info.append({
                "name": name,
                "is_dir": os.path.isdir(p),
                "size": os.path.getsize(p) if os.path.isfile(p) else None,
            })
        return {"path": abs_path, "entries": info}
    except Exception as e:
        return {"error": str(e)}
