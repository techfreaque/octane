from dataclasses import dataclass
import os


@dataclass
class InstallConfig:
    install_path: str
    branch: str = "STABLE"
    autostart: bool = False
    activate_cmd: str = "source .venv/bin/activate"
    env_file: str = ".env-example-unix"
    python_cmd: str = "python3"
    create_env: str = "python3 -m venv .venv"
    git_url: str = "https://github.com/techfreaque/octane"

    @property
    def venv_path(self) -> str:
        return os.path.join(self.install_path, ".venv")
