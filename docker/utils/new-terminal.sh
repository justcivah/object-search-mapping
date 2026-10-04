#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

# fail message if the container is not running
if ! docker compose ps --status running --services | grep -qx ros2; then
    echo "Error: ros2 container is not running. Start it with scripts/run.sh" >&2
    exit 1
fi

docker compose exec ros2 bash
