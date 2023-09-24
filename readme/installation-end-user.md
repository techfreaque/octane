# Installation (End User)

* [Linux Docker Installation](installation-end-user.md#docker-on-linux-installation) (recommended)
* [Linux Local Installation](installation-end-user.md#linux-local-installation)
* [Windows Docker Installation](installation-end-user.md#docker-on-windows-installation) (recommended)
* [Windows Local Installation](installation-end-user.md#windows-local-installation)

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

### Stop/Start/Restart Octane docker container

```
docker start octane1
docker restart octane1
docker stop octane1
```

### Access the Webinterface
* go to myDomainOrIP.com:5001 or localhost:5001

## Linux Local Installation

[Watch the video installation guide for Ubuntu 22.04](https://youtu.be/XI9L85kkFCA)

### Download and Install Requirements
* git, python3-venv, build-essential, python3-dev

* Use your distros package manager if possible

* On a Debian/Ubuntu based distribution you can install the packages with this command:
    ```
    sudo apt install -y python3-venv git build-essential python3-dev
    ```

### Downloading the Package
 * Open a terminal inside the folder you want your Octane to be installed
    ```
    git clone https://github.com/techfreaque/octane
    ```

### Install / Update / Repair Package

* once you have downloaded the repository through git, you can install it by executing:
    ```
    cd octane
    chmod u+x linux-install-update-and-repair-STABLE-octane.sh
    ./linux-install-update-and-repair-STABLE-octane.sh
    ```

### Start On Linux

* To start Octane on Linux, run:
    ```
    ./linux-start-octane.sh
    ```
### Access the Webinterface
* go to myDomainOrIP.com:5001 or localhost:5001


## Docker on Windows Installation
[Watch the video installation guide for Docker on Windows](https://youtu.be/P4bEarM7GRE)
### Download and Install Requirements

Make sure you have git and docker installed on your windows machine

* [Git](https://git-scm.com/downloads)
* [Docker](https://www.docker.com/products/docker-desktop/)
* Time drifting can be an issue on Windows, you can solve it by auto-syncing your time periodically with a tool like [Time Sync tool](http://www.timesynctool.com/)

### Downloading the Package
* open a power shell promt in the folder you want your octane and execute the following command:
    ```
    git clone https://github.com/techfreaque/octane
    ```

### Install/Start & Update the docker container

* make sure docker is running and set up properly
* open the new octane folder and right click on windows-docker_install_or_update.ps1 and click run with powershell
* Once the installation is done your Octane should be up and running
* Note that your octane will start automatically with windows

### Stop/Start/Restart Octane docker container

* You can start/stop/restart the container with docker desktop or run the following commands
    ```
    docker start octane1
    docker restart octane1
    docker stop octane1
    ```

### Access the Webinterface
*  go to myDomainOrIP.com:5001 or localhost:5001

## Windows Local Installation
[Watch the video installation guide for installing locally on Windows](https://youtu.be/SjYHsxf7Xu0)

### Download and Install Requirements

* Make sure you have git installed on your Windows PC. [Download Git](https://git-scm.com/downloads)
* Time drifting can be an issue on Windows, you can solve it by auto-syncing your time periodically with a tool like [Time Sync tool](http://www.timesynctool.com/)

### Downloading the Package

* Execute this command in a PowerShell window inside the folder you want your Octane instance to be.

    ```
    git clone https://github.com/techfreaque/octane
    ```

### Install Visual Studio Build Tools

1. open the just downloaded octane folder and execute the file vs_build_tools.exe in windows_dependecies.
2. Select "Desktop Development with C++" and install it


### Install / Update / Repair Package

once you have downloaded the repository through git, you can install it by:
1. To be able to run PowerShell scripts on your windows computer, you must run the following command in a power shell prompt and confirm the policy change:\
    ```
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```

1. Right-click on the file windows-install-repair-and-update-to-STABLE-installation.ps1
2. Click on run with PowerShell, once the installation is completed, your bot will start automatically.

### Start On Windows

* To start Octane on Windows, just double-click the Windows-Start-Octane.exe file

### Access the Webinterface
* go to myDomainOrIP.com:5001 or localhost:5001
