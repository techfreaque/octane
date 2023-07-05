git stash
git pull
git checkout main
git pull

timedatectl set-ntp true

mkdir -p user
cp -n ./octobot-packages/OctoBot/octobot/config/default_config.json user/config.json
cp -n scripts/.env-example-unix .env

python -m venv .venv
python3 -m venv .venv

source .venv/bin/activate

chmod u+x scripts/update-octobot-packages.sh
chmod u+x scripts/build-and-install-octobot-tentacles.sh
chmod u+x scripts/cythonize-octobot-packages.sh
chmod u+x linux-docker_install_or_update.sh
chmod u+x linux-start-octane.sh
chmod u+x linux-install-update-and-repair-BETA-octane.sh
chmod u+x linux-install-update-and-repair-STABLE-octane.sh
scripts/update-octobot-packages.sh
scripts/cythonize-octobot-packages.sh
scripts/build-and-install-octobot-tentacles.sh
./linux-start-octane.sh
