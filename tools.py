import os
import subprocess


WORKSPACE_ROOT = os.getcwd()


def confirm_safe_path(path: str) -> str:
    full_path = os.path.abspath(path)

    if not full_path.startswith(WORKSPACE_ROOT):
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

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"{path} written successfully."


def run_python(path: str) -> str:
    path = confirm_safe_path(path)
    if path.startswith("ERROR"):
        return path

    result = subprocess.run(
        ["python", path],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return f"SUCCESS:\n{result.stdout}"
    else:
        return f"ERROR:\n{result.stderr}"


def install_package(package: str) -> str:
    result = subprocess.run(
        ["pip", "install", package],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return f"{package} installed successfully."
    else:
        return f"Installation failed:\n{result.stderr}"