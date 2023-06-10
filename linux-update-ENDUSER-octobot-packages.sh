git stash
git pull
git checkout main
git pull

cp -n ./octobot-packages/OctoBot/octobot/config/default_config.json user/config.json
cp -n .env-example-unix .env

python -m venv .venv
source .venv/bin/activate

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
