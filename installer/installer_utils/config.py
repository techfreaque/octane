from dataclasses import dataclass
import enum
import os


@dataclass
class InstallConfig:
    install_path: str
    branch: str = "main"
    autostart: bool = False
    activate_cmd: str = "source .venv/bin/activate"
    env_file: str = ".env-example-unix"
    python_cmd: str = "python3"
    create_env: str = "python3 -m venv .venv"
    git_url: str = "https://github.com/techfreaque/octane"
    timesync: bool = True
    dev_env: bool = False
    repair: bool = False

    @property
    def venv_path(self) -> str:
        return os.path.join(self.install_path, ".venv")


class Channels(enum.Enum):
    STABLE = "main"
    BETA = "dev"
