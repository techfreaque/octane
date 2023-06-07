git stash
git pull
git checkout main
git pull

chmod u+x scripts/update-octobot-packages.sh
chmod u+x scripts/build-and-install-octobot-tentacles.sh
chmod u+x scripts/cythonize-octobot-packages.sh
chmod u+x linux-docker_install_or_update.sh
chmod u+x linux-start-octobot.sh
chmod u+x linux-update-DEVELOPER-octobot-packages.sh
chmod u+x linux-update-ENDUSER-octobot-packages.sh
scripts/update-octobot-packages.sh
scripts/cythonize-octobot-packages.sh
scripts/build-and-install-octobot-tentacles.sh
./linux-start-octobot.sh
