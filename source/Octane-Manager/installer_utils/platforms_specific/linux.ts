import * as fs from 'fs';
import * as path from 'path';
import { EnvironmentUtil } from '../modules/environment_util';
import { InstallerBase } from '../modules/installer_base';
import { DependencyInstaller } from '../modules/dependency_installer';
import { InstallConfig } from '../config';
import { check_dependency_installed, run_command } from '../utils';

class LinuxInstallerBase extends InstallerBase {
    setup_autostart(config: InstallConfig): void {
        const autostart_dir = path.join(os.homedir(), ".config", "autostart");
        fs.mkdirSync(autostart_dir, { recursive: true });
        const desktop_file = path.join(autostart_dir, "octane.desktop");
        const desktop_content = `
[Desktop Entry]
Type=Application
Exec=${path.join(config.install_path, '.venv/bin/python')} ${path.join(config.install_path, 'main.py')}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Octane
        `;
        fs.writeFileSync(desktop_file, desktop_content);
    }
}

class LinuxDependencyInstaller extends DependencyInstaller {
    install_system_dependencies(config: InstallConfig): void {
        const missing_dependencies = ["git", "python3"].filter(cmd => !check_dependency_installed(`which ${cmd}`));

        if (missing_dependencies.length > 0) {
            throw new Error(`Missing required dependencies: ${missing_dependencies.join(', ')}`);
        }

        if (config.timesync) {
            run_command("timedatectl set-ntp true");
        }
    }
}

class LinuxEnvironmentUtil extends EnvironmentUtil {
    // Additional Linux-specific environment setup can be added here
}
