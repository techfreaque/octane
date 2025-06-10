import * as fs from 'fs';
import * as path from 'path';
import * as shutil from 'fs-extra';
import { EnvironmentUtil } from './environment_util';
import { ProgressHandler } from './progress_handler';
import { InstallConfig } from '../config';
import { run_command } from '../utils';

class OctaneInstaller {
    install_packages(config: InstallConfig, progress: ProgressHandler): void {
        this._uninstall_packages(config, progress);
        this._update_pip_and_wheel(config, progress);
        this._install_requirements(config, progress);
        this._install_packages(config, progress);
        this._update_tentacles(config, progress);
    }

    private _update_pip_and_wheel(config: InstallConfig, progress: ProgressHandler): void {
        progress.update_progress("Upgrading pip and wheel");
        run_command(`${config.activate_cmd} && ${config.python_cmd} -m pip install --upgrade pip wheel`);
    }

    private _uninstall_packages(config: InstallConfig, progress: ProgressHandler): void {
        progress.update_progress("Cleaning existing package links");
        run_command(
            `${config.activate_cmd} && ${config.python_cmd} -m pip uninstall -y octane OctoBot OctoBot-Backtesting ` +
            "OctoBot-Trading Async-Channel OctoBot-Evaluators OctoBot-Commons " +
            "OctoBot-Tentacles-Manager OctoBot-Services"
        );
    }

    private _install_packages(config: InstallConfig, progress: ProgressHandler): void {
        const octane_packages = [
            "Async-Channel",
            "OctoBot-Tentacles-Manager",
            "OctoBot-Commons",
            "OctoBot-Trading",
            "OctoBot-Backtesting",
            "OctoBot-evaluators",
            "OctoBot-Services",
            "trading-backend"
        ];

        for (const package of octane_packages) {
            run_command(`${config.activate_cmd} && ${config.python_cmd} -m pip install -e octobot-packages/${package}/`);
            progress.update_progress(`Installed ${package}`);
        }
    }

    private _install_requirements(config: InstallConfig, progress: ProgressHandler): void {
        const octane_packages: { [key: string]: string[] } = {
            "Async-Channel": ["requirements.txt"],
            "OctoBot-Tentacles-Manager": ["requirements.txt"],
            "OctoBot-Commons": ["requirements.txt"],
            "OctoBot-Trading": ["requirements.txt"],
            "OctoBot-Backtesting": ["requirements.txt"],
            "OctoBot-evaluators": ["requirements.txt"],
            "OctoBot-Services": ["requirements.txt"],
            "trading-backend": ["requirements.txt"]
        };

        for (const [package_name, requirements] of Object.entries(octane_packages)) {
            progress.update_progress(`Installing dev requirements for ${package_name}`);
            for (const requirement of requirements) {
                run_command(`${config.activate_cmd} && ${config.python_cmd} -m pip install -r ${config.install_path}/source/${package_name}/${requirement}`);
            }
        }
    }

    private _update_tentacles(config: InstallConfig, progress: ProgressHandler): void {
        try {
            process.chdir(config.install_path);
            const separator = EnvironmentUtil.get_env_file_separator();
            const pythonpath = [
                "${PWD}/octobot-packages/Async-Channel",
                "${PWD}/octobot-packages/OctoBot-Tentacles-Manager",
                "${PWD}/octobot-packages/OctoBot-Commons",
                "${PWD}/octobot-packages/OctoBot-Trading",
                "${PWD}/octobot-packages/OctoBot-Backtesting",
                "${PWD}/octobot-packages/OctoBot-evaluators",
                "${PWD}/octobot-packages/OctoBot-Services",
                "${PWD}/octobot-packages/trading-backend"
            ].join(separator);
            const activate_cmd = EnvironmentUtil.get_activate_cmd(config);
            run_command(
                `${activate_cmd} && ` +
                `PYTHONPATH=${pythonpath} ` +
                `Octane tentacles -p ./any_platform.zip -d ./octobot-packages/reference_tentacles && ` +
                `Octane tentacles --install --all --location ./output/any_platform.zip`
            );
            shutil.removeSync("./output");
        } catch (ex) {
            progress.update_progress("Failed to update tentacles (extensions)");
            throw new Error(`Installing extensions step failed: ${ex}`);
        }
    }
}
