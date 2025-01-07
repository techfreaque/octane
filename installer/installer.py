import os
import platform
from tkinter import messagebox
from installer_utils.config import InstallConfig
from installer_utils.gui import InstallerGUI, ProgressWindow
from installer_utils.platforms import WindowsHandler, LinuxHandler, MacHandler


class Installer:
    def __init__(self):
        self.handlers = {
            "Windows": WindowsHandler(),
            "Linux": LinuxHandler(),
            "Darwin": MacHandler(),
        }
        self.current_platform = platform.system()
        self.handler = self.handlers.get(self.current_platform)
        if not self.handler:
            raise RuntimeError(f"Unsupported platform: {self.current_platform}")

    def install(self, config: InstallConfig):
        with ProgressWindow() as progress:
            try:
                self.handler.ensure_dependencies()
                self.handler.setup_environment(config)

                if not os.path.exists(os.path.join(config.install_path, ".git")):
                    self._clone_repository(config)
                else:
                    self._update_repository(config)

                self.handler.install_packages(config)

                if config.autostart:
                    self.handler.setup_autostart(config)

            except Exception as ex:
                messagebox.showerror("Error", f"Installation failed: {ex}")
                raise


def main():
    gui = InstallerGUI()
    config = gui.show()
    if config:
        installer = Installer()
        installer.install(config)


if __name__ == "__main__":
    main()
