git checkout main
git reset --hard origin/main
git pull
scripts\update-octobot-packages.ps1
scripts\cythonize-octobot-packages.ps1
scripts\build-and-install-octobot-tentacles.ps1