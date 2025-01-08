from .base import PlatformHandler
from ..config import InstallConfig
from ..utils import check_dependency_installed, run_command
import os


class LinuxHandler(PlatformHandler):
    def install_dependencies(self, config: InstallConfig):
        missing_dependencies = [
            cmd
            for cmd in ["git", "python3"]
            if not check_dependency_installed(f"which {cmd}")
        ]

        if missing_dependencies:
            raise RuntimeError(
                f"Missing required dependencies: {', '.join(missing_dependencies)}"
            )

        if config.timesync:
            run_command("timedatectl set-ntp true")

    def setup_autostart(self, config: InstallConfig):
        autostart_dir = os.path.expanduser("~/.config/autostart")
        os.makedirs(autostart_dir, exist_ok=True)
        desktop_file = os.path.join(autostart_dir, "octane.desktop")
        with open(desktop_file, "w") as f:
            f.write(
                "[Desktop Entry]\n"
                "Type=Application\n"
                f"Exec={os.path.join(config.install_path, '.venv/bin/python')} "
                f"{os.path.join(config.install_path, 'main.py')}\n"
                "Hidden=false\n"
                "NoDisplay=false\n"
                "X-GNOME-Autostart-enabled=true\n"
                "Name=Octane\n"
            )



    def get_activate_cmd(self, config: InstallConfig):
        return f"source {config.install_path}/.venv/bin/activate"

    def get_create_env_cmd(self, config: InstallConfig):
        return f"python3 -m venv {config.install_path}/.venv"

    def get_python_cmd(self):
        return "python3"

    def get_env_file(self):
        return ".env-example-unix"
