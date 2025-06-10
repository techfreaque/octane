import { exec, ExecException } from 'child_process';

async function runCommand(cmd: string): Promise<void> {
    console.log(`Running command: ${cmd}`);
    return new Promise((resolve, reject) => {
        exec(cmd, (error: ExecException | null, stdout: string, stderr: string) => {
            if (error) {
                console.error(`Error: ${error.message}`);
                console.error(`Stderr: ${stderr}`);
                reject(new Error(`Command failed with return code ${error.code}: ${cmd}`));
                return;
            }
            console.log(`Stdout: ${stdout}`);
            resolve();
        });
    });
}

async function checkDependencyInstalled(command: string): Promise<boolean> {
    return new Promise((resolve) => {
        exec(command, (error: ExecException | null) => {
            if (error) {
                resolve(false);
                return;
            }
            resolve(true);
        });
    });
}

export { runCommand, checkDependencyInstalled };