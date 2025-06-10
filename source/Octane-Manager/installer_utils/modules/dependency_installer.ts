import { execSync } from 'child_process';
import { ProgressHandler } from './progress_handler';
import { check_dependency_installed, run_command } from '../utils';
import { InstallConfig } from '../config';

class DependencyInstaller {
    install_dependencies(config: InstallConfig, progress: ProgressHandler): void {
        this.install_system_dependencies(config, progress);
        progress.update_progress("Basic Octane dependencies installed.");
        this.check_and_install_code_server(progress);
    }

    install_system_dependencies(config: InstallConfig, progress: ProgressHandler): void {
        // Implementation needed
    }

    check_and_install_code_server(progress: ProgressHandler): void {
        if (!check_dependency_installed("which code-server")) {
            this.install_vs_code_server();
            progress.update_progress("VSCode server installed.");
        } else {
            progress.update_progress("VSCode server already installed.");
        }
    }

    install_vs_code_server(): void {
        /** Install code-server on Linux/macOS using official script. */
        run_command("curl -fsSL https://code-server.dev/install.sh | sh");
    }

    _is_code_server_installed(): boolean {
        /** Check if code-server is installed. */
        try {
            execSync("code-server --version", { stdio: 'ignore' });
            return true;
        } catch (error) {
            return false;
        }
    }
}
