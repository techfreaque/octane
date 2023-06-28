git pull
docker build --tag octane -f scripts/Dockerfile-win .

docker stop octane1
docker rm octane1
docker run -d --name octane1 -p 5001:5001 -v $PSScriptRoot/users/user1/user:/octane/user -v $PSScriptRoot/users/user1/tentacles:/octane/tentacles -v $PSScriptRoot/users/user1/logs:/octane/logs -v $PSScriptRoot/users/user1/backtesting:/octane/backtesting octane
docker logs -f octane1
