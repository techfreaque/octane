import os
import platform
import shutil
from ..utils import run_command
from ..config import InstallConfig


class PlatformHandler:
    def install_dependencies(self, config: InstallConfig):
        pass

    def setup_environment(self, config: InstallConfig):
        config.activate_cmd = self.get_activate_cmd(config)
        config.create_env = self.get_create_env_cmd(config)
        config.python_cmd = self.get_python_cmd()
        config.env_file = self.get_env_file()
        self._setup_environment(config)

    def setup_autostart(self, config: InstallConfig):
        pass

    def install_packages(
        self,
        config: InstallConfig,
        update_progress_callback,
        current_percent: int,
        current_step: int,
        total_steps: int,
    ):
        current_step = self._install_dev_env_packages(
            config,
            update_progress_callback,
            current_percent,
            current_step,
            total_steps,
            percentage_for_tasks=10,
        )
        current_step = self._install_stable_packages(
            config,
            update_progress_callback,
            current_percent,
            current_step,
            total_steps,
        )
        return current_step

    def run_additional_install_step(self, config: InstallConfig):
        try:
            os.chdir(config.install_path)
            activate_cmd = self.get_activate_cmd(config=config)
            separator = ";" if platform.system() == "Windows" else ":"
            pythonpath = separator.join([
                "${PWD}/octobot-packages/Async-Channel",
                "${PWD}/octobot-packages/OctoBot-Tentacles-Manager",
                "${PWD}/octobot-packages/OctoBot-Commons",
                "${PWD}/octobot-packages/OctoBot-Trading",
                "${PWD}/octobot-packages/OctoBot-Backtesting",
                "${PWD}/octobot-packages/OctoBot-evaluators",
                "${PWD}/octobot-packages/OctoBot-Services",
                "${PWD}/octobot-packages/trading-backend"
            ])
            run_command(f"{activate_cmd} && "
                        f"PYTHONPATH={pythonpath} "
                        f"{config.python_cmd} octobot-packages/OctoBot/start.py tentacles -p ./any_platform.zip -d ./octobot-packages/reference_tentacles && "
                        f"{config.python_cmd} octobot-packages/OctoBot/start.py tentacles --install --all --location ./output/any_platform.zip")
            shutil.rmtree('./output', ignore_errors=True)
        except Exception as ex:
            raise RuntimeError(f"Additional install step failed: {ex}")

    def clone_repository(self, config: InstallConfig):
        os.makedirs(config.install_path, exist_ok=True)
        os.chdir(config.install_path)
        run_command(f"git clone -b {config.branch} {config.git_url} .")


    def update_repository(self, config: InstallConfig):
        os.chdir(config.install_path)
        run_command("git stash || echo 'No changes to stash'")
        run_command(f"git pull origin {config.branch}")

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
        if not os.path.exists(target_env):
            source_env = os.path.join(
                config.install_path, "installer", "installer_utils", self.get_env_file()
            )
            shutil.copyfile(source_env, target_env)

        # Set up virtual environment
        run_command(config.create_env)

    def _install_stable_packages(
        self,
        config: InstallConfig,
        update_progress_callback,
        current_percent: int,
        current_step: int,
        total_steps: int,
    ):
        packages = [
            "OctoBot",
            "OctoBot-Backtesting",
            "OctoBot-Commons",
            "OctoBot-evaluators",
            "OctoBot-Services",
            "OctoBot-Tentacles-Manager",
            "OctoBot-Trading",
            "Async-Channel",
        ]

        # Install basic requirements
        current_percent += 2.5
        current_step += 1
        update_progress_callback(
            current_percent, current_step, total_steps, "Upgrading pip and wheel"
        )
        run_command(
            f"{config.activate_cmd} && {config.python_cmd} -m pip install --upgrade pip wheel"
        )

        # Uninstall existing packages
        current_percent += 2.5
        current_step += 1
        update_progress_callback(
            current_percent,
            current_step,
            total_steps,
            "cleaning existing package links",
        )
        run_command(
            f"{config.activate_cmd} && {config.python_cmd} -m pip uninstall -y octane OctoBot OctoBot-Backtesting "
            "OctoBot-Trading Async-Channel OctoBot-Evaluators OctoBot-Commons "
            "OctoBot-Tentacles-Manager OctoBot-Services"
        )

        # Install package requirements
        for i, package in enumerate(packages, start=1):
            current_percent += 2.5
            current_step += 1
            update_progress_callback(
                current_percent,
                current_step,
                total_steps,
                f"Installing requirements for {package}",
            )
            run_command(
                f"{config.activate_cmd} && {config.python_cmd} -m pip install -r octobot-packages/{package}/requirements.txt"
            )

        # Install Octane requirements
        current_percent += 10
        current_step += 1
        update_progress_callback(
            current_percent,
            current_step,
            total_steps,
            "Installing Octane requirements (this can take a while)",
        )
        run_command(
            f"{config.activate_cmd} && {config.python_cmd} -m pip install -r octobot-packages/OctoBot/strategy_maker_requirements.txt"
        )

        # Install packages
        for package in packages:
            current_percent += 2.5
            current_step += 1
            update_progress_callback(
                current_percent,
                current_step,
                total_steps,
                f"Installing {package}",
            )
            run_command(
                f"{config.activate_cmd} && {config.python_cmd} -m pip install -e octobot-packages/{package}/"
            )
        return current_step

    def _install_dev_env_packages(
        self,
        config: InstallConfig,
        update_progress_callback,
        current_percent: int,
        current_step: int,
        total_steps: int,
        percentage_for_tasks: int,
    ):
        steps = [
            {
                "description": "Upgrading pip and wheel",
                "percentage": 10,
                "command": f"{config.activate_cmd} && {config.python_cmd} -m pip install --upgrade pip wheel",
            },
            {
                "description": "Installing development requirements",
                "percentage": 40,
                "command": f"{config.activate_cmd} && {config.python_cmd} -m pip install -r requirements-dev.txt",
            },
            {
                "description": "Installing pre-commit hooks",
                "percentage": 10,
                "command": f"{config.activate_cmd} && {config.python_cmd} -m pip install pre-commit && pre-commit install",
            },
            {
                "description": "Installing development packages",
                "percentage": 40,
                "command": f"{config.activate_cmd} && {config.python_cmd} -m pip install -e .",
            },
        ]
        packages = [
            "OctoBot-Backtesting",
            "OctoBot-Commons",
            "OctoBot-evaluators",
            "OctoBot-Services",
            "OctoBot-Tentacles-Manager",
            "OctoBot-Trading",
            "OctoBot",
        ]

        # Install dev requirements
        for package in packages:
            update_progress_callback(
                current_percent,
                current_step,
                total_steps,
                f"Installing dev requirements for {package}",
            )
            run_command(
                f"{config.activate_cmd} && {config.python_cmd} -m pip install -r {config.install_path}/octobot-packages/{package}/dev_requirements.txt"
            )
            current_percent += int(percentage_for_tasks / len(packages))
            current_step += 1

        return current_step

    def get_activate_cmd(self):
        raise NotImplementedError

    def get_create_env_cmd(self):
        raise NotImplementedError

    def get_python_cmd(self):
        raise NotImplementedError

    def get_env_file(self):
        raise NotImplementedError
