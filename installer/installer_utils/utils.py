import subprocess
import sys


def run_command(cmd):
    print(f"Running command: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed with return code {result.returncode}: {cmd}")


def check_dependency_installed(command):
    """Returns True if command is found in PATH, else False."""
    try:
        result = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return result.returncode == 0
    except Exception:
        return False
