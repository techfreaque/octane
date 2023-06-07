
# make sure the time sync is active on host 
timedatectl set-ntp true


git pull
chmod u+x linux-docker_install_or_update.sh
docker build --tag octobot .

docker stop octobot
docker rm octobot
docker run -d --name octobot -p 5001:5001 -v $PWD/users/user1/user:/octobot/user -v $PWD/users/user1/tentacles:/octobot/tentacles -v $PWD/tentacles:/octobot/reference_tentacles -v $PWD/reference_profiles:/octobot/reference_profiles -v $PWD/users/user1/logs:/octobot/logs -v $PWD/users/user1/backtesting:/octobot/backtesting octobot
# docker logs -f octobot
