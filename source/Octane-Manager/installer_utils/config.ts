import * as path from 'path';

class InstallConfig {
    install_path: string;
    branch: string;
    autostart: boolean;
    activate_cmd: string;
    env_file: string;
    python_cmd: string;
    create_env: string;
    git_url: string;
    timesync: boolean;
    dev_env: boolean;
    repair: boolean;

    constructor(
        install_path: string,
        branch: string = "main",
        autostart: boolean = false,
        activate_cmd: string = "source .venv/bin/activate",
        env_file: string = ".env-example-unix",
        python_cmd: string = "python3",
        create_env: string = "python3 -m venv .venv",
        git_url: string = "https://github.com/techfreaque/octane",
        timesync: boolean = true,
        dev_env: boolean = false,
        repair: boolean = false
    ) {
        this.install_path = install_path;
        this.branch = branch;
        this.autostart = autostart;
        this.activate_cmd = activate_cmd;
        this.env_file = env_file;
        this.python_cmd = python_cmd;
        this.create_env = create_env;
        this.git_url = git_url;
        this.timesync = timesync;
        this.dev_env = dev_env;
        this.repair = repair;
    }

    get venv_path(): string {
        return path.join(this.install_path, ".venv");
    }
}

enum Channels {
    STABLE = "main",
    BETA = "dev"
}

export { InstallConfig, Channels };
