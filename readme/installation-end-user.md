# Installation (End User)

* [Docker Linux Installation](installation-end-user.md#docker-on-linux-installation)
* [Linux Local Installation](installation-end-user.md#linux-local-installation)
* [Windows Installation](installation-end-user.md#windows-installation)

## Docker on Linux Installation

### Download and Install Requirements

Make sure you have git and docker installed on your linux machine, use your distros package manager if possible

* [Git](https://git-scm.com/downloads)
* [Docker](https://www.docker.com/products/docker-desktop/)

### Downloading the Package

```
git clone https://github.com/techfreaque/octane
```

### Install/Start & Update the docker container

* make sure docker is running and set up properly
* execute the following commands in a shell, to install/update and start the docker container:

```
cd octane
chmod u+x linux-docker_install_or_update.sh # only on the first run
./linux-docker_install_or_update.sh
```

### Stop/Start/Restart OctoBot docker container

```
docker start octobot
docker restart octobot
docker stop octobot
```

### Access the Webinterface
* go to myDomainOrIP.com:5001 

## Linux Local Installation

### Download and Install Requirements
* git
* python3-venv

* Use your distros package manager if possible

* On a Debian/Ubuntu based distribution you can install the packages with this command:
    ```
    sudo apt install -y python3-venv git
    ```

### Downloading the Package
 * Open a terminal inside the folder you want your Octane to be installed
    ```
    git clone https://github.com/techfreaque/octane
    ```

### Install / Update / Repair Package

once you have downloaded the repository through git, you can install it by executing:

```
cd octane
chmod u+x linux-install-update-and-repair-STABLE-octane.sh
./linux-install-update-and-repair-STABLE-octane.sh
```

## Start On Linux

To start Octane on Linux, run:
```
./linux-start-octane.sh
```
### Access the Webinterface
* go to myDomainOrIP.com:5001 
## Windows Installation

### Download and Install Requirements



* Make sure you have git installed on your Windows PC. [Download Git](https://git-scm.com/downloads)
* Time drifting can be an issue on Windows, you can solve it by auto-syncing your time periodically with a tool like [Time Sync tool](http://www.timesynctool.com/)

### Downloading the Package

Execute this command in a PowerShell window inside the folder you want your OctoBot instance to be.

```
git clone https://github.com/techfreaque/octane
```

### Install / Update / Repair Package

once you have downloaded the repository through git, you can install it by:
1. To be able to run PowerShell scripts on your windows computer, you must run the following command in a power shell prompt and confirm the policy change:\
```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser```

1. Right-click on the file windows-install-repair-and-update-to-STABLE-installation.ps1
2. Click on run with PowerShell, once the installation is completed, your bot will start automatically.

### Start On Windows

To start OctoBot on Windows, just double-click the Windows-Start-Octobot.exe file

### Access the Webinterface
* go to myDomainOrIP.com:5001 