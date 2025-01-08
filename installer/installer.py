import os
import platform
import tkinter as tk
from tkinter import ttk, filedialog, END
from installer_utils.utils import run_command
from installer_utils.platforms.base import PlatformHandler
from installer_utils.config import InstallConfig, Channels
from installer_utils.platforms import WindowsHandler, LinuxHandler, MacHandler


class InstallerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Octane Installer")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.setup_page = ttk.Frame(self.notebook)
        self.progress_page = ttk.Frame(self.notebook)
        self.done_page = ttk.Frame(self.notebook)

        self.notebook.add(self.setup_page, text="Setup")
        self.notebook.add(self.progress_page, text="Progress")
        self.notebook.add(self.done_page, text="Done")
        self.notebook.hide(self.progress_page)
        self.notebook.hide(self.done_page)

        self._setup_widgets()
        self._progress_widgets()
        self._done_widgets()

        self.handlers = {
            "Windows": WindowsHandler(),
            "Linux": LinuxHandler(),
            "Darwin": MacHandler(),
        }
        self.current_platform = platform.system()
        self.handler: PlatformHandler = self.handlers.get(self.current_platform)
        if not self.handler:
            raise RuntimeError(f"Unsupported platform: {self.current_platform}")

    def _setup_widgets(self):
        # Setup page widgets
        tk.Label(self.setup_page, text="Install Path:").grid(
            row=0, column=0, padx=5, pady=5
        )
        self.path_var = tk.StringVar(value=os.getcwd())
        path_entry = tk.Entry(self.setup_page, textvariable=self.path_var, width=50)
        path_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self.setup_page, text="Browse", command=self._browse).grid(
            row=0, column=2, padx=5, pady=5
        )

        self.autostart_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            self.setup_page, text="Add to autostart", variable=self.autostart_var
        ).grid(row=1, columnspan=3, padx=5, pady=5)

        tk.Label(self.setup_page, text="Select Branch:").grid(
            row=2, column=0, padx=5, pady=5
        )
        self.branch_var = tk.StringVar(value="STABLE")
        branch_dropdown = tk.OptionMenu(
            self.setup_page, self.branch_var, "STABLE", "BETA"
        )
        branch_dropdown.grid(row=2, column=1, padx=5, pady=5)

        self.timesync_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            self.setup_page,
            text="Enable Time Synchronization",
            variable=self.timesync_var,
        ).grid(row=3, columnspan=3, padx=5, pady=5)

        self.dev_env_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            self.setup_page,
            text="Setup Development Environment",
            variable=self.dev_env_var,
        ).grid(row=4, columnspan=3, padx=5, pady=5)

        tk.Button(
            self.setup_page, text="Install / Update", command=self._on_install
        ).grid(
            row=5, columnspan=3, pady=10
        )  # Update row number

    def _progress_widgets(self):
        # Progress page widgets
        tk.Label(
            self.progress_page, text="Please wait while installing/updating..."
        ).pack(pady=5)

        self.progress_bar = ttk.Progressbar(
            self.progress_page, orient=tk.HORIZONTAL, length=300, mode="determinate"
        )
        self.progress_bar.pack(padx=10, pady=10)
        self.progress_label = tk.Label(self.progress_page, text="Progress: 0%")
        self.progress_label.pack()

        self.command_listbox = tk.Listbox(self.progress_page, width=60)
        self.command_listbox.pack(padx=10, pady=5)

    def _done_widgets(self):
        # Done page widgets
        self.done_label = tk.Label(self.done_page, text="")
        self.done_label.pack(pady=5)

        self.command_listbox_done = tk.Listbox(self.done_page, width=60)
        self.command_listbox_done.pack(padx=10, pady=5)

        self.complete_button = tk.Button(
            self.done_page,
            text="Close Installer",
            command=self.root.destroy,
        )
        self.complete_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.retry_button = tk.Button(
            self.done_page, text="Retry", command=self.retry, state=tk.DISABLED
        )
        self.retry_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def _browse(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_var.set(folder)

    def _on_install(self):
        self.config = InstallConfig(
            install_path=self.path_var.get(),
            branch=Channels.STABLE.value
            if self.branch_var.get() == "STABLE"
            else Channels.BETA.value,
            autostart=self.autostart_var.get(),
            timesync=self.timesync_var.get(),
            dev_env=self.dev_env_var.get(),
        )
        self.notebook.hide(self.setup_page)
        self.notebook.hide(self.done_page)
        self.notebook.select(self.progress_page)
        self.install(self.config)

    def update_progress(
        self, current_percent: int, current_step: int, total_steps: int, command: str
    ):
        percentage = int((current_percent / 100) * 100)
        self.progress_bar["maximum"] = 100
        self.progress_bar["value"] = current_percent
        self.progress_label.config(text=f"Progress: {percentage}%")
        self.command_listbox.insert(
            tk.END, f"Step {current_step}/{total_steps} ({current_percent}%): {command}"
        )
        self.command_listbox.yview(tk.END)
        self.root.update_idletasks()

    def show_retry(self):
        self.done_label.config(text="Installation failed. Please try again.")
        self.complete_button.config(state=tk.NORMAL)
        self.retry_button.config(state=tk.NORMAL)
        self.command_listbox_done.delete(0, tk.END)
        for item in self.command_listbox.get(0, tk.END):
            self.command_listbox_done.insert(tk.END, item)
        self.notebook.hide(self.setup_page)
        self.notebook.hide(self.progress_page)
        self.notebook.select(self.done_page)

    def show_complete(self):
        self.command_listbox.insert(
            tk.END, f"100% Installation completed successfully!"
        )
        self.done_label.config(text="Installation completed successfully!")
        self.complete_button.config(state=tk.NORMAL)
        self.retry_button.pack_forget()
        self.command_listbox_done.delete(0, tk.END)
        for item in self.command_listbox.get(0, tk.END):
            self.command_listbox_done.insert(tk.END, item)
        self.notebook.hide(self.setup_page)
        self.notebook.hide(self.progress_page)
        self.notebook.select(self.done_page)

    def retry(self):
        self.retry_button.config(state=tk.DISABLED)
        self.progress_bar["value"] = 0
        self.progress_label.config(text="Progress: 0%")
        self.command_listbox.delete(0, tk.END)
        self.notebook.hide(self.done_page)
        self.notebook.hide(self.progress_page)
        self.notebook.select(self.setup_page)

    def install(self, config: InstallConfig):
        try:
            steps = [
                {"description": "Ensuring dependencies", "percentage": 10},
                {"description": "Cloning repository", "percentage": 10},
                {"description": "Updating repository", "percentage": 10},
                {"description": "Setting up environment", "percentage": 10},
                {"description": "Installing packages", "percentage": 50},
                {"description": "Running additional install step", "percentage": 10},
                {"description": "Setting up autostart", "percentage": 10},
            ]

            total_steps = len(steps)
            current_step = 1
            current_percent = 0

            for step in steps:
                self.update_progress(
                    current_percent + step["percentage"],
                    current_step,
                    total_steps,
                    step["description"],
                )

                if step["description"] == "Ensuring dependencies":
                    self.handler.install_dependencies(config)
                elif step["description"] == "Cloning repository":
                    if not os.path.exists(os.path.join(config.install_path, ".git")):
                        if os.path.exists(config.install_path):
                            raise RuntimeError(
                                f"Installation path {config.install_path} already exists and is not a Octane installation"
                            )
                        self._clone_repository(config)
                    else:
                        self._update_repository(config)
                elif step["description"] == "Setting up environment":
                    self.handler.setup_environment(config)
                elif step["description"] == "Installing packages":
                    current_step = self.handler.install_packages(
                        config,
                        self.update_progress,
                        current_percent,
                        current_step,
                        total_steps,
                    )
                elif step["description"] == "Running additional install step":
                    self.handler.run_additional_install_step(config)
                elif step["description"] == "Setting up autostart" and config.autostart:
                    self.handler.setup_autostart(config)

                current_percent += step["percentage"]
                current_step += 1

            self.show_complete()

        except Exception as ex:
            self.command_listbox.insert(END, f"ERROR: Installation failed: {ex}")
            self.command_listbox.yview(END)
            self.show_retry()

    def _clone_repository(self, config: InstallConfig):
        try:
            self.handler.clone_repository(config)
        except Exception as ex:
            self.command_listbox.insert(END, f"ERROR: Cloning repository failed: {ex}")
            self.command_listbox.yview(END)
            raise

    def _update_repository(self, config: InstallConfig):
        try:
            self.handler.update_repository(config)
        except Exception as ex:
            self.command_listbox.insert(END, f"ERROR: Updating repository failed: {ex}")
            self.command_listbox.yview(END)
            raise

    def show(self):
        self.root.mainloop()


def main():
    gui = InstallerGUI()
    gui.show()


if __name__ == "__main__":
    main()
