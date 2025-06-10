if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi
source ${PWD}/.venv/bin/activate
Octane
