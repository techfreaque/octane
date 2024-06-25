git pull

$sourceFile = 'scripts/.env-example-unix'
$destinationFile = '.env'
if (-not (test-path $destinationFile))
{
  $opts = @{'path' = $sourceFile; 'destination' = $destinationFile; 'confirm' = $false}
  copy-item @opts
}
if (!(Test-Path "custom_requirements.txt"))
{
    Copy-Item "scripts/custom_requirements.txt.template" -Destination "custom_requirements.txt"
}

$DOCKER_PYTHON_VERSION = $env:DOCKER_PYTHON_VERSION
if (-not $DOCKER_PYTHON_VERSION) {
    $DOCKER_PYTHON_VERSION = "3.11"
}

docker build --tag octane --build-arg "DOCKER_PYTHON_VERSION=$DOCKER_PYTHON_VERSION" -f scripts/Dockerfile-win .

docker stop octane1
docker rm octane1
docker run -d --name octane1 -p 5001:5001 -v $PSScriptRoot/users/user1/user:/octobot/user -v $PSScriptRoot/users/user1/tentacles:/octobot/tentacles -v $PSScriptRoot/users/user1/logs:/octobot/logs -v $PSScriptRoot/users/user1/backtesting:/octobot/backtesting octane
docker logs -f octane1
