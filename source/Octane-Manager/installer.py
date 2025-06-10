from .installer_utils.config import Channels, InstallConfig

ARG TENTACLES_URL_TAG=""
ENV TENTACLES_URL_TAG=$TENTACLES_URL_TAG
ENV SHARE_YOUR_OCOBOT=

class Installer:
    def get_default_config(self):
        self.config = InstallConfig(
            install_path=self.path_var.get(),
            branch=Channels.STABLE.value
            if self.branch_var.get() == "STABLE"
            else Channels.BETA.value,
            autostart=self.autostart_var.get(),
            timesync=self.timesync_var.get(),
            repair=self.repair_var.get(),
            dev_env=self.dev_env_var.get(),
        )
    def install(self, config: InstallConfig, on_progress: callable):
        try:
            steps = {
                "ensuring_dependencies": {
                    "description": "Ensuring dependencies",
                    "percentage": 10,
                },
                "install_vscode_server": {
                    "description": "Installing code-server",
                    "percentage": 5,
                },
                "downloading_octane": {
                    "description": "Downloading Octane",
                    "percentage": 10,
                },
                "setting_up_environment": {
                    "description": "Setting up environment",
                    "percentage": 10,
                },
                "installing_packages": {
                    "description": "Installing packages",
                    "percentage": 60 if config.autostart else 65,
                },
                "installing_octane_extensions": {
                    "description": "Installing Octane extensions",
                    "percentage": 10,
                },
                "generating_octane_binary": {
                    "description": "Generating the Octane start binary",
                    "percentage": 5,
                },
                **(
                    {
                        "setting_up_autostart": {
                            "description": "Setting up autostart",
                            "percentage": 5,
                        },
                    }
                    if config.autostart
                    else {}
                ),
            }

            general_steps = len(steps.keys())
            total_steps = general_steps + installing_packages_steps
            current_step = 1
            current_percent = 0

            for step_key, step in steps.items():
                self.update_progress(
                    current_percent,
                    current_step,
                    total_steps,
                    step["description"],
                )

                if step_key == "ensuring_dependencies":
                    self.handler.install_dependencies(config)
                elif step_key == "install_vscode_server":
                    self.handler.check_and_install_code_server()
                elif step_key == "downloading_octane":
                    if not os.path.exists(os.path.join(config.install_path, ".git")):
                        if os.path.exists(config.install_path):
                            raise RuntimeError(
                                f"Installation path {config.install_path} already exists and is not a Octane installation"
                            )
                        self._clone_repository(config)
                    else:
                        self._update_repository(config)
                elif step_key == "setting_up_environment":
                    self.handler.setup_environment(config)
                elif step_key == "installing_packages":
                    current_step = self.handler.install_packages(
                        config,
                        self.update_progress,
                        current_percent,
                        current_step,
                        total_steps,
                    )
                elif step_key == "installing_octane_extensions":
                    self.handler.run_additional_install_step(config)
                elif step_key == "generating_octane_binary":
                    self.handler.create_starter_executable(config)
                elif step_key == "setting_up_autostart" and config.autostart:
                    self.handler.setup_autostart(config)

                current_percent += step["percentage"]
                current_step += 1
            self.show_complete()

        except Exception as ex:
            self.command_listbox.insert(END, f"ERROR: Installation failed: {ex}")
            self.command_listbox.yview(END)
            self.show_retry()
