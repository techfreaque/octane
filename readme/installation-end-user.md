# Installation (End User)

* [Docker Linux Installation](installation-end-user.md#docker-installation-on-linux)
* [Windows Installation](installation-end-user.md#windows-installation)

## Docker on Linux Installation

### Download and Install Requirements

Make sure you have git and docker installed on your linux machine

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
cd OctoBot-2
chmod u+x linux-docker_install_or_update.sh # only on the first run
./linux-docker_install_or_update.sh
```

### **Stop/Start/Restart OctoBot docker container**

```
docker start octobot
docker restart octobot
docker stop octobot
```

## Windows Installation

### Download and Install Requirements



* Make sure you have git installed on your Windows PC. [Download Git](https://git-scm.com/downloads)
* Time drifting can be an issue on Windows, you can solve it by auto-syncing your time periodically with a tool like [Time Sync tool](http://www.timesynctool.com/)

### Downloading the Package

#### Download it through git

Execute this command in a PowerShell window inside the folder you want your OctoBot instance to be.

```
git clone https://github.com/techfreaque/octane
```

#### Install / Update / Repair Package

once you have downloaded the repository through git, you can install it by:

1. Right-click on the file windows-install-repair-and-update-to-STABLE-installation.ps1
2. Click on run with PowerShell, once the installation is completed, your bot will start automatically.

**Start On Windows**

To start OctoBot on Windows, just double-click the Windows-Start-Octobot.exe file

##
