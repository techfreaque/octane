import os
from ..utils import check_dependency_installed, run_command
from .base import InstallConfig, PlatformHandler


class WindowsHandler(PlatformHandler):
    def install_dependencies(self):
        if check_dependency_installed("choco --version"):
            run_command("choco install git python visualstudio2022buildtools -y")
        elif check_dependency_installed("winget --info"):
            run_command("winget install --id Git.Git -e --source winget")
            run_command("winget install --id Python.Python.3 -e --source winget")
            run_command(
                "winget install --id Microsoft.VisualStudio.2022.BuildTools -e --source winget"
            )
        else:
            raise RuntimeError("No package manager found (chocolatey/winget)")

    def setup_environment(self, config: InstallConfig):
        config.activate_cmd = "source .venv/bin/activate"
        config.create_env = "python -m venv .venv"
        config.python_cmd = "python"
        config.env_file = ".env-example-unix"
        self._setup_environment(config)

    def setup_autostart(self, config: InstallConfig):
        startup_folder = os.path.join(
            os.environ.get("APPDATA", ""),
            "Microsoft",
            "Windows",
            "Start Menu",
            "Programs",
            "Startup",
        )
        script_path = os.path.join(config.install_path, "start_octane.bat")
        with open(script_path, "w") as f:
            f.write(
                f'@echo off\ncd /d "{config.install_path}"\n'
                f"call {config.activate_cmd}\npython main.py\n"
            )
