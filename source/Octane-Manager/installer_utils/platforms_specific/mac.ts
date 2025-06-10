import * as fs from 'fs';
import * as path from 'path';
import { EnvironmentUtil } from '../modules/environment_util';
import { InstallConfig } from '../config';
import { DependencyInstaller } from '../modules/dependency_installer';
import { InstallerBase } from '../modules/installer_base';
import { check_dependency_installed, run_command } from '../utils';

class MacInstallerBase extends InstallerBase {
    setup_autostart(config: InstallConfig): void {
        const plist_dir = path.join(os.homedir(), "Library", "LaunchAgents");
        fs.mkdirSync(plist_dir, { recursive: true });
        const plist_path = path.join(plist_dir, "com.octane.startup.plist");
        const plist_content = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.octane.startup</string>
    <key>ProgramArguments</key>
    <array>
        <string>${path.join(config.install_path, '.venv/bin/python')}</string>
        <string>${path.join(config.install_path, 'main.py')}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>`;
        fs.writeFileSync(plist_path, plist_content);
    }
}

class MacDependencyInstaller extends DependencyInstaller {
    install_system_dependencies(config: InstallConfig): void {
        const missing_dependencies = ["git", "python3"].filter(cmd => !check_dependency_installed(`which ${cmd}`));

        if (missing_dependencies.length > 0) {
            if (!check_dependency_installed("which brew")) {
                throw new Error(
                    `The following dependencies are missing: ${missing_dependencies.join(', ')}, either install them or install brew and run the installer again.`
                );
            }
            run_command("brew install git python");
        }
    }
}

class MacEnvironmentUtil extends EnvironmentUtil {
    // Additional macOS-specific environment setup can be added here
}
