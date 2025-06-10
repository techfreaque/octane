import * as fs from 'fs';
import * as path from 'path';
import { ProgressHandler } from './progress_handler';
import { run_command } from '../utils';
import { InstallConfig } from '../config';

class OctaneDownloader {
    download_octane(config: InstallConfig, progress: ProgressHandler): void {
        if (!fs.existsSync(path.join(config.install_path, ".git"))) {
            if (fs.existsSync(config.install_path)) {
                throw new Error(
                    `Installation path ${config.install_path} already exists and is not an Octane installation`
                );
            }
            this._clone_repository(config, progress);
        } else {
            this._update_repository(config, progress);
        }
    }

    private _clone_repository(config: InstallConfig, progress: ProgressHandler): void {
        try {
            this.clone_repository(config);
            progress.update_progress("Octane successfully downloaded.");
        } catch (exception) {
            progress.on_error("ERROR: Failed to download octane.");
            throw new Error(`ERROR: Failed to download octane: ${exception}`);
        }
    }

    private _update_repository(config: InstallConfig, progress: ProgressHandler): void {
        try {
            this.update_repository(config);
            progress.update_progress("Octane successfully updated.");
        } catch (exception) {
            progress.on_error("ERROR: Failed to update octane.");
            throw new Error(`ERROR: Failed to update octane: ${exception}`);
        }
    }

    clone_repository(config: InstallConfig): void {
        fs.mkdirSync(config.install_path, { recursive: true });
        process.chdir(config.install_path);
        run_command(`git clone -b ${config.branch} ${config.git_url} .`);
    }

    update_repository(config: InstallConfig): void {
        process.chdir(config.install_path);
        run_command("git stash || echo 'No changes to stash'");
        run_command(`git pull origin ${config.branch}`);
    }
}
