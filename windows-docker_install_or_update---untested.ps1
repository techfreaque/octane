git pull
docker build --tag octobot .

docker stop octobot1
docker rm octobot1
docker run -d --name octobot1 -p 5001:5001 -v $PSScriptRoot/users/user1/user:/octobot/user -v $PSScriptRoot/users/user1/tentacles:/octobot/tentacles -v $PSScriptRoot/users/user1/logs:/octobot/logs -v $PSScriptRoot/users/user1/backtesting:/octobot/backtesting octobot
# docker logs -f octobot1
