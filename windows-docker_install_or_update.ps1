git stash
git pull

$sourceFile = 'scripts/.env-example-unix'
$destinationFile = '.env'
if (-not (test-path $destinationFile)) {
  $opts = @{'path' = $sourceFile; 'destination' = $destinationFile; 'confirm' = $false }
  copy-item @opts
}

# Read and process the .env file
Get-Content $destinationFile | ForEach-Object {
  # Skip empty lines and lines starting with #
  if ($_ -and $_ -notmatch '^#') {
      # Split the line into key and value
      $parts = $_ -split '=', 2
      $key = $parts[0].Trim()
      $value = $parts[1].Trim()
      
      # Set the environment variable
      [System.Environment]::SetEnvironmentVariable($key, $value)
  }
}

if (!(Test-Path "custom_requirements_to_uninstall.txt")) {
  Copy-Item "scripts/custom_requirements_to_uninstall.txt.template" -Destination "custom_requirements_to_uninstall.txt"
}

if (!(Test-Path "custom_requirements.txt")) {
  Copy-Item "scripts/custom_requirements.txt.template" -Destination "custom_requirements.txt"
}

$DOCKER_PYTHON_VERSION = $env:DOCKER_PYTHON_VERSION
if (-not $DOCKER_PYTHON_VERSION) {
  $DOCKER_PYTHON_VERSION = "3.11"
}
Write-Output "using python $DOCKER_PYTHON_VERSION"

docker build --tag octane --build-arg "DOCKER_PYTHON_VERSION=$DOCKER_PYTHON_VERSION" -f scripts/Dockerfile-win .

# Check if AMOUNT_OF_DOCKER_INSTANCES is not set or empty
if (-not $env:AMOUNT_OF_DOCKER_INSTANCES) {
  $env:AMOUNT_OF_DOCKER_INSTANCES = 1
}

# Loop through the number of Docker instances
for ($n = 1; $n -le $env:AMOUNT_OF_DOCKER_INSTANCES; $n++) {
  docker stop octane$n
  docker rm octane$n
  docker run -d --name octane$n -p 500${n}:5001 -p 900${n}:9000 -v "$PSScriptRoot/users/user$n/user:/octobot/user" -v "$PSScriptRoot/users/user$n/tentacles:/octobot/tentacles" -v "$PSScriptRoot/users/user$n/logs:/octobot/logs" -v "$PSScriptRoot/users/user$n/backtesting:/octobot/backtesting" octane
}

docker logs -f octane1
