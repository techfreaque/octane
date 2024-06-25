
# make sure the time sync is active on host 
timedatectl set-ntp true

git stash
git pull
chmod +x linux-docker_install_or_update.sh
cp -n scripts/.env-example-unix .env
cp -n scripts/custom_requirements.txt.template custom_requirements.txt
source ./.env
DOCKER_PYTHON_VERSION=${DOCKER_PYTHON_VERSION:-3.11}
echo using python $DOCKER_PYTHON_VERSION
docker build --tag octane --build-arg "DOCKER_PYTHON_VERSION=$DOCKER_PYTHON_VERSION" -f scripts/Dockerfile .

if [ -z "$AMOUNT_OF_DOCKER_INSTANCES" ]
then
      AMOUNT_OF_DOCKER_INSTANCES=1
fi

for n in $(seq 1 $AMOUNT_OF_DOCKER_INSTANCES)
do
    docker stop octane$n
    docker rm octane$n
    docker run -d --name octane$n -p 500$n:5001 -p 900$n:9000 -v $PWD/users/user$n/user:/octobot/user -v $PWD/users/user$n/tentacles:/octobot/tentacles -v $PWD/users/user$n/logs:/octobot/logs -v $PWD/users/user$n/backtesting:/octobot/backtesting octane
done

# docker logs -f octane1
