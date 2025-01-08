import os
from .base import InstallConfig, PlatformHandler
from ..utils import check_dependency_installed, run_command


class MacHandler(PlatformHandler):
    def install_dependencies(self, config: InstallConfig):
        if not check_dependency_installed("which brew"):
            raise RuntimeError("Homebrew not found, please install it first.")
        run_command("brew install git python")

    def setup_autostart(self, config: InstallConfig):
        plist_dir = os.path.expanduser("~/Library/LaunchAgents")
        os.makedirs(plist_dir, exist_ok=True)
        plist_path = os.path.join(plist_dir, "com.octane.startup.plist")
        with open(plist_path, "w") as f:
            f.write(
                f"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
                <plist version="1.0">
                <dict>
                    <key>Label</key>
                    <string>com.octane.startup</string>
                    <key>ProgramArguments</key>
                    <array>
                        <string>{os.path.join(config.install_path, '.venv/bin/python')}</string>
                        <string>{os.path.join(config.install_path, 'main.py')}</string>
                    </array>
                    <key>RunAtLoad</key>
                    <true/>
                </dict>
                </plist>"""
            )
            
    def get_activate_cmd(self, config: InstallConfig):
        return f"source {config.install_path}/.venv/bin/activate"

    def get_create_env_cmd(self, config: InstallConfig):
        return f"python3 -m venv {config.install_path}/.venv"

    def get_python_cmd(self):
        return "python3"

    def get_env_file(self):
        return ".env-example-unix"
