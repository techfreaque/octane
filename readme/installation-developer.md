# Installation (Developer)

### install requirements

#### Download and install:

* SCM: [Git](https://git-scm.com/downloads)
* Programming language: [Python 3.10](https://www.python.org/downloads/release/python-3109/)
* Download [Visual Studio Build Tools](https://aka.ms/vs/17/release/vs\_BuildTools.exe) and install "Desktop development with C++". It can be from 2019 or later.

#### optional developer requirements

* IDE: [Visual Studio Code](https://code.visualstudio.com/Download)
* We also use [Git Extensions](https://gitextensions.github.io/) to easily switch between versions

### download repo

* Execute the following command in a power shell prompt inside the folder you want to have your OctoBot:\
  `git clone https://github.com/techfreaque/OctoBot-2`

### create virtual environment

* To be able to run PowerShell scripts on your windows computer, you must run the following command in a power shell prompt and confirm the policy change:\
  `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
* right click on the create\_venv.ps1 and then click "Run with PowerShell"

### install/update packages

* if you just want to use it without editing the underlying source code, execute (Right click and then click "Run with Powershell"):\
  `update-ENDUSER-octobot-packages.ps1`
* If you want to edit the underlying source code, execute (Right click and then click "Run with Powershell"):\
  `update-DEVELOPER-octobot-packages.ps1`\
  Developer mode will only work, if you've never used the script update-ENDUSER-octobot-packages.ps1 before. Start fresh if you want to develop.

### Start

#### Start script

* execute start-octobot.ps1 script to start OctoBot (Right click and then click "Run with Powershell")

#### Start with VSCode

* Or open the OctoBot-2 folder with VSCode and press F5 on your keyboard to start OctoBot

### Use the latest nightly version (optional)

* You can use Git Extensions to check out the latest version on the dev branch.
* Usually the dev branch is pretty stable, but you should definitely use the main branch for production.
