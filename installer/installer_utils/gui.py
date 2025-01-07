import tkinter as tk
from tkinter import ttk, filedialog
import os
from typing import Optional
from .config import InstallConfig


class ProgressWindow:
    def __init__(self, title="Installing..."):
        self.window = tk.Toplevel()
        self.window.title(title)
        label = tk.Label(self.window, text="Please wait while installing/updating...")
        label.pack(pady=5)
        self.progress_bar = ttk.Progressbar(
            self.window, orient=tk.HORIZONTAL, length=300, mode="indeterminate"
        )
        self.progress_bar.pack(padx=10, pady=10)

    def __enter__(self):
        self.progress_bar.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress_bar.stop()
        self.window.destroy()


class InstallerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Octane Installer")
        self._setup_widgets()

    def _setup_widgets(self):
        # Install path
        tk.Label(self.root, text="Install Path:").grid(row=0, column=0, padx=5, pady=5)
        self.path_var = tk.StringVar(value=os.getcwd())
        path_entry = tk.Entry(self.root, textvariable=self.path_var, width=50)
        path_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Browse", command=self._browse).grid(
            row=0, column=2, padx=5, pady=5
        )

        # Autostart
        self.autostart_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            self.root, text="Add to autostart", variable=self.autostart_var
        ).grid(row=1, columnspan=3, padx=5, pady=5)

        # Branch
        tk.Label(self.root, text="Select Branch:").grid(row=2, column=0, padx=5, pady=5)
        self.branch_var = tk.StringVar(value="STABLE")
        branch_dropdown = tk.OptionMenu(self.root, self.branch_var, "STABLE", "BETA")
        branch_dropdown.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(text="Install / Update", command=self._on_install).grid(
            row=3, columnspan=3, pady=10
        )

    def _browse(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_var.set(folder)

    def _on_install(self):
        self.config = InstallConfig(
            install_path=self.path_var.get(),
            branch=self.branch_var.get(),
            autostart=self.autostart_var.get(),
        )
        self.root.destroy()

    def show(self) -> Optional[InstallConfig]:
        self.root.mainloop()
        return getattr(self, "config", None)
