import os
from .base import InstallConfig, PlatformHandler
from ..utils import check_dependency_installed, run_command


class MacHandler(PlatformHandler):
    def ensure_dependencies(self):
        if not check_dependency_installed("which brew"):
            raise RuntimeError("Homebrew not found")
        run_command("brew install git python")

    def setup_environment(self, config: InstallConfig):
        config.activate_cmd = "source .venv/bin/activate"
        config.create_env = "python3 -m venv .venv"
        config.python_cmd = "python3"
        config.env_file = ".env-example-unix"
        self._setup_environment(config)

    def install_packages(self, config: InstallConfig):
        self._install_packages(config)

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
