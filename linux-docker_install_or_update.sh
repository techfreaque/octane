
# make sure the time sync is active on host 
timedatectl set-ntp true

git stash
git pull
chmod +x linux-docker_install_or_update.sh
cp -n scripts/.env-example-unix .env
docker build --tag octane -f scripts/Dockerfile .

docker stop octane1
docker rm octane1
docker run -d --name octane1 -p 5001:5001 -p 9000:9000 -v $PWD/users/user1/user:/octobot/user -v $PWD/users/user1/tentacles:/octobot/tentacles -v $PWD/users/user1/logs:/octobot/logs -v $PWD/users/user1/backtesting:/octobot/backtesting octane
# docker logs -f octane1
