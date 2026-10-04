#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
    ./utils/generate-env.sh
fi

# allow containers to draw windows on the host display
xhost +local:docker
docker compose up -d
echo "Container started. Open a terminal using the script new-terminal.sh"
