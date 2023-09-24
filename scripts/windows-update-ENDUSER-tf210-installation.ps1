git checkout tf210
git reset --hard origin/tf210
git pull
scripts\update-octobot-packages.ps1
scripts\cythonize-octobot-packages.ps1
scripts\build-and-install-octobot-tentacles.ps1