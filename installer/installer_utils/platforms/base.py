import os
import shutil

from ..utils import run_command
from ..config import InstallConfig


class PlatformHandler:
    def install_dependencies(self, config: InstallConfig):
        pass

    def setup_environment(self, config: InstallConfig):
        pass

    def setup_autostart(self, config: InstallConfig):
        pass

    def install_packages(self, config: InstallConfig):
        if config.branch == "dev":
            self._install_beta_packages(config.activate_cmd)
        else:
            self._install_stable_packages(config.activate_cmd)

    def _clone_repository(self, config: InstallConfig):
        os.makedirs(config.install_path, exist_ok=True)
        os.chdir(config.install_path)
        run_command(f"git clone {config.git_url} .")

    def _update_repository(self, config: InstallConfig):
        os.chdir(config.install_path)
        run_command("git stash || echo 'No changes to stash'")
        run_command("git pull")

    def _setup_environment(self, config: InstallConfig):
        os.makedirs(os.path.join(config.install_path, "user"), exist_ok=True)

        # Copy default configs
        target_config = os.path.join(config.install_path, "user", "config.json")
        source_config = os.path.join(
            config.install_path,
            "octobot-packages",
            "OctoBot",
            "octobot",
            "config",
            "default_config.json",
        )
        if not os.path.exists(target_config):
            shutil.copyfile(source_config, target_config)

        # Copy .env file
        target_env = os.path.join(config.install_path, ".env")
        source_env = os.path.join("scripts", config.env_file)
        if not os.path.exists(target_env):
            shutil.copyfile(source_env, target_env)

        # Set up virtual environment
        run_command(config.create_env)

    def _install_stable_packages(self, config: InstallConfig):
        # Install basic requirements
        run_command(
            f"{config.activate_cmd} && {config.python_cmd} -m pip install --upgrade pip wheel"
        )

        # Uninstall existing packages
        run_command(
            f"{config.activate_cmd} && {config.python_cmd} -m pip uninstall -y octane OctoBot OctoBot-Backtesting "
            "OctoBot-Trading Async-Channel OctoBot-Evaluators OctoBot-Commons "
            "OctoBot-Tentacles-Manager OctoBot-Services"
        )
        # Install package requirements
        for package in [
            "OctoBot",
            "OctoBot-Backtesting",
            "OctoBot-Commons",
            "OctoBot-evaluators",
            "OctoBot-Services",
            "OctoBot-Tentacles-Manager",
            "OctoBot-Trading",
            "Async-Channel",
        ]:
            run_command(
                f"{config.activate_cmd} && {config.python_cmd} -m pip install -r octobot-packages/{package}/requirements.txt"
            )

        # Install strategy maker requirements
        run_command(
            f"{config.activate_cmd} && {config.python_cmd} -m pip install -r octobot-packages/OctoBot/strategy_maker_requirements.txt"
        )

        # Install packages in development mode
        for package in [
            "trading-backend",
            "Async-Channel",
            "OctoBot-Commons",
            "OctoBot-Tentacles-Manager",
            "OctoBot-Backtesting",
            "OctoBot-Trading",
            "OctoBot-Services",
            "OctoBot-evaluators",
            "OctoBot",
        ]:
            run_command(
                f"{config.activate_cmd} && {config.python_cmd} -m pip install -e octobot-packages/{package}/"
            )

    def _install_beta_packages(self, config: InstallConfig):
        # Install dev requirements
        for package in [
            "OctoBot-Backtesting",
            "OctoBot-Commons",
            "OctoBot-evaluators",
            "OctoBot-Services",
            "OctoBot-Tentacles-Manager",
            "OctoBot-Trading",
            "OctoBot",
        ]:
            run_command(
                f"{config.activate_cmd} && {config.python_cmd} -m pip install -r octobot-packages/{package}/dev_requirements.txt"
            )

        # Install regular requirements and packages
        self._install_stable_packages(config.activate_cmd)
