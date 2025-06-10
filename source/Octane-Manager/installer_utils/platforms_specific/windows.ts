import * as fs from 'fs';
import * as path from 'path';
import { InstallConfig } from '../config';
import { DependencyInstaller } from '../modules/dependency_installer';
import { EnvironmentUtil } from '../modules/environment_util';
import { InstallerBase } from '../modules/installer_base';
import { check_dependency_installed, run_command } from '../utils';

class WindowsInstallerBase extends InstallerBase {
    setup_autostart(config: InstallConfig): void {
        const startup_folder = path.join(
            process.env.APPDATA || "",
            "Microsoft",
            "Windows",
            "Start Menu",
            "Programs",
            "Startup"
        );
        const script_path = path.join(config.install_path, "start_octane.bat");
        const script_content = `@echo off\ncd /d "${config.install_path}"\ncall ${config.activate_cmd}\npython main.py\n`;
        fs.writeFileSync(script_path, script_content);
    }
}

class WindowsDependencyInstaller extends DependencyInstaller {
    install_system_dependencies(config: InstallConfig): void {
        const missing_dependencies = ["git", "python3"].filter(cmd => !check_dependency_installed(`which ${cmd}`));

        if (missing_dependencies.length > 0) {
            if (check_dependency_installed("choco --version")) {
                run_command("choco install git python visualstudio2022buildtools -y");
            } else if (check_dependency_installed("winget --info")) {
                run_command("winget install --id Git.Git -e --source winget");
                run_command("winget install --id Python.Python.3 -e --source winget");
                run_command("winget install --id Microsoft.VisualStudio.2022.BuildTools -e --source winget");
            } else {
                throw new Error("No package manager found (chocolatey/winget)");
            }
        }
    }

    install_vs_code_server(): void {
        /** Install code-server on Windows using chocolatey or winget. */
        if (check_dependency_installed("choco --version")) {
            run_command("choco install code-server -y");
        } else if (check_dependency_installed("winget --info")) {
            run_command("winget install --id Coder.code-server -e --source winget");
        } else {
            throw new Error("No package manager found (chocolatey/winget)");
        }
    }
}

class WindowsEnvironmentUtil extends EnvironmentUtil {
    static get_env_file_separator(): string {
        return ";";
    }

    static get_activate_cmd(config: InstallConfig): string {
        return `source ${config.install_path}/.venv/Scripts/activate`;
    }

    static get_create_env_cmd(config: InstallConfig): string {
        return `python -m venv ${config.install_path}/.venv`;
    }

    static get_python_cmd(): string {
        return "python";
    }

    static get_env_file(): string {
        return ".env-example-windows";
    }
}
