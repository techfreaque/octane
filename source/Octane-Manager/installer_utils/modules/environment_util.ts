import * as fs from 'fs';
import * as path from 'path';
import * as shutil from 'fs-extra';
import { InstallConfig } from '../config';
import { ProgressHandler } from './progress_handler';
import { run_command } from '../utils';

class EnvironmentUtil {
    static setup_environment(config: InstallConfig, progress: ProgressHandler): void {
        config.activate_cmd = this.get_activate_cmd(config);
        config.create_env = this.get_create_env_cmd(config);
        config.python_cmd = this.get_python_cmd();
        // TODO export to current env
        config.env_file = this.get_env_file();
        this._setup_environment(config);
        progress.update_progress("Environment setup complete.");
    }

    static get_activate_cmd(config: InstallConfig): string {
        return `source ${config.install_path}/.venv/bin/activate`;
    }

    static get_create_env_cmd(config: InstallConfig): string {
        return `python3 -m venv ${config.install_path}/.venv`;
    }

    static get_python_cmd(): string {
        return "python3";
    }

    static get_env_file(): string {
        return ".env-example-unix";
    }

    static get_env_file_separator(): string {
        return ":";
    }

    static export_env(config: InstallConfig): void {
        // TODO
    }

    private static _setup_environment(config: InstallConfig): void {
        fs.mkdirSync(path.join(config.install_path, "user"), { recursive: true });

        // Copy default configs
        const target_config = path.join(config.install_path, "user", "config.json");
        const source_config = path.join(
            config.install_path,
            "octobot-packages",
            "OctoBot",
            "octobot",
            "config",
            "default_config.json"
        );
        if (!fs.existsSync(target_config)) {
            shutil.copyFileSync(source_config, target_config);
        }

        // Copy .env file
        const target_env = path.join(config.install_path, ".env");
        if (!fs.existsSync(target_env)) {
            const source_env = path.join(
                config.install_path, "installer", "installer_utils", this.get_env_file()
            );
            shutil.copyFileSync(source_env, target_env);
        }

        // Set up virtual environment
        run_command(config.create_env);
    }
}
