import * as os from 'os';
import * as path from 'path';
import { InstallConfig } from '../config';
import { ProgressHandler } from './progress_handler';
import { run_command } from '../utils';

class InstallerBase {
    setup_autostart(config: InstallConfig, progress: ProgressHandler): void {
        // Implementation needed
    }

    create_starter_executable(config: InstallConfig, progress: ProgressHandler): void {
        /** Create a small script that sets env vars and calls Octane, then build a one-file executable. */
        const script_path = path.join(config.install_path, "start_octane.py");
        const pkg_sep = os.platform() === "win32" ? ";" : ":";
        const pythonpath = [
            `${config.install_path}/octobot-packages/Async-Channel`,
            `${config.install_path}/octobot-packages/OctoBot-Tentacles-Manager`,
            `${config.install_path}/octobot-packages/OctoBot-Commons`,
            `${config.install_path}/octobot-packages/OctoBot-Trading`,
            `${config.install_path}/octobot-packages/OctoBot-Backtesting`,
            `${config.install_path}/octobot-packages/OctoBot-evaluators`,
            `${config.install_path}/octobot-packages/OctoBot-Services`,
            `${config.install_path}/octobot-packages/trading-backend`,
        ].join(pkg_sep);

        // Write a small script that sets env vars and calls start.py
        const script_content = `
import os, sys, subprocess
if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    os.environ["EXIT_BEFORE_TENTACLES_AUTO_REINSTALL"] = "True"
    os.environ["PYTHONPATH"] = r"${pythonpath}"
    print('Starting Octane...')
    cmd = [sys.executable, "octobot-packages/OctoBot/start.py"]
    sys.exit(subprocess.call(cmd))
        `;
        fs.writeFileSync(script_path, script_content);

        // Run PyInstaller on the script to produce a single binary called "octane"
        run_command(
            `${config.activate_cmd} && ` +
            `${config.python_cmd} -m pip install pyinstaller && ` +
            `${config.python_cmd} -m PyInstaller --noconfirm --onefile ` +
            `--name octane ${script_path}`
        );

        // The compiled binary (octane or octane.exe) will be in dist/ under install_path
        // Move it up for convenience
        const dist_binary = path.join(
            config.install_path,
            "dist",
            os.platform() === "win32" ? "octane.exe" : "octane"
        );
        const final_binary = path.join(
            config.install_path,
            os.platform() === "win32" ? "octane.exe" : "octane"
        );

        if (fs.existsSync(dist_binary)) {
            fs.renameSync(dist_binary, final_binary);
        }

        console.log(`Created start binary at: ${final_binary}`);
    }
}
