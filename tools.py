import os
import re
import subprocess

# Fix #1: Use env variable or fall back to cwd at call time (not import time)
WORKSPACE_ROOT = os.environ.get("WORKSPACE_ROOT", "")


def confirm_safe_path(path: str) -> str:
    # Resolve at call time, not import time
    workspace = os.path.abspath(WORKSPACE_ROOT) if WORKSPACE_ROOT else os.path.abspath(os.getcwd())
    full_path = os.path.abspath(path)

    if not full_path.startswith(workspace):
        return "ERROR: Access denied. Outside workspace."

    return full_path


def read_file(path: str) -> str:
    path = confirm_safe_path(path)
    if path.startswith("ERROR"):
        return path

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str, content: str) -> str:
    path = confirm_safe_path(path)
    if path.startswith("ERROR"):
        return path

    # Fix #2: Only call makedirs if there is a directory component
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"{path} written successfully."


def run_python(path: str) -> str:
    path = confirm_safe_path(path)
    if path.startswith("ERROR"):
        return path

    # Fix #3: Add 30s timeout to prevent infinite hangs
    try:
        result = subprocess.run(
            ["python", path],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return f"SUCCESS:\n{result.stdout}"
        else:
            return f"ERROR:\n{result.stderr}"

    except subprocess.TimeoutExpired:
        return "ERROR: Script timed out after 30 seconds. Check for infinite loops or blocking input."


def install_package(package: str) -> str:
    # Fix #4: Validate package name before passing to pip
    if not re.match(r'^[a-zA-Z0-9_\-\.]+$', package):
        return "ERROR: Invalid package name. Only letters, numbers, hyphens, underscores and dots are allowed."

    result = subprocess.run(
        ["pip", "install", package],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return f"{package} installed successfully."
    else:
        return f"Installation failed:\n{result.stderr}"
